import sys
import os
import logging.handlers

LOGGER = logging.getLogger('messenger.server')
FORMATTER = logging.Formatter(
    "%(asctime)s -- %(levelname)s -- в файле %(filename)s -- в строке %(lineno)d -- %(message)s")
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'server_logs/log_file.log')

TO_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf-8', interval=1, when='H')
TO_FILE.setFormatter(FORMATTER)
TO_FILE.setLevel(logging.DEBUG)
TO_STDERR = logging.StreamHandler(sys.stderr)
TO_STDERR.setFormatter(FORMATTER)
TO_STDERR.setLevel(logging.ERROR)

LOGGER.addHandler(TO_FILE)
LOGGER.addHandler(TO_STDERR)
LOGGER.setLevel(logging.DEBUG)

if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')