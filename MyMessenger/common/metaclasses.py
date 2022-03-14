"""metaclass module"""
import dis
import logging

server_logger = logging.getLogger('server_logger')
client_logger = logging.getLogger('client_logger')


class ServerVerifier(type):
    """main class for Server metaclass"""

    def __init__(self, class_name, base_classes, class_dict):
        # список методов класса
        methods = []
        # список атрибутов класса
        attrs = []

        for function in class_dict:
            try:
                ret = dis.get_instructions(class_dict[function])
            except TypeError:
                pass
            else:
                # добавляем аргументы и методы в списки основываясь на итераторе
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL' and i.opname not in methods:
                        methods.append(i.argval)
                    elif i.opname == 'LOAD_ATTR' and i.opname not in attrs:
                        attrs.append(i.argval)

        if 'connect' in methods:
            server_logger.critical('метод connect ошибочно используется при работе сервера')

        if 'sock' not in attrs:
            server_logger.critical('неверная инициализация сокета. необходимы sock')

        super().__init__(class_name, base_classes, class_dict)


class ClientVerifier(type):
    """main class for Client metaclass"""

    def __init__(self, class_name, base_classes, class_dict):
        # список методов класса
        methods = []
        # список атрибутов класса
        attrs = []

        for function in class_dict:
            try:
                ret = dis.get_instructions(class_dict[function])
            except TypeError:
                pass
            else:
                # добавляем аргументы и методы в списки основываясь на итераторе
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL' and i.opname not in methods:
                        methods.append(i.argval)
                    elif i.opname == 'LOAD_ATTR' and i.opname not in attrs:
                        attrs.append(i.argval)
                    # так как send_message & get_message являются
                    # методами родительского класса MySocket,
                    # то надо добавить LOAD_METHOD в список методов
                    elif i.opname == 'LOAD_METHOD' and i.opname not in methods:
                        methods.append(i.argval)

        if 'accept' in methods or 'listen' in methods or 'socket' in methods:
            client_logger.critical('методы accept / listen /'
                                   ' socket ошибочно используется при работе клиента')

        if 'send_message' not in methods or 'get_message' not in methods:
            client_logger.critical('необходимо использовать get_message и send_message для клиента')

        if 'sock' not in attrs:
            client_logger.critical('неверная инициализация сокета. необходимы sock')

        super().__init__(class_name, base_classes, class_dict)
