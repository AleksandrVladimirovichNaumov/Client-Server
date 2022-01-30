import json
import socket
import sys

from decorators import log
from jim import JIMClient
from my_socket import MessengerSocket
from log.client_log_config import client_logger


@log
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
            client_logger.info(f'отправлено precense сообщение на сервер [{self.address}:{self.port}]')
            server_answer = self.sock.recv(1024)
            client_logger.info(
                f'получено сообщение от сервера [{self.address}:{self.port}]: {self.response_meaning(server_answer)}')
        except Exception as e:
            client_logger.error(f'ошибка отправки presence сообщения: {e}')
        finally:
            self.sock.close()

    def presence(self):
        """
        первичный запрос на подключение к серверу
        :param name: пользователь
        :return: -
        """
        self.send_message(self.server_request('presence', self.username), self.sock)

    def response_meaning(self, response):
        dict_response = json.loads(response.decode())
        return f'ответ сервера {dict_response.get("response")} ({self.get_jim_responses().get(dict_response.get("response"))})'


if __name__ == "__main__":
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = False
        server_port = False
    except ValueError:
        client_logger.critical('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    except IndexError:
        client_logger.critical('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    if server_address:
        if server_port:
            my_messenger_client = MyMessengerClient(address=server_address, port=server_port)
        else:
            my_messenger_client = MyMessengerClient(address=server_address)
    else:
        if server_port:
            my_messenger_client = MyMessengerClient(port=server_port)
        else:
            my_messenger_client = MyMessengerClient()
    my_messenger_client.start()
