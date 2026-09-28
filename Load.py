import os
import boto3
import logging
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

S3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


files_to_upload = os.listdir('data/JSON_data')

for file in files_to_upload:

    try:
        filepath = f'data/JSON_data/{file}'
        S3_client.upload_file(filepath, AWS_BUCKET_NAME, file)
        print(f'{file} uploaded successfully')
        os.remove(filepath)
    except Exception as e:
        print(f'An error has occured {e}')

