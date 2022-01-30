import logging
import sys


class log:
    def __init__(self, class_obj):
        # класс, который оборачивает декортор
        self.class_obj = class_obj
        # по умолчанию False, если вызван из неподдерживаемого модуля
        self.loger = False
        # из какого модуля вызван
        self.from_module = sys.argv[0]
        # определяем какой файл запускает декоратор для выбора логера
        if self.from_module == 'client.py':
            self.loger = logging.getLogger('client_logger')

        elif self.from_module == 'server.py':

            self.loger = logging.getLogger('server_logger')

        else:
            print(f'{self.from_module} не поддерживается декоратором @log')

    # декоратор обработывает каждый вызов класса
    def __call__(self, *args, **kwargs):

        if self.loger is not False:
            #   добавляем запись в логи

            self.loger.debug(f'Класс {self.class_obj.__name__} вызван из {self.from_module}')
        return self.class_obj(*args, **kwargs)
