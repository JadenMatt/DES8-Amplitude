from modules.log_initialiser import setup_log
from datetime import datetime

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S') 

logger = setup_log('log', timestamp)
logger.info('logger successfully initiated')