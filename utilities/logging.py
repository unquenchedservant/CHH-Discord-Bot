import logging
import logging.config
import utilities
from utilities import Config

config = Config(True) # EDIT THIS LATER TO NOT HAVE A BOOLEAN
logging.config.fileConfig("logging.conf")

logger = logging.getLogger()
if config.is_dev:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

def setLoggerLevel(is_dev):
    if is_dev:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

