"""main module for client_files app"""

import binascii
import hashlib
import hmac
import json
import os
import sys
import threading
import time
from threading import Thread

from Crypto.PublicKey import RSA
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

from client_files.client_gui import ClientGui, ClientLoginGui
from client_files.client_storage import ClientStorage
from common.arg_parser import ArgParser
from common.decorators import Log
from common.descriptor import ServerPort, ServerHost
from common.jim import JIMClient
from common.metaclasses import ClientVerifier
from common.my_socket import MessengerSocket
from log.client_log_config import client_logger

sock_lock = threading.Lock()


@Log
class MyMessengerClient(MessengerSocket, JIMClient, ArgParser, metaclass=ClientVerifier):
    """client_files"""
    # используем дескриптер ServerPort ServerHost,
    # чтобы проверять номер порта и адрес, к которому хотим подключиться
    port = ServerPort()
    address = ServerHost()

    # используем дескриптер ServerPort ServerHost,
    # чтобы проверять номер порта и адрес, к которому хотим подключиться

    def __init__(self, size=1024, encoding='utf-8'):
        super().__init__(size, encoding)
        # с помощью методов родителя ArgParser берем значения если сервер запущен с параметрами
        self.username = self.get_username()
        self.address = self.get_address()
        self.port = self.get_port()
        self.mode = self.get_mode()
        # поток для получения сообщений
        receiver_thread = Thread(target=self.message_meaning)
        receiver_thread.daemon = True
        # поток для отправки сообщений
        sender_thread = Thread(target=self.message)
        sender_thread.daemon = True
        # thread for command from terminal
        client_thread = Thread(target=self.start)
        client_thread.daemon = True

        self.list_of_threads = [receiver_thread, sender_thread, client_thread]
        # поток для получения сообщений
        # self.receiver_thread = Thread(target=self.message_meaning)
        # self.receiver_thread.daemon = True
        # # поток для отправки сообщений
        # self.sender_thread = Thread(target=self.message)
        # self.sender_thread.daemon = True
        # # thread for command from terminal
        # self.client_thread = Thread(target=self.start)
        # self.client_thread.daemon = True
        self.database = ClientStorage(self.username)

        self.keys = None

    def turn_on(self):
        """
        start a thread of a client_files
        """
        self.list_of_threads[2].start()

    def start(self):
        """
        запускаем клиента: пробуем подключится и отправить
        presence сообщение, далее работаем согласно типу клиента
        :return: -
        """
        try:

            self.send_message(self.jim_create_message('contacts', self.username), self.sock)
            client_logger.info('произошел запрос на получение контактов')
            server_answer = self.sock.recv(self.size)
            client_logger.info(
                f'список контактов: {self.response_meaning(server_answer)}')

        except Exception as exception:
            client_logger.error(f'ошибка отправки presence сообщения: {exception}')
        else:
            # запускаем потоки на прием и отправку сообщений
            time.sleep(1)
            self.list_of_threads[0].start()

            self.list_of_threads[1].start()
            # основной цикл
            while True:
                time.sleep(1)
                if self.list_of_threads[1].is_alive() and self.list_of_threads[0].is_alive():
                    continue
                break

        finally:
            # отправляем сообщение об отключении
            self.exit_messsage()
            time.sleep(2)
            self.sock.close()
            sys.exit(0)

    def login(self, username, password):
        """
        trying to login
        """
        try:
            # Загружаем ключи с файла, если же файла нет, то генерируем новую пару.
            # need to change for whl
            # dir_path = os.path.dirname(os.path.realpath(__file__))
            dir_path = os.getcwd()
            key_file = os.path.join(dir_path, f'{username}.key')
            if not os.path.exists(key_file):
                self.keys = RSA.generate(2048, os.urandom)
                with open(key_file, 'wb') as key:
                    key.write(self.keys.export_key())
            else:
                with open(key_file, 'rb') as key:
                    self.keys = RSA.import_key(key.read())
            client_logger.debug("Keys sucsessfully loaded.")
            # connect to server_files
            try:
                self.sock.connect((self.address, self.port))
            except Exception:
                pass
            client_logger.info(f'connected to server_files [{self.address}:{self.port}]')
            # making hash from password
            passwd_bytes = password.encode('utf-8')
            salt = username.lower().encode('utf-8')
            passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bytes, salt, 10000)
            passwd_hash_string = binascii.hexlify(passwd_hash)
            # sending username and password
            self.presence(username,
                          {'password': passwd_hash_string.decode('ascii'),
                           'public_key': self.keys.publickey().export_key().decode('ascii')})
            server_answer = self.sock.recv(self.size)

            servers_answer_meaning = self.response_meaning(server_answer)
            resulted_hash = hmac.new(passwd_hash_string,
                                     servers_answer_meaning.encode('utf-8'),
                                     'MD5')
            digest = resulted_hash.digest()

            self.presence(username,
                          {'password': passwd_hash_string.decode('ascii'),
                           'public_key': binascii.b2a_base64(digest).decode('ascii')})

            server_answer = self.sock.recv(self.size)
            # decode answer from server_files
            servers_answer_meaning = self.response_meaning(server_answer)
            client_logger.info(
                'получено сообщение от сервера '
                f'[{self.address}:{self.port}]: {servers_answer_meaning}')
            return servers_answer_meaning
        except Exception as exception:
            client_logger.error(f'registration/authentication error: {exception}')

    def presence(self, username, data):
        """
        первичный запрос на подключение к серверу
        :return: -
        """

        # checking username from login dialog and in instance of a class
        if username != self.username:
            self.username = username
        # creating message
        jim_message = self.jim_create_message('presence', username, data)
        # sending message
        self.send_message(jim_message, self.sock)
        client_logger.info(f'отправлено precense сообщение от {self.username}')

    def exit_messsage(self):
        """
        сообщение об отключении от сервера
        :return: -
        """
        self.send_message(self.jim_create_message('exit', self.username), self.sock)
        client_logger.info(f'отправлено exit сообщение от {self.username}')

    def message(self):
        """
        отправка сообщения

        :return: -
        """
        while True:
            to_user = input(
                'кому отправить сообщение '
                '(exit - выйти, contacts - контакты, add - добавить контакт, delete):\n')
            if to_user.lower() == 'exit':
                break
            elif to_user.lower() == 'contacts':
                self.send_message(self.jim_create_message('contacts', self.username), self.sock)
                client_logger.info('произошел запрос на получение контактов')

            elif to_user.lower() == 'add':
                contact = input('введите имя контакта для добавления: ')
                self.send_message(self.jim_create_message('add', self.username, contact), self.sock)
                client_logger.info(f'произошел запрос на добавление контакта {contact}')

            elif to_user.lower() == 'delete':
                contact = input('введите имя контакта для удаления: ')
                self.send_message(self.jim_create_message('delete', self.username, contact),
                                  self.sock)
                client_logger.info(f'произошел запрос на удаление контакта {contact}')

            else:
                message = input('введите сообщение: ')

                self.client_send_message('message', message, to_user)

    def client_send_message(self, message_type, message, to_user=None):
        """
        send any type messages from client_files to server_files/contacts
        """
        self.send_message(self.jim_create_message(message_type, self.username, message, to_user),
                          self.sock)
        client_logger.debug(f'отправлено {message_type} сообщение от {self.username}')
        if message_type == 'message':
            self.database.add_message(to_user,
                                      False,
                                      message)

    def response_meaning(self, response):
        """
        расшифровка ответа сервера
        :param response:
        :return:
        """
        dict_response = json.loads(response.decode())
        client_logger.info(
            f'ответ сервера {dict_response.get("response")} '
            f'({self.get_jim_responses().get(dict_response.get("response"))})')
        return dict_response.get("alert")

    def message_meaning(self):
        """
        расшифровка сообщения от клиента в цикле для потока
        :param response:
        :return:
        """
        while True:
            time.sleep(1)

            try:
                # получить сообщение от пользователя
                message = self.get_message(self.sock)
                if self.get_jim_user() in message:
                    print(f'\n сообщение от  {message[self.get_jim_user()]} '
                          f'[{message[self.get_jim_time()]}]: {message[self.get_jim_data()]}')
                    self.database.add_message(message[self.get_jim_user()],
                                              True,
                                              message[self.get_jim_data()])
                else:
                    print(message['alert'])

            except Exception:
                pass


