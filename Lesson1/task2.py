"""
Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона. Меняться должен только последний
октет каждого адреса. По результатам проверки должно выводиться соответствующее сообщение.
"""
from Lesson1.task1 import host_ping


def host_range_ping(start_ip, end_ip):
    """
    проверяет доступность ip из указанного диапазона
    :param start_ip: первый ip диапазона
    :param end_ip: последний ip диапазона (включительно)
    :return: словарь, какие ip доступны, а какие нет
    """
    #выделяем константную частьip адреса
    try:
        constant_part1 = start_ip[:start_ip.rfind('.')+1]
        constant_part2 = end_ip[:start_ip.rfind('.')+1]
    except Exception as e:
        return e
    # проверяем, правильно ли указаны ip (первые три октета должны быть одинаковые)
    if constant_part1 != constant_part2:
        return 'первые три октета должны быть одинаковые'
    # получаем начало и конец диапазона
    start_of_range = int(start_ip[start_ip.rfind('.') +1:])
    end_of_range = int(end_ip[start_ip.rfind('.') + 1:])
    # создаем список ip адресов
    list_of_ip = [f'{constant_part1}{x}' for x in range(start_of_range, end_of_range+1)]
    return host_ping(list_of_ip)

if __name__ == '__main__':
    print(host_range_ping('192.168.0.1', '192.167.0.6'))
    print(host_range_ping('192.168.0.1', '192.168.0.6'))