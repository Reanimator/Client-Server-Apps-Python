"""Программа-сервер"""

import socket
import sys
import argparse
import logging
import select
import time
from logs.configs.decors import log_inspector
from common.variables import DEFAULT_PORT, MAX_CONNECTIONS, ACTION, TIME, USER, \
    ACCOUNT_NAME, SENDER, PRESENCE, RESPONSE, ERROR, MESSAGE, MESSAGE_TEXT
from common.utils import get_message, send_message

LOGGER_SERVER = logging.getLogger('messenger.server')


@log_inspector
def process_client_message(message, messages_list, client):
    """
    Обработчик сообщений от клиентов, принимает словарь - сообщение от клинта,
    проверяет корректность, отправляет словарь-ответ для клиента с результатом приёма.
    :param message:
    :param messages_list:
    :param client:
    :return:
    """
    LOGGER_SERVER.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


@log_inspector
def arg_parser():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    if not 1023 < listen_port < 65536:
        LOGGER_SERVER.critical(f'Запуска сервера с неподходящим портом {listen_port}. Допустимы с 1024 до 65535.')
        sys.exit(1)

    return listen_address, listen_port


@log_inspector
def main():
    """Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию"""
    listen_address, listen_port = arg_parser()
    LOGGER_SERVER.info(f'Запущен сервер, с портом: {listen_port} и адресом: {listen_address}.')
    print("Режим работы - сервер")
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.1)
    clients = []
    messages = []
    transport.listen(MAX_CONNECTIONS)
    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            LOGGER_SERVER.info(f'Установлено соедение с ПК {client_address}')
            clients.append(client)
        recv_data_lst = []
        send_data_lst = []
        err_lst = []
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message)
                except:
                    LOGGER_SERVER.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)
        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    LOGGER_SERVER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
