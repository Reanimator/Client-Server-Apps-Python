"""Программа-сервер"""

import socket
import sys
import json
import logging
import logs.configs.config_server_log
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message

LOGGER_SERVER = logging.getLogger('messenger.server')


def process_client_message(message):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :return:
    '''
    LOGGER_SERVER.debug(f'Принято сообщение от клиента: {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and str(message["time"]).replace('.', '', 1).isdigit() and USER in message \
            and message[USER][ACCOUNT_NAME] == 'Guest':
        LOGGER_SERVER.debug(f'Сообщение {message} допустимо')
        return {RESPONSE: 200}
    LOGGER_SERVER.debug(f'Сообщение {message} не допустимо')
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    '''
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8079 -a 192.168.1.2
    :return:
    '''

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if not 1023 < listen_port < 65536:
            LOGGER_SERVER.critical(f'Запуск сервера с недопустимым портом {listen_port} невозможен')
            raise ValueError
    except IndexError:
        LOGGER_SERVER.error('При запуске сервера указан неверно параметр \'p\'')
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        print(
            'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Затем загружаем какой адрес слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
            LOGGER_SERVER.debug(f'Выбран адрес {listen_address} для прослушивания')
        else:
            listen_address = ''
            LOGGER_SERVER.debug('Сервер слушает все адреса')

    except IndexError:
        LOGGER_SERVER.error('При запуске сервера указан неверно параметр \'a\'')
        print(
            'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    # Готовим сокет

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    LOGGER_SERVER.debug('Сокет подготовлен')

    # Слушаем порт

    transport.listen(MAX_CONNECTIONS)
    LOGGER_SERVER.debug('Слушаем порт')

    while True:
        client, client_address = transport.accept()
        try:
            message_from_cient = get_message(client)
            print(message_from_cient)
            # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
            response = process_client_message(message_from_cient)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            logging.error('Принято некорретное сообщение от клиента.')
            print('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
