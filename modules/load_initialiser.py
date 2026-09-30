import os
import boto3
import logging


logger = logging.getLogger(__name__)

def load_to_s3(files_to_upload:str, AWS_ACCESS_KEY:str, AWS_SECRET_ACCESS_KEY:str, AWS_BUCKET_NAME:str):
    """ This function will load your JSON data to your s3 bucket

    Args:
        files_to_upload (str): the filepath of your JSON_data folder
        AWS_ACCESS_KEY (str): Linked to AWS IAM user
        AWS_SECRET_ACCESS_KEY (str): Linked to AWS IAM USER
        AWS_BUCKET_NAME (str): s3 location where data is stored
    """


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
            logger.info(f'{file} uploaded successfully')
            os.remove(filepath)
        except Exception as e:
            print(f'An error has occured {e}')
            logger.error(f'An error has occured {e}')