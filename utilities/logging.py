import logging
import logging.config
import utilities

logging.config.fileConfig("logging.conf")

logger = logging.getLogger()
if utilities.is_dev:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

def setLoggerLevel(is_dev):
    if is_dev:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)