import logging
import os.path
import sys

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'client.log')
client_format = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

#поток для логов
steam_handler = logging.StreamHandler(sys.stderr)
steam_handler.setFormatter(client_format)
steam_handler.setLevel(logging.INFO)
client_logs = logging.FileHandler(path, encoding='UTF-8')
client_logs.setFormatter(client_format)

#логгер
client_logger = logging.getLogger('client_logger')
client_logger.setLevel(logging.INFO)
client_logger.addHandler(client_logs)
client_logger.addHandler(steam_handler)


