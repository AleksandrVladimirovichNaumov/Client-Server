import json
import socket
import sys
from time import sleep

from arg_parser import ArgParser
from decorators import log
from jim import JIMClient
from my_socket import MessengerSocket
from log.client_log_config import client_logger


@log
class MyMessengerClient(MessengerSocket, JIMClient, ArgParser):
    def __init__(self, size=1024, encoding='utf-8', username='Guest'):
        super().__init__(size, encoding)
        self.username = self.get_username()
        self.address = self.get_address()
        self.port = self.get_port()
        self.mode = self.get_mode()
        # пользователь может быть или отправитель или получатель (упращенный функционал)
        self.type = type

    def start(self):
        """
        запускаем клиента: пробуем подключится и отправить presence сообщение, далее работаем согласно типу клиента
        :return: -
        """
        try:
            # отправка precence и получение ок ответа от сервера
            self.sock.connect((self.address, self.port))
            client_logger.info(f'произошло подключение к серверу [{self.address}:{self.port}]')
            self.presence()
            server_answer = self.sock.recv(self.size)
            client_logger.info(
                f'получено сообщение от сервера [{self.address}:{self.port}]: {self.response_meaning(server_answer)}')

        except Exception as e:
            client_logger.error(f'ошибка отправки presence сообщения: {e}')
        else:
            # основной цикл
            while True:
                # если пользователь читатель
                if self.mode == 'reader':
                    try:
                        # выводим сообщение на экран
                        print(self.message_meaning(self.get_message(self.sock)))
                    except:
                        pass
                # если пользователь отправитель
                elif self.mode == 'sender':
                    # ждем сообщение для отправки
                    message = input('введите сообщение для рассылки или q для выхода: ')
                    # q - выход, остальное отправляем
                    if message == 'q':
                        break
                    else:
                        self.message(message)

        finally:
            self.sock.close()
            sys.exit(0)

    def presence(self):
        """
        первичный запрос на подключение к серверу
        :return: -
        """
        self.send_message(self.jim_create_message('presence', self.username), self.sock)
        client_logger.info(f'отправлено precense сообщение от {self.username}')

    def message(self, message):
        """
        рассылка сообщений
        :param message: сообщение для отправки
        :return: -
        """
        self.send_message(self.jim_create_message('message', self.username, message), self.sock)
        client_logger.info(f'отправлено message сообщение от {self.username}')

    def response_meaning(self, response):
        """
        расшифровка ответа сервера
        :param response:
        :return:
        """
        dict_response = json.loads(response.decode())
        return f'ответ сервера {dict_response.get("response")} ({self.get_jim_responses().get(dict_response.get("response"))})'

    def message_meaning(self, message):
        """
        расшифровка сообщения от клиента
        :param response:
        :return:
        """
        return f'сообщение от  {message[self.get_jim_user()]} [{message[self.get_jim_time()]}]: {message[self.get_jim_data()]}'


if __name__ == "__main__":
    # try:
    #     server_address = sys.argv[1]
    #     server_port = int(sys.argv[2])
    #     type = sys.argv[3]
    #     if server_port < 1024 or server_port > 65535:
    #         raise ValueError
    # except IndexError:
    #     server_address = False
    #     server_port = False
    # except ValueError:
    #     client_logger.critical('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
    #     sys.exit(1)
    #
    # except IndexError:
    #     client_logger.critical('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
    #     sys.exit(1)
    #
    # if server_address:
    #     if server_port:
    #         my_messenger_client = MyMessengerClient(address=server_address, port=server_port)
    #     else:
    #         my_messenger_client = MyMessengerClient(address=server_address)
    # else:
    #     if server_port:
    #         my_messenger_client = MyMessengerClient(port=server_port)
    #     else:
    #         my_messenger_client = MyMessengerClient()

    my_messenger_client = MyMessengerClient()
    my_messenger_client.start()
