import sys
from loguru import logger

logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{message}</level>")
logger.add("file.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", rotation="1 week")


class AquariumLogger:

    def info(self, message):
        logger.info(message)

    def debug(self, message):
        logger.debug(message)

    def error(self, message):
        logger.error(message)
