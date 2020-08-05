import sys
import os
import logging.handlers
from common.variables import LOG_LEVEL

LOGGER = logging.getLogger('messenger.client')
FORMATTER = logging.Formatter(
    "%(asctime)s -- %(levelname)s -- в файле %(filename)s -- в строке %(lineno)d -- %(message)s")
PATH = os.path.dirname(os.path.abspath(__file__))
print(PATH)
PATH = os.path.join(PATH, '..', 'client_logs/log_file.log')
print(PATH)

TO_FILE = logging.handlers.TimedRotatingFileHandler(
    PATH, encoding='utf-8', interval=1, when='H')
TO_FILE.setFormatter(FORMATTER)
TO_FILE.setLevel(LOG_LEVEL)
TO_STDERR = logging.StreamHandler(sys.stderr)
TO_STDERR.setFormatter(FORMATTER)
TO_STDERR.setLevel(logging.ERROR)

LOGGER.addHandler(TO_FILE)
LOGGER.addHandler(TO_STDERR)

LOGGER.debug("в файл")
LOGGER.error("в файл и консоль")
