"""
Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
 («Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции
 ip_address().
"""
import ipaddress
import subprocess


def host_ping(list_to_ping):
    """
    возвращает словарь со списками пингующихся и не пингующихся адресов
    :param list_to_ping: список адресов для проверки
    :return: словарь, какие ip доступны, а какие нет
    """

    # словарь с результатами
    ping_result = {"Узел доступен": [], "Узел недоступен": []}
    # перебераем адреса
    for address in list_to_ping:
        try:
            # пробуем получить ip
            address = str(ipaddress.ip_address(address))
        except Exception as e:
            print(e)

        ping_process = subprocess.Popen(['ping', address, '-c 1'], stdout=subprocess.PIPE)
        # ждем завершения пинга

        ping_process.wait()
        print(ping_process)
        # добавляем в словарь результатов в зависимости от пинга
        if ping_process.returncode == 0:
            ping_result.get("Узел доступен").append(address)
        else:
            ping_result.get("Узел недоступен").append(address)
        ping_process.kill()
    return ping_result


if __name__ == '__main__':
    print(host_ping(['yandex.ru', '156.185.177.11', 'google.ru', '192.168.0.1', 'net-takogo-adresa.ru']))
