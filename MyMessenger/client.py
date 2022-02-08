import json
import socket
import sys
import time
from threading import Thread
from time import sleep

from arg_parser import ArgParser
from decorators import log
from jim import JIMClient
from my_socket import MessengerSocket
from log.client_log_config import client_logger


@log
class MyMessengerClient(MessengerSocket, JIMClient, ArgParser):
    def __init__(self, size=1024, encoding='utf-8'):
        super().__init__(size, encoding)
        self.username = self.get_username()
        self.address = self.get_address()
        self.port = self.get_port()
        self.mode = self.get_mode()
        # пользователь может быть или отправитель или получатель (упращенный функционал)
        self.type = type
        # поток для получения сообщений
        self.receiver_thread = Thread(target=self.message_meaning)
        self.receiver_thread.daemon = True
        # поток для отправки сообщений
        self.sender_thread = Thread(target=self.message)
        self.sender_thread.daemon = True


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
            # запускаем потоки на прием и отправку сообщений
            time.sleep(1)
            self.receiver_thread.start()

            self.sender_thread.start()
            # основной цикл
            while True:
                time.sleep(1)
                if self.sender_thread.is_alive() and self.receiver_thread.is_alive():
                    continue
                break
                # # если пользователь читатель
                # if self.mode == 'reader':
                #     try:
                #         # выводим сообщение на экран
                #         print(self.message_meaning(self.get_message(self.sock)))
                #     except:
                #         pass
                # # если пользователь отправитель
                # elif self.mode == 'sender':
                #     # ждем сообщение для отправки
                #     message = input('введите сообщение для рассылки или q для выхода: ')
                #     # q - выход, остальное отправляем
                #     if message == 'q':
                #         break
                #     else:
                #         self.message(message, 'guest')

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

    def message(self):
        """
        отправка сообщения

        :return: -
        """
        while True:
            to_user = input('кому отправить сообщение (q - выйти): ')
            if to_user.lower() == 'q':
                break
            else:
                message = input('введите сообщение: ')
                self.send_message(self.jim_create_message('message', self.username, message, to_user), self.sock)
                client_logger.debug(f'отправлено message сообщение от {self.username}')

    def response_meaning(self, response):
        """
        расшифровка ответа сервера
        :param response:
        :return:
        """
        dict_response = json.loads(response.decode())
        return f'ответ сервера {dict_response.get("response")} ({self.get_jim_responses().get(dict_response.get("response"))})'

    def message_meaning(self):
        """
        расшифровка сообщения от клиента
        :param response:
        :return:
        """
        while True:
            try:
                message = self.get_message(self.sock)
                print(f'\n сообщение от  {message[self.get_jim_user()]} [{message[self.get_jim_time()]}]: {message[self.get_jim_data()]}')
            except:
                pass


if __name__ == "__main__":

    my_messenger_client = MyMessengerClient()
    my_messenger_client.start()
