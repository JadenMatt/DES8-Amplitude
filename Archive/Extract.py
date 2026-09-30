# Import Packages

import requests
import os
import json
from datetime import datetime, timedelta
import logging
import boto3
from dotenv import load_dotenv
import zipfile
import gzip
import shutil

# Define Variables

# Load in .env file for API keys

load_dotenv()

amp_api_key = os.getenv('AMP_API_KEY')
amp_secret_key = os.getenv('AMP_SECRET_KEY')


# AWS Access Key Details

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')


# Calling previous day

Previous_Day = datetime.now() - timedelta(days=1)
starttime_hour = 00
endtime_hour = 23

starttime = Previous_Day.strftime(f'%Y%m%dT{starttime_hour}')
endtime = Previous_Day.strftime(f'%Y%m%dT{endtime_hour}')


url = 'https://analytics.eu.amplitude.com/api/2/export'

params = {
        'start': starttime,
        'end': endtime
}

# Local data folder and filename

data_dir= 'data'
os.makedirs(data_dir, exist_ok=True)

temp_dir= 'data/temp_dir'
os.makedirs(temp_dir, exist_ok=True)

json_dir= 'data/JSON_data'
os.makedirs(json_dir, exist_ok=True)


timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S') # - Don't use / when creating a file name
zip_filename = f'{data_dir}/{timestamp}.zip' 

#Create log folder

log_dir = 'log'
os.makedirs(log_dir, exist_ok = True)
log_filename = f'{log_dir}/{timestamp}.log'

#Configure logging messages

logging.basicConfig(
    filename = log_filename,
    filemode = "a", # Append new logs to file by default, can be "w" to overwrite the file
    format = "%(levelname)s:%(name)s:%(message)s", # format for content output in log file
    level=logging.WARNING, # minimum serverity for log to be recorded in a log file
)

#Create the logger

logger = logging.getLogger()

logger.debug("This is a debug message")    
logger.info("System working :)")            
logger.warning("Something unexpected :(")        
logger.error("An error occurred :'(")             
logger.critical("Critical system error </3")

# session = boto3.Session( AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)


# s3 = session.resource('s3')

# my_bucket = s3.Bucket(AWS_BUCKET_NAME)

# s3_file_list = []

# for my_bucket_object in my_bucket.objects.all():
#   s3_file_list.append(my_bucket_object.key)
  

# # Get list of Local directory files

# concat_file_list = ' '.join(s3_file_list)
# JSON_List = os.listdir('data/JSON_data')

# for object in JSON_List:
#     if concat_file_list.find(object) != -1:
#         print(f'{object} already in bucket')
#     else:
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

logger.info("Process Finished")