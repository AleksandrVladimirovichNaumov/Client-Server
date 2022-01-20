import socket

from MySocket import MessengerSocket


class MyMessengerClient(MessengerSocket):
    def __init__(self, address, port):
        super().__init__(address, port)

    def start(self):
        try:
            while True:
                # коннектимся с сервером
                self.sock=socket.socket()
                self.sock.connect((self.address, self.port))
                # попробуйте уменьшить размер пакета и передать длинное сообщение
                # аргумент устанавливает максимальное количество байтов в сообщении.
                #  Если столько байт, сколько указано, не пришло, а
                #  какие-то данные уже появились, она всё равно возвращает всё, что имеется
                TIME_BYTES = self.sock.recv(1024)

                print(f"Клиент: текущее время: {TIME_BYTES.decode('utf-8')}")
        except Exception as e:
            print(f'client error {e}')

        finally:
            self.sock.close()


if __name__ == "__main__":
    my_messenger_client = MyMessengerClient('localhost', 8888)
    my_messenger_client.start()
