import argparse
import sys


class ArgParser():
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-p', default=7777, type=int, nargs='?')
        self.parser.add_argument('-a', default='127.0.0.1', nargs='?')
        self.parser.add_argument('-m', default='reader', nargs='?')
        self.parser.add_argument('-u', default='Guest', nargs='?')
        namespace = self.parser.parse_args(sys.argv[1:])
        self.address = namespace.a
        self.port = namespace.p
        self.mode = namespace.m
        self.username = namespace.u

    def get_address(self):
        return ArgParser().address

    def get_port(self):
        return ArgParser().port

    def get_mode(self):
        return  ArgParser().mode

    def get_username(self):
        return  ArgParser().username