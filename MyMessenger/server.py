import select
import sys


from arg_parser import ArgParser
from descriptor import ServerPort, ServerHost
from jim import JIMServer
from my_socket import MessengerSocket
from log.server_log_config import server_logger
from decorators import log


@log
class MessengerServer(MessengerSocket, JIMServer, ArgParser):
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
                print('это список сообщений',self.message_list)
                print('это адресаты',self.client_list)
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
                # добавляем его в адресную книгу
                self.adress_book[received_message[self.get_jim_user()]]=client
                return
            # обработка сообщения от клиента
            elif received_message[self.get_jim_action()] == 'message':
                self.message_list.append((
                    received_message[self.get_jim_user()],
                    received_message[self.get_jim_data()],
                    received_message[self.get_jim_to_user()]

                ))
                server_logger.info(self.message_list)
                return
            # обработка неправильных сообщений
            else:
                return self.jim_create_server_response(400)
        # обработка неправильных сообщений
        else:
            return self.jim_create_server_response(400)


if __name__ == "__main__":
    my_messenger_server = MessengerServer()
    my_messenger_server.start()

