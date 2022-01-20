import time
from MySocket import MessengerSocket


class MessengerServer(MessengerSocket):
    def __init__(self,address, port,max_connections):
        self.max_connections = max_connections
        super().__init__(address, port)


    def start(self):
        self.sock.bind((self.address, self.port))
        self.sock.listen(self.max_connections)
        print('Сервер запущен')
        try:
            while True:
                CLIENT_SOCK, ADDR = self.sock.accept()
                print(f'Сервер: получен запрос на соединение от клиента с адресом и портом: {ADDR}')
                TIMESTR = time.ctime(time.time()) + "\n"
                # отправляем клиенту сообщение
                CLIENT_SOCK.send(TIMESTR.encode('utf-8'))
                CLIENT_SOCK.close()
        except Exception as e:
            print(f'server error {e}')
        finally:
            self.sock.close()

if __name__ == "__main__":
    my_messenger_server = MessengerServer('', 8888, 5)
    my_messenger_server.start()
