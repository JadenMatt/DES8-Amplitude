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

# Retry Variables

max_retry  = 5
attempt = 0
delay = 10

#API call error handling
while attempt < max_retry:


    #API Call and status response

    response = requests.get(url, params=params, auth=(amp_api_key, amp_secret_key))
    print (response.status_code)

    if response.status_code == 200: 
        data = response.content
        print('Data retrieved successfully! :)')
        with open(filename, 'wb') as file:
            file.write(data)
        break
    else:
        print(f'Error {response.status_code}')
        break 