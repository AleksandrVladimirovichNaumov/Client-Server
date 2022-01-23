import json
import socket

from JIM import JIMClient
from MySocket import MessengerSocket


class MyMessengerClient(MessengerSocket, JIMClient):
    def __init__(self, address='127.0.0.1', port=7777, size=1024, encoding='utf-8', username='Guest'):
        super().__init__(address, port, size, encoding)
        self.username = username

    def start(self):
        """
        запускаем клиента: пробуем подключится и отправить presence сообщение
        :return: -
        """
        try:
            self.sock.connect((self.address, self.port))
            self.presence()
            server_answer = self.sock.recv(1024)
            print(server_answer)
        except Exception as e:
            print(f'ошибка отправки presence сообщения: {e}')
        finally:
            self.sock.close()

    def presence(self):
        """
        первичный запрос на подключение к серверу
        :param name: пользователь
        :return: -
        """
        self.send_message(self.server_request('presence', self.username), self.sock)


if __name__ == "__main__":
    my_messenger_client = MyMessengerClient()
    my_messenger_client.start()
