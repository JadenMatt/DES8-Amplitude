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

file_to_upload = 'data/JSON_data/100011471_2026-09-24_0#0.json'
filename_s3 = '100011471_2026-09-24_0#0.json'

S3_client.upload_file(file_to_upload, AWS_BUCKET_NAME, filename_s3)
print('Upload Successful')