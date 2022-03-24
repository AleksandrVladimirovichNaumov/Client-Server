"""main server_files module"""
import binascii
import hmac
import os
import select
import sys
import threading
from threading import Thread

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

from common.arg_parser import ArgParser
from common.descriptor import ServerPort, ServerHost
from common.jim import JIMServer
from common.metaclasses import ServerVerifier
from common.my_socket import MessengerSocket
from log.server_log_config import server_logger
from common.decorators import Log
from server_files.server_gui import AdminConsole
from server_files.server_settings import SERVER_MAX_CONNECTIONS
from server_files.storage import MessengerStorage

conflag_lock = threading.Lock()


@Log
class MessengerServer(MessengerSocket, JIMServer, ArgParser, metaclass=ServerVerifier):
    """server_files"""
    # используем дескриптер ServerPort ServerHost, чтобы проверять номер порта и адрес
    port = ServerPort()
    address = ServerHost()

    def __init__(self, size=1024, encoding='utf-8', max_connections=SERVER_MAX_CONNECTIONS):
        self.address = self.get_address()
        self.port = self.get_port()
        self.max_connections = max_connections
        # список сообщений для клиентов
        message_list = []
        # список пользователей
        client_list = []
        # адресная книга (словарь ник:сокет)
        self.adress_book = {}
        # списки для select
        recv_data_list = []
        send_data_list = []
        errors_list = []
        self.dict_of_lists = {
            'message_list': message_list,
            'client_list': client_list,
            'recv_data_list': recv_data_list,
            'send_data_list': send_data_list,
            'errors_list': errors_list
        }
        # база данных
        self.database = MessengerStorage()
        # поток обработки команд пользователя
        self.user_commands_thread = Thread(target=self.user_commands)
        self.user_commands_thread.daemon = True
        # поток работы сервера
        self.server_thread = Thread(target=self.start)
        self.server_thread.daemon = True

        super().__init__(size, encoding)

    def turn_on(self):
        """
        start server_files main thread
        """
        self.server_thread.start()

    def start(self):
        """
        запуск сервера
        :return: -
        """
        # подготовка сокета
        self.sock.bind((self.address, self.port))
        self.sock.settimeout(0.5)
        self.sock.listen(self.max_connections)
        server_logger.info(f'Сервер {self.address}:{self.port} запущен')
        self.user_commands_thread.start()

        # Работa сервера в цикле
        while True:
            try:
                # пробуем подключить клиента
                client, client_address = self.sock.accept()

            except Exception:
                pass
            else:
                # добавляем клиента в список пользователей чата
                self.dict_of_lists['client_list'].append(client)

                server_logger.info(
                    'Сервер: получен запрос на соединение от'
                    f' клиента с адресом и портом: {client_address}')

            # обнуляем списки select'a перед каждой итерацией
            self.dict_of_lists['recv_data_list'] = []
            self.dict_of_lists['send_data_list'] = []
            self.dict_of_lists['errors_list'] = []

            try:
                # если есть ждущие клиенты - добавляем в список
                if self.dict_of_lists['client_list']:
                    self.dict_of_lists['recv_data_list'], \
                    self.dict_of_lists['send_data_list'], \
                    self.dict_of_lists['errors_list'] = select.select(self.dict_of_lists['client_list'],
                                                     self.dict_of_lists['client_list'],
                                                     [],
                                                     0)
            except Exception as exception:
                print(exception)

            # обрабатываем поступивших клиентов с сообщениями
            if self.dict_of_lists['recv_data_list']:
                for client_with_message in self.dict_of_lists['recv_data_list']:
                    try:
                        # пробуем ответить на precense сообщение или
                        # добавить входящее сообщение в список рассылки
                        self.answer(self.get_message(client_with_message), client_with_message)
                    except Exception as exception:
                        print(exception)
                        # если в сообщении ошибка - исключаем клиента из списка входящих
                        self.dict_of_lists['client_list'].remove(client_with_message)

            # рассылаем сообщения, если они есть и если есть кому рассылать
            if self.dict_of_lists['message_list'] and self.dict_of_lists['send_data_list']:
                print('это список сообщений', self.dict_of_lists['message_list'])
                print('это адресаты', self.dict_of_lists['client_list'])
                # создаем сообщение для отправки согласно jim протоколй
                message = self.jim_create_message(
                    'message',
                    self.dict_of_lists['message_list'][0][0],
                    self.dict_of_lists['message_list'][0][1]
                )
                to_user = self.dict_of_lists['message_list'][0][2]
                # удаляем сообщение из списка входящих на сервер
                del self.dict_of_lists['message_list'][0]
                # отправляем необходимому клиенту (берем сокет из адресной книги)
                try:
                    self.send_message(message, self.adress_book.get(to_user))
                except Exception as exception:
                    print(exception)

    def answer(self, received_message, client):
        """
        create answer from server_files
        """
        server_logger.info(received_message)

        if self.get_jim_time() and self.get_jim_action() \
                and self.get_jim_user() in received_message:

            # обработка precense сообщения
            if received_message[self.get_jim_action()] == 'presence':
                # getting username from message
                new_username = received_message[self.get_jim_user()]

                # if there is no such user - register new user
                if new_username not in self.database.get_only_usernames():
                    try:
                        # getting password from message
                        new_password = \
                            received_message[self.get_jim_data()]['password'].encode('utf-8')
                        self.database.login(new_username,
                                            client.getpeername()[0],
                                            client.getpeername()[1],
                                            new_password)
                    except Exception as exception:
                        server_logger.debug(exception)

                random_str = binascii.hexlify(os.urandom(64))

                hash = hmac.new(self.database.get_password(new_username),
                                random_str,
                                'MD5')
                digest = hash.digest()
                try:
                    self.send_message(self.jim_create_server_response(205,
                                                                      random_str.decode('ascii')),
                                      client)
                    answer = self.get_message(client)
                except Exception as exception:

                    server_logger.debug(exception)

                    return
                client_digest = binascii.a2b_base64(answer['data']['public_key'])
                if hmac.compare_digest(client_digest, digest):
                    try:
                        self.send_message(self.jim_create_server_response(200, 'OK'), client)
                    except Exception as exception:

                        server_logger.debug(exception)
                        return
                    # добавляем его в адресную книгу
                    self.adress_book[new_username] = client
                    # добавляем клиента в бд
                    self.database.login(new_username,
                                        client.getpeername()[0],
                                        client.getpeername()[1],
                                        answer['data']['password'],
                                        answer['data']['public_key']
                                        )
                    return
                else:
                    try:
                        self.send_message(self.jim_create_server_response(402, 'bad password'),
                                          client)

                    except Exception:


                        return

            # обработка сообщения от клиента
            elif received_message[self.get_jim_action()] == 'message':
                from_user = received_message[self.get_jim_user()]
                to_user = received_message[self.get_jim_to_user()]
                self.dict_of_lists['message_list'].append((
                    from_user,
                    received_message[self.get_jim_data()],
                    to_user

                ))
                server_logger.info(self.dict_of_lists['message_list'])

                # добавляем в список контактов в бд
                # self.database.add_contact(from_user, to_user)
                return
            # обработка сообщения о выходе клиента
            elif received_message[self.get_jim_action()] == 'exit':
                logout_user = received_message[self.get_jim_user()]
                # удаляем клиента в из списка онлайн из бд
                self.database.logout(logout_user)
                server_logger.info(f'{logout_user} отключился от сервера')
                return
            # обработка сообщения о запросе списка контактов
            elif received_message[self.get_jim_action()] == 'contacts':
                from_user = received_message[self.get_jim_user()]
                # подготавливаем список контактов
                contact_list = self.database.get_contacts_list(from_user)
                # отправляем список контактов
                self.send_message(self.jim_create_server_response(202, contact_list), client)
                server_logger.info(f'Список контактов был отправлен пользователю {from_user}')
                return
            # обработка сообщения об удалении контакта
            elif received_message[self.get_jim_action()] == 'delete':
                from_user = received_message[self.get_jim_user()]
                contact = received_message[self.get_jim_data()]
                result = f'Контакт {contact} был удален из списка пользователя {from_user}'
                # подготавливаем список контактов
                self.database.delete_contact(from_user, contact)
                # отправляем список контактов
                self.send_message(self.jim_create_server_response(203, result), client)
                server_logger.info(result)
                return
            # обработка сообщения об добавлении контакта
            elif received_message[self.get_jim_action()] == 'add':
                from_user = received_message[self.get_jim_user()]
                contact = received_message[self.get_jim_data()]
                result = f'Контакт {contact} был добавлен в список пользователя {from_user}'
                # добавляем контакт
                self.database.add_contact(from_user, contact)
                # отправляем список контактов
                self.send_message(self.jim_create_server_response(204, result), client)
                server_logger.info(result)
                return
            # обработка неправильных сообщений
            else:
                return self.jim_create_server_response(400)
        # обработка неправильных сообщений
        else:
            return self.jim_create_server_response(400)

    def user_commands(self):
        """
        terminal commands service
        """
        while True:
            command = input('Введите команду: ')
            if command == 'help':
                print('Поддерживаемые команды:')
                print('users - список известных пользователей')
                print('connected - список подключенных пользователей')
                print('loglist - история входов пользователя')

                print('help - вывод справки по поддерживаемым командам')

            elif command == 'users':
                for user in sorted(self.database.get_user_list()):
                    print(f'Пользователь {user[0]}, последний вход: {user[1]}')
            elif command == 'connected':
                for user in sorted(self.database.get_online_user_list()):
                    print(
                        f'Пользователь {user[0]}, подключен: {user[1]}:{user[2]}, '
                        f'время установки соединения: {user[3]}')
            elif command == 'loglist':
                for user in sorted(self.database.get_login_history_list()):
                    print(f'Пользователь: {user[0]} время входа: {user[1]}. '
                          f'Вход с: {user[2]}:{user[3]}')
            else:
                print('Команда не распознана.')


