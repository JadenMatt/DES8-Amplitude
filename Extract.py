# Import Packages

import requests
import os
import json
from datetime import datetime
import logging
import boto3
import dotenv

# Define Variables

starttime = '20260924T00'
endtime = '20260924T23'
URL = f'https://amplitude.com/api/2/export?start={starttime}&end={endtime} HTTP/1.1'

amp_api_key = os.getenv('AMP_API_KEY')
amp_secret_key = os.getenv('AMP_SECRET_KEY')

deng_aws_access_key = os.getenv('DENG_AWS_ACCESS_KEY')
deng_aws_secret_key = os.getenv('DENG_AWS_SECRET_KEY')



