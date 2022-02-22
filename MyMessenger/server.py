import select
import sys
from threading import Thread

from arg_parser import ArgParser
from descriptor import ServerPort, ServerHost
from jim import JIMServer
from metaclasses import ServerVerifier
from my_socket import MessengerSocket
from log.server_log_config import server_logger
from decorators import log
from storage import MessengerStorage


@log
class MessengerServer(MessengerSocket, JIMServer, ArgParser, metaclass=ServerVerifier):
    # используем дескриптер ServerPort ServerHost, чтобы проверять номер порта и адрес
    port = ServerPort()
    address = ServerHost()

    def __init__(self, size=1024, encoding='utf-8', max_connections=5):
        self.address = self.get_address()
        self.port = self.get_port()
        self.max_connections = max_connections
        # список сообщений для клиентов
        self.message_list = []
        # список пользователей
        self.client_list = []
        # адресная книга (словарь ник:сокет)
        self.adress_book = {}
        # списки для select
        self.recv_data_list = []
        self.send_data_list = []
        self.errors_list = []
        # база данных
        self.database = MessengerStorage()

        self.user_commands_thread = Thread(target=self.user_commands)
        self.user_commands_thread.daemon = True

        # Thread.__init__(self)
        super().__init__(size, encoding)


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

            except:
                pass
            else:
                # добавляем клиента в список пользователей чата
                self.client_list.append(client)

                server_logger.info(
                    f'Сервер: получен запрос на соединение от клиента с адресом и портом: {client_address}')

            # обнуляем списки select'a перед каждой итерацией
            self.recv_data_list = []
            self.send_data_list = []
            self.errors_list = []

            try:
                # если есть ждущие клиенты - добавляем в список
                if self.client_list:
                    self.recv_data_list, self.send_data_list, self.errors_list = select.select(self.client_list,
                                                                                               self.client_list, [], 0)
            except OSError:
                pass

            # обрабатываем поступивших клиентов с сообщениями
            if self.recv_data_list:
                for client_with_message in self.recv_data_list:
                    try:
                        # пробуем ответить на precense сообщение или добавить входящее сообщение в список рассылки
                        self.answer(self.get_message(client_with_message), client_with_message)
                    except:
                        # если в сообщении ошибка - исключаем клиента из списка входящих
                        self.client_list.remove(client_with_message)

            # рассылаем сообщения, если они есть и если есть кому рассылать
            if self.message_list and self.send_data_list:
                print('это список сообщений', self.message_list)
                print('это адресаты', self.client_list)
                # создаем сообщение для отправки согласно jim протоколй
                message = self.jim_create_message(
                    'message',
                    self.message_list[0][0],
                    self.message_list[0][1]
                )
                to_user = self.message_list[0][2]
                # удаляем сообщение из списка входящих на сервер
                del self.message_list[0]
                # отправляем необходимому клиенту (берем сокет из адресной книги)
                try:
                    self.send_message(message, self.adress_book.get(to_user))
                except Exception as e:
                    print(e)


    def answer(self, received_message, client):
        server_logger.info(received_message)

        if self.get_jim_time() and self.get_jim_action() and self.get_jim_user() in received_message:
            # обработка precense сообщения
            if received_message[self.get_jim_action()] == 'presence':
                self.send_message(self.jim_create_server_response(200), client)
                # получаем username из сообщения
                new_username = received_message[self.get_jim_user()]
                # добавляем его в адресную книгу
                self.adress_book[new_username] = client
                # добавляем клиента в бд
                self.database.login(new_username, client.getpeername()[0], client.getpeername()[1])
                return
            # обработка сообщения от клиента
            elif received_message[self.get_jim_action()] == 'message':
                from_user = received_message[self.get_jim_user()]
                to_user = received_message[self.get_jim_to_user()]
                self.message_list.append((
                    from_user,
                    received_message[self.get_jim_data()],
                    to_user

                ))
                server_logger.info(self.message_list)

                # добавляем в список контактов в бд
                self.database.add_contact(from_user, to_user)
                return
            if received_message[self.get_jim_action()] == 'exit':
                logout_user = received_message[self.get_jim_user()]
                # удаляем клиента в из списка онлайн из бд
                self.database.logout(logout_user)
                server_logger.info(f'{logout_user} отключился от сервера')
                return
            if received_message[self.get_jim_action()] == 'contacts':
                from_user = received_message[self.get_jim_user()]
                to_user = from_user
                self.message_list.append((
                    'server',
                    str(self.database.get_contacts_list(from_user)),
                    to_user

                ))
                server_logger.info(self.message_list)
                return
            # обработка неправильных сообщений
            else:
                return self.jim_create_server_response(400)
        # обработка неправильных сообщений
        else:
            return self.jim_create_server_response(400)

    def user_commands(self):
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
                        f'Пользователь {user[0]}, подключен: {user[1]}:{user[2]}, время установки соединения: {user[3]}')
            elif command == 'loglist':
                for user in sorted(self.database.get_login_history_list()):
                    print(f'Пользователь: {user[0]} время входа: {user[1]}. Вход с: {user[2]}:{user[3]}')
            else:
                print('Команда не распознана.')


if __name__ == "__main__":
    my_messenger_server = MessengerServer()
    # my_messenger_server.daemon = True
    my_messenger_server.start()


