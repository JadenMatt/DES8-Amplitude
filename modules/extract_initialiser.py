import os
import zipfile
import logging
import gzip
import shutil
import requests

logger = logging.getLogger(__name__)


def extractor(url:str, data_dir:str, temp_dir:str, json_dir:str, timestamp:str, amp_api_key:str, amp_secret_key:str, starttime:str, endtime:str, starttime_hour:int, endtime_hour:int):
    """ This function will extract and unzip a zip file from the API, place resulting gzip files into a temp folder and extract the JSON data from each gzip file into a JSON directory

    Args:
        url (str): URL you want to download your zip file from
        data_dir (str): Where you want to store your zip file
        temp_dir (str): Where you want to store your gzip files
        json_dir (str): Where you want to store your raw JSON data
        timestamp (str): This will be the filename for your zip file
        amp_api_key (str): API Access Key
        amp_secret_key (str): API Secret Access Key
        starttime (str): The starting date
        endtime (str): The ending date
        starttime_hour (int): The starting hour
        endtime_hour (int): The ending hour
    """
    params = {
        'start': starttime,
        'end': endtime
    }

    zip_filename = f'{data_dir}/{timestamp}.zip' 

    try:
        #API Call and status response
        
        response = requests.get(url, params=params, auth=(amp_api_key, amp_secret_key))

        if response.status_code == 200: 
            data = response.content
            print('Data retrieved successfully! :)')
            logger.info("Data retrieved successfully")
            logger.info("Saving data")
            with open(zip_filename, 'wb') as file:
                    file.write(data)
            with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
    # Open gzip files inside extracted folder (handles nested sub-folders)
            for root, dirs, files in os.walk(temp_dir):
                for file_name in files:
                    if file_name.endswith('.gz'):
                        # Full path to the compressed file inside root
                        gz_file_paths = os.path.join(root, file_name)
                        
                        # Strip .gz extension for output file
                        json_file_name = file_name[:-3]
                        JSON_output_file_path = os.path.join(json_dir, json_file_name)

                        with gzip.open(gz_file_paths, 'rb') as f_in:
                            with open(JSON_output_file_path, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)

            logger.info("Data Saved, W code")
        elif response.status_code == 400:
            print('File size to large, shorten time range and try again! :(')
            logger.error(f"API Call Error '{response.status_code}: {response.text}, L code'")

        elif response.status_code == 404:
            print('No data available in time range, change time range and try again! :(')
            logger.error(f"API Call Error '{response.status_code}: {response.text}, L code'")

        elif response.status_code == 504:
            print('Timeout, consider Amazon S3 destination and try again! :(')
            logger.error(f"API Call Error '{response.status_code}: {response.text}, L code'")
        else:
            print(f'Error {response.status_code}')
            logger.error(f"API Call Error '{response.status_code}: {response.text}, L code'")
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        print(f"Request failed: {e}")