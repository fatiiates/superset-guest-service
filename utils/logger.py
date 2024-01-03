import logging
import os
from utils.environment import Environment

def setup_logger():
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()

    if LOG_LEVEL == 'DEBUG':
        LOG_LEVEL = logging.DEBUG
    elif LOG_LEVEL == 'INFO':
        LOG_LEVEL = logging.INFO
    elif LOG_LEVEL == 'WARNING':
        LOG_LEVEL = logging.WARNING
    elif LOG_LEVEL == 'ERROR':
        LOG_LEVEL = logging.ERROR
    elif LOG_LEVEL == 'CRITICAL':
        LOG_LEVEL = logging.CRITICAL
    else:
        LOG_LEVEL = logging.INFO
    

    logging.basicConfig(level=LOG_LEVEL,  # Set the logging level
                    format='%(asctime)s - %(levelname)s - %(message)s')
