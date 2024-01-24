import logging
from common.config import LOG_LEVEL

def setup_logger():
    global LOG_LEVEL

    LOG_LEVEL = LOG_LEVEL.upper()

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