if __name__ == "__main__":
    my_messenger_client = MyMessengerClient()

    APP = QApplication(sys.argv)  # создание нашего приложение

    LOGIN_OBJ = ClientLoginGui()  # creating login dialog
    LOGIN_OBJ.set_client_obj(my_messenger_client)  # providing client_files to gui

    # checking login - if correct open main windows
    while True:

        if LOGIN_OBJ.exec_() == QtWidgets.QDialog.Accepted:
            # starting client_files threads
            my_messenger_client.turn_on()
            WINDOW_OBJ = ClientGui()  # создаем объект

            WINDOW_OBJ.set_database(my_messenger_client.database)
            WINDOW_OBJ.set_client_obj(my_messenger_client)

            WINDOW_OBJ.listView.setModel(WINDOW_OBJ.contact_list())
            break
        time.sleep(1)


    def data_load():
        """
        то, что будет обновлять по таймеру
        :return: -
        """

        WINDOW_OBJ.refresh_messages_history()


    data_load()
    WINDOW_OBJ.show()  # показываем наше окно

    # Таймер, обновляющий список клиентов 1 раз в секунду
    timer = QTimer()
    timer.timeout.connect(data_load)
    timer.start(1000)

    APP.exec_()
    # sys.exit(APP.exec_())  # выход
    my_messenger_client.exit_messsage()
