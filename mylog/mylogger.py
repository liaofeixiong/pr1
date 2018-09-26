import logging

formatstr = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=formatstr)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("D:\\log.txt"))
#log info
def info(msg):
    logger.info(str(msg))


#log exception
def error(msg):
    logger.error(str(msg))
    if isinstance(msg, Exception):
        logger.error(msg.__context__)
        logger.error(msg.__cause__)