"""module to parse arguments from terminal"""
import argparse
import sys

from MyMessenger.client.client_settings import CLIENT_USERNAME
from MyMessenger.server.server_settings import SERVER_PORT, SERVER_IP


class ArgParser():
    """
    main class for arguments parsing
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-p', default=SERVER_PORT, type=int, nargs='?')
        self.parser.add_argument('-a', default=SERVER_IP, nargs='?')
        self.parser.add_argument('-m', default='reader', nargs='?')
        self.parser.add_argument('-u', default=CLIENT_USERNAME, nargs='?')
        namespace = self.parser.parse_args(sys.argv[1:])
        self.address = namespace.a
        self.port = namespace.p
        self.mode = namespace.m
        self.username = namespace.u

    @staticmethod
    def get_address():
        """
        get arg of address
        """
        return ArgParser().address

    @staticmethod
    def get_port():
        """
        get arg of port
        """
        return ArgParser().port

    @staticmethod
    def get_mode():
        """
        get arg of mode
        """
        return ArgParser().mode

    @staticmethod
    def get_username():
        """
        get arg of username
        """
        return ArgParser().username
