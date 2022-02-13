"""
Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2. Но в данном случае
результат должен быть итоговым по всем ip-адресам, представленным в табличном формате (использовать модуль tabulate).
Таблица должна состоять из двух колонок и выглядеть примерно так:

Reachable       Unreachable
-------------   -------------
10.0.0.1        10.0.0.3
10.0.0.2        10.0.0.4

"""
import tabulate

from Lesson1.task2 import host_range_ping


def host_range_ping_tab(start_ip, end_ip):
    """
    выводит таблицу с доступными и недоступными ip
    :param start_ip: первый ip диапазона
    :param end_ip: последний ip диапазона (включительно)
    :return: -
    """
    print(tabulate.tabulate(host_range_ping(start_ip, end_ip), headers='keys'))

if __name__ == "__main__":
    host_range_ping_tab('192.168.0.1', '192.168.0.6')