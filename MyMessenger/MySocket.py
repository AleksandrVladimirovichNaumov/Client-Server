import json
from socket import socket, AF_INET, SOCK_STREAM


class MessengerSocket():

    def __init__(self, address, port, size, encoding):
        self.address = address
        self.port = port
        self.size = size
        self.encoding = encoding
        self.sock = socket(AF_INET, SOCK_STREAM)

    def get_message(self, client):
        """
        получаем и декодируем ответ
        :param response: ответ от версера
        :return: словарь с сообщением
        """
        try:
            response = client.recv(self.size)
            if isinstance(response, bytes):
                json_response=json.loads(response.decode(self.encoding))
                if isinstance(json_response, dict):
                    return json_response
                raise ValueError
            raise ValueError
        except Exception as e:
            print(f'Ошибка получения сообщения: {e}')

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
            else:
                raise ValueError
        except Exception as e:
            print(f'Ошибка отправки сообщения: {e}')
