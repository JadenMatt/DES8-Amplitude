# Import Packages

import requests
import os
import json
from datetime import datetime
import logging
import boto3
from dotenv import load_dotenv

# Define Variables

# Load in .env file for API keys

load_dotenv()

amp_api_key = os.getenv('AMP_API_KEY')
amp_secret_key = os.getenv('AMP_SECRET_KEY')

starttime = '20260922T00'
endtime = '20260922T05'

url = 'https://analytics.eu.amplitude.com/api/2/export'

params = {
        'start': starttime,
        'end': endtime
}

# Local data folder and filename

data_dir= 'data'
os.makedirs(data_dir, exist_ok=True)

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S') # - Don't use / when creating a file name
filename = f'{data_dir}/{timestamp}.json' 

#Create log folder

log_dir = 'log'
os.makedirs(log_dir, exist_ok = True)
log_filename = f'{log_dir}/{timestamp}.json'

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



try:


    #API Call and status response

    response = requests.get(url, params=params, auth=(amp_api_key, amp_secret_key))
    print (response.status_code)

    if response.status_code == 200: 
        data = response.content
        print('Data retrieved successfully! :)')
        logger.info("Data retrieved successfully")
        logger.info("Saving data")
        with open(filename, 'wb') as file:
            file.write(data)
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