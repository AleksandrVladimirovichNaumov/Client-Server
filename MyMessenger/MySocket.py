from socket import socket, AF_INET, SOCK_STREAM


class MessengerSocket():

    def __init__(self, address, port):
        self.address = address
        self.port = port

        self.sock = socket(AF_INET, SOCK_STREAM)
