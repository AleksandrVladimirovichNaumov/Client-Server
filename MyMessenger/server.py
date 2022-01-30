import sys
import time

from jim import JIMServer
from my_socket import MessengerSocket
from log.server_log_config import server_logger
from decorators import log


@log
class MessengerServer(MessengerSocket, JIMServer):
    def __init__(self, address='127.0.0.1', port=7777, size=1024, encoding='utf-8', max_connections=5):
        self.max_connections = max_connections
        super().__init__(address, port, size, encoding)

    def start(self):
        """
        запуск сервера
        :return: -
        """
        self.sock.bind((self.address, self.port))
        self.sock.listen(self.max_connections)
        server_logger.info(f'Сервер {self.address}: {self.port} запущен')
        try:
            while True:
                client, client_address = self.sock.accept()
                server_logger.info(
                    f'Сервер: получен запрос на соединение от клиента с адресом и портом: {client_address}')
                self.send_message(self.answer(self.get_message(client)), client)
                client.close()
        except Exception as e:
            server_logger.error(f'ошибка сервера {e}')
        finally:
            self.sock.close()

    def answer(self, received_message):
        server_logger.info(received_message)
        if self.get_jim_time() and self.get_jim_action() and self.get_jim_user() in received_message:
            if received_message.get(self.get_jim_action()) == 'presence' and received_message.get(
                    self.get_jim_user()) == 'Guest':
                return self.server_response(200)
            else:
                return self.server_response(400)
        else:
            return self.server_response(400)


if __name__ == "__main__":
    # проверяем параметры
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
            if listen_port < 1024 or listen_port > 65535:
                raise ValueError
        else:
            listen_port = False

    except IndexError:
        server_logger.error('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        server_logger.error('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = False

    except IndexError:
        server_logger.error('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)
    # запускаем согласно параметрам
    if listen_port:
        if listen_address:
            my_messenger_server = MessengerServer(port=listen_port, address=listen_address)
        else:
            my_messenger_server = MessengerServer(port=listen_port)
    else:
        if listen_address:
            my_messenger_server = MessengerServer(address=listen_address)
        else:
            my_messenger_server = MessengerServer()

    my_messenger_server.start()
