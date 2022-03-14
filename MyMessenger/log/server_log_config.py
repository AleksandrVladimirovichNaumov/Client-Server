"""module for server logger"""
import os
import sys
from logging import handlers
import logging

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'server.log')
server_format = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

#поток для логов
steam_handler_server = logging.StreamHandler(sys.stderr)
steam_handler_server.setFormatter(server_format)
steam_handler_server.setLevel(logging.DEBUG)
server_logs = handlers.TimedRotatingFileHandler(path, encoding='UTF-8', interval=1, when='D')
server_logs.setFormatter(server_format)

#логгер
server_logger = logging.getLogger('server_logger')
server_logger.setLevel(logging.DEBUG)
server_logger.addHandler(server_logs)
server_logger.addHandler(steam_handler_server)
