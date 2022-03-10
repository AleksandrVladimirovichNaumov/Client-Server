import json
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

from metaclasses import ServerVerifier


class MessengerSocket():

    def __init__(self, size, encoding):
        self.size = size
        self.encoding = encoding
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def get_message(self, client):
        """
        получаем и декодируем ответ
        :param response: ответ от версера
        :return: словарь с сообщением
        """
        try:
            response = client.recv(self.size)
            if isinstance(response, bytes):
                json_response = json.loads(response.decode(self.encoding))
                if isinstance(json_response, dict):
                    return json_response
                raise ValueError
            raise ValueError
        except Exception as e:
            # print(f'Ошибка получения сообщения: {e}')
            return e

    def send_message(self, message, client):
        """
        кодируем и отправляем сообщение
        :param message: сообщение для отправки ввиде словаря
        :return: отправляем сообщение в байтах
        """
        try:
            if isinstance(message, dict):
                bytes_message = json.dumps(message).encode(self.encoding)
                client.send(bytes_message)
                # print(f'сообщение отправлено получателю {client}')
        except Exception as e:
            print(f'Ошибка отправки сообщения: {e}')
