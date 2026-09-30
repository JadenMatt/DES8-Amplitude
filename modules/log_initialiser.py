import os
import logging

def setup_log(log_dir:str, timestamp:str):

    #Create log folder

    log_dir = 'log'
    os.makedirs(log_dir, exist_ok = True)
    log_filename = f'{log_dir}/{timestamp}.log'

    #Configure logging messages

    logging.basicConfig(
        filename = log_filename,
        filemode = "a", # Append new logs to file by default, can be "w" to overwrite the file
        format = "%(levelname)s:%(name)s:%(message)s", # format for content output in log file
        level=logging.warning, # minimum serverity for log to be recorded in a log file
    )

    #Create the logger

    return logging.getLogger()

    logger.debug("This is a debug message")    
    logger.info("System working :)")            
    logger.warning("Something unexpected :(")        
    logger.error("An error occurred :'(")             
    logger.critical("Critical system error </3")