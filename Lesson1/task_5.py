"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""

import subprocess
import time

import chardet as chardet

address_list = ['yandex.ru', 'youtube.com']


def ping_target(address, sec):
    """
    ping web address for required time
    :param address: address to ping
    :param sec: time to ping in seconds
    :return: print result
    """
    ping_value = subprocess.Popen(['ping', address], stdout=subprocess.PIPE)
    time.sleep(sec)
    ping_value.kill()
    for line in ping_value.stdout:
        response = chardet.detect(line)
        print(line.decode(response['encoding']).encode('UTF-8').decode('UTF-8').replace('bytes from', 'байт(ов) от').
              replace('ms', 'мс').replace('bytes of data', 'байт(ов) данных').replace('PING', 'ПИНГ'))


for address in address_list:
    ping_target(address, 3)
