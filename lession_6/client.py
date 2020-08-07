"""Программа-клиент"""

import sys
import json
import socket
import time
import logging
from logs.configs.decors import log_inspector
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message


LOGGER_CLIENT = logging.getLogger('messenger.client')


@log_inspector
def create_presence(account_name='Guest'):
    '''
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    '''
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    LOGGER_CLIENT.debug(f'Сгенерирован запрос с сообщением {PRESENCE} для {account_name}')
    return out


@log_inspector
def process_ans(message):
    '''
    Функция разбирает ответ сервера
    :param message:
    :return:
    '''
    if RESPONSE in message:
        LOGGER_CLIENT.info(f'Получен код от сервера {message[RESPONSE]}')
        if message[RESPONSE] == 200:
            LOGGER_CLIENT.debug('Отправлено - 200 : OK')
            return '200 : OK'
        elif message[RESPONSE] == 400:
            LOGGER_CLIENT.info(f'Отправлено - 400 : {message[ERROR]}')
            return f'400 : {message[ERROR]}'
        else:
            LOGGER_CLIENT.error('Получен неизвестный код')
            return 'Неизвестный код'
    raise ValueError

@log_inspector
def main():
    '''
    Загружаем параметы коммандной строки
    '''
    # client.py 192.168.1.2 8079
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if not 1023 < server_port < 65536:
            LOGGER_CLIENT.critical(f'Запуск клиента с недопустимым портом {server_port} невозможен')
            raise ValueError
        LOGGER_CLIENT.debug(f'Клиент запущен по адресу {server_address} и порту {server_port}')
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
        LOGGER_CLIENT.debug(f'Используемся адрес {server_address} и порт {server_port} по умолчанию')
    except ValueError:
        LOGGER_CLIENT.info('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Инициализация сокета и обмен
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    message_to_server = create_presence()
    send_message(transport, message_to_server)
    LOGGER_CLIENT.debug(f'Отправили сообщение {message_to_server} на сервер')
    try:
        answer = process_ans(get_message(transport))
        LOGGER_CLIENT.info(f'Получен ответ от сервера {answer}')
        print(answer)
    except (ValueError, json.JSONDecodeError):
        LOGGER_CLIENT.error('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
