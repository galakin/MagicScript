import logging
import datetime


def loggin_messages(msg, logging_file="pythonScript.log", log_level="INFO"):
    logger = logging.getLogger(__name__)

    # Add the handler to the logger

    if log_level == "INFO":
        logging.basicConfig(filename=logging_file, level=logging.INFO)
        logger.info(msg)
        print(str(datetime.datetime.today()) + " - INFO - " + str(msg))
    return 0
