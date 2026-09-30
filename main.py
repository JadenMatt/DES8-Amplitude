from modules.log_initialiser import setup_log
from datetime import datetime
from modules.extract_initialiser import extractor
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from modules.load_initialiser import load_to_s3

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S') 

logger = setup_log('log', timestamp)
logger.info('logger successfully initiated')

Previous_Day = datetime.now() - timedelta(days=1)
starttime_hour = 00
endtime_hour = 23

starttime = Previous_Day.strftime(f'%Y%m%dT{starttime_hour}')
endtime = Previous_Day.strftime(f'%Y%m%dT{endtime_hour}')

url = 'https://analytics.eu.amplitude.com/api/2/export'

# Local data folder and filename

data_dir= 'data'
os.makedirs(data_dir, exist_ok=True)

temp_dir= 'data/temp_dir'
os.makedirs(temp_dir, exist_ok=True)

json_dir= 'data/JSON_data'
os.makedirs(json_dir, exist_ok=True)

load_dotenv()

amp_api_key = os.getenv('AMP_API_KEY')
amp_secret_key = os.getenv('AMP_SECRET_KEY')

extractor(url, data_dir, temp_dir, json_dir, timestamp, amp_api_key, amp_secret_key, starttime, endtime, starttime_hour, endtime_hour)


load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

files_to_upload = os.listdir('data/JSON_data')

load_to_s3(files_to_upload, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME)