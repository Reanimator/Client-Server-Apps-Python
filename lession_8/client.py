"""Программа-клиент"""

import sys
import json
import socket
import time
import logging
import argparse
import threading
from logs.configs.decors import log_inspector
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER, EXIT, DESTINATION
from errors import ReqFieldMissingError, ServerError
from common.utils import get_message, send_message


LOGGER_CLIENT = logging.getLogger('messenger.client')




@log_inspector
def create_exit_message(account_name):
    """Функция создаёт словарь с сообщением о выходе"""
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: account_name
    }


@log_inspector
def message_from_server(sock, my_username):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    while True:
        message = get_message(sock)
        if ACTION in message and message[ACTION] == MESSAGE and \
                    SENDER in message and DESTINATION in message \
                    and MESSAGE_TEXT in message and message[DESTINATION] == my_username:
            print(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
            LOGGER_CLIENT.info(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        else:
            LOGGER_CLIENT.error(f'Получено некорректное сообщение с сервера: {message}')


@log_inspector
def create_message(sock, account_name='Guest'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    to_user = input('Введите получателя сообщения: ')
    message = input('Введите сообщение для отправки:')
    message_dict = {
        ACTION: MESSAGE,
        SENDER: account_name,
        DESTINATION: to_user,
        TIME: time.time(),
        MESSAGE_TEXT: message
    }
    LOGGER_CLIENT.debug(f'Сформирован словарь сообщения: {message_dict}')
    try:
        send_message(sock, message_dict)
        LOGGER_CLIENT.info(f'Отправлено сообщение для пользователя {to_user}')
    except:
        LOGGER_CLIENT.critical('Потеряно соединение с сервером.')
        sys.exit(1)


@log_inspector
def user_interactive(sock, username):
    """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'm':
            create_message(sock, username)
        elif command == 'h':
            print_help()
        elif command == 'q':
            send_message(sock, create_exit_message(username))
            print('Завершение соединения.')
            LOGGER_CLIENT.info('Завершение работы по команде пользователя.')
            time.sleep(1)
            break
        else:
            print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')


def print_help():
    """Функция выводящяя справку по использованию"""
    print('Можно ввести:')
    print('m - отправить сообщение.')
    print('h - подсказки по командам')
    print('q - выход')


@log_inspector
def create_presence(account_name='Guest'):
    '''
    Функция генерирует запрос о присутствии клиента
    '''
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
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name
    if not 1023 < server_port < 65536:
        LOGGER_CLIENT.critical(f'Неподходящий номер порта: {server_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    return server_address, server_port, client_name


@log_inspector
def main():
    '''
    Загружаем параметы коммандной строки
    '''
    server_address, server_port, client_name = arg_parser()

    LOGGER_CLIENT.info(f'Запущен клиент с адресом сервера: {server_address}, '
                       f'портом: {server_port} и режимом работы: {client_name}')
    if not client_name:
        client_name = input('Введите имя пользователя: ')
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence(client_name))
        answer = process_ans(get_message(transport))
        LOGGER_CLIENT.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print('Установлено соединение с сервером.')
        print(f'Имя клиента {client_name}')
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
        receiver = threading.Thread(target=message_from_server, args=(transport, client_name))
        receiver.daemon = True
        receiver.start()

        user_interface = threading.Thread(target=user_interactive, args=(transport, client_name))
        user_interface.daemon = True
        user_interface.start()
        LOGGER_CLIENT.debug('Запущены процессы')

        while True:
            time.sleep(0.5)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break

if __name__ == '__main__':
    main()