if __name__ == "__main__":
    # запуск сервака
    my_messenger_server = MessengerServer()
    my_messenger_server.turn_on()

    APP = QApplication(sys.argv)  # создание нашего приложение
    WINDOW_OBJ = AdminConsole()  # создаем объект


    def data_load():
        """
        то, что будет обновлять по таймеру
        :return: -
        """
        # загружаем таблицу с пользователями
        WINDOW_OBJ.tableView.setModel(WINDOW_OBJ.users_list(my_messenger_server.database))
        WINDOW_OBJ.tableView.resizeColumnsToContents()
        WINDOW_OBJ.tableView.resizeRowsToContents()
        # загружаем таблицу с историей подключений
        WINDOW_OBJ.tableView_2.setModel(WINDOW_OBJ.login_history_list(my_messenger_server.database))
        WINDOW_OBJ.tableView_2.resizeColumnsToContents()
        WINDOW_OBJ.tableView_2.resizeRowsToContents()
        # загружаем логи
        WINDOW_OBJ.listView.setModel(WINDOW_OBJ.logs_list())


    # загружаем ip
    WINDOW_OBJ.lineEdit.setText(my_messenger_server.address)
    # загружаем порт
    WINDOW_OBJ.lineEdit_2.setText(str(my_messenger_server.port))
    # загружаем максимум подключений к серверу
    WINDOW_OBJ.lineEdit_3.setText(str(my_messenger_server.max_connections))
    WINDOW_OBJ.show()  # показываем наше окно

    # Таймер, обновляющий список клиентов 1 раз в секунду
    timer = QTimer()
    timer.timeout.connect(data_load)
    timer.start(1000)

    sys.exit(APP.exec_())  # выход
