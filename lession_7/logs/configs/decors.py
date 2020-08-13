import sys
import os
import logging
import logging.handlers
import inspect


def log_inspector(log_func):
    def log_saver(*args, **kwargs):
        if sys.argv[0].find('client') == -1:
            LOGGER = logging.getLogger('messenger.server')
            PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'server_logs/log_file.log')
        else:
            LOGGER = logging.getLogger('messenger.client')
            PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'client_logs/log_file.log')
        FORMATTER = logging.Formatter(
            "%(asctime)s -- %(levelname)s -- в файле %(filename)s -- в строке %(lineno)d -- %(message)s")
        TO_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf-8', interval=1, when='H')
        TO_FILE.setFormatter(FORMATTER)
        TO_FILE.setLevel(logging.DEBUG)
        TO_STDERR = logging.StreamHandler(sys.stderr)
        TO_STDERR.setFormatter(FORMATTER)
        TO_STDERR.setLevel(logging.ERROR)

        LOGGER.addHandler(TO_FILE)
        LOGGER.addHandler(TO_STDERR)
        LOGGER.setLevel(logging.DEBUG)
        LOGGER.debug(f'Вызвана функция {log_func.__name__} c параметрами {args}, {kwargs}'
                     f' из модуля {log_func.__module__} из функции {inspect.stack()[1][3]}')
        out = log_func(*args, **kwargs)
        return out
    return log_saver
