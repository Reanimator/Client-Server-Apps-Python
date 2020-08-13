"""Программа-клиент"""

import sys
import json
import socket
import time
import logging
import argparse
from logs.configs.decors import log_inspector
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER
from errors import ReqFieldMissingError, ServerError
from common.utils import get_message, send_message


LOGGER_CLIENT = logging.getLogger('messenger.client')


@log_inspector
def message_from_server(message):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        LOGGER_CLIENT.info(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        LOGGER_CLIENT.error(f'Получено некорректное сообщение с сервера: {message}')


@log_inspector
def create_message(sock, account_name='Guest'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    message = input('Введите сообщение для отправки или \'exit\' для завершения работы: ')
    if message == 'exit':
        sock.close()
        LOGGER_CLIENT.info('Завершение работы по команде пользователя.')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    LOGGER_CLIENT.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@log_inspector
def create_presence(account_name='Guest'):
    '''
    Функция генерирует запрос о присутствии клиента
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
    '''
    LOGGER_CLIENT.debug(f'Разбор приветственного сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise ServerError(f'400 : {message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


@log_inspector
def arg_parser():
    """Создаём парсер аргументов коммандной строки
    и читаем параметры, возвращаем 3 параметра
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode
    if not 1023 < server_port < 65536:
        LOGGER_CLIENT.critical(f'Неподходящий номер порта: {server_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    if client_mode not in ('listen', 'send'):
        LOGGER_CLIENT.critical(f'Недопустимый режим работы {client_mode}. Допустимые режимы: listen , send')
        sys.exit(1)
    return server_address, server_port, client_mode


@log_inspector
def main():
    '''
    Загружаем параметы коммандной строки
    '''
    server_address, server_port, client_mode = arg_parser()

    LOGGER_CLIENT.info(f'Запущен клиент с адресом сервера: {server_address}, '
                       f'портом: {server_port} и режимом работы: {client_mode}')
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence())
        answer = process_ans(get_message(transport))
        LOGGER_CLIENT.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        LOGGER_CLIENT.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError as error:
        LOGGER_CLIENT.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        LOGGER_CLIENT.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        LOGGER_CLIENT.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}')
        sys.exit(1)
    else:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            if client_mode == 'send':
                try:
                    send_message(transport, create_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOGGER_CLIENT.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)
            if client_mode == 'listen':
                try:
                    message_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOGGER_CLIENT.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
