"""module for server GUI"""
from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, qApp

from common.descriptor import ServerPort, ServerHost
from server_settings import SERVER_PORT, SERVER_MAX_CONNECTIONS, SERVER_IP


class AdminConsole(QWidget):
    '''
    класс графичееского иннтерфеса сервера
    '''

    # используем дескрипторы
    port = ServerPort()
    address = ServerHost()

    def __init__(self):
        super().__init__()
        # Использование функции loadUi()
        uic.loadUi('server/gui_server.ui', self)  # загружаем наше окно

        # Обрабокта события нажатия кнопки
        self.actionExit.triggered.connect(qApp.quit)
        self.pushButton.clicked.connect(self.save_settings)

    def users_list(self, database):
        """
        создает контент таблицы со всеми зарегистрированными пользователями
        :param database: база, с которой надо работать
        :param online: отображать всех или только онлайн
        :return: таблица пользователей
        """
        # создаем модель таблицы
        users_table = QStandardItemModel()

        # проверяем онлайн или нет
        if self.checkBox.isChecked():
            # обозначаем заголовки
            users_table.setHorizontalHeaderLabels(['Username', 'Last login', 'IP', 'Port'])
            # забираем userlist из бд безопасно, малоли бд занята
            while True:
                try:
                    user_list = database.get_online_user_list()
                    break
                except Exception:
                    pass
            # создаем ячейку из каждой строки
            for row in user_list:
                user, id, time, ip, port = row
                user = QStandardItem(user)  # создаем элемент
                user.setEditable(False)  # редактирование
                time = QStandardItem(str(time.replace(microsecond=0)))
                time.setEditable(False)
                ip = QStandardItem(ip)  # создаем элемент
                ip.setEditable(False)  # редактирование
                port = QStandardItem(str(port))  # создаем элемент
                port.setEditable(False)  # редактирование
                users_table.appendRow([user, time, ip, port])  # добавляем строку
        else:
            # обозначаем заголовки
            users_table.setHorizontalHeaderLabels(['Username', 'Last login'])
            # забираем userlist из бд безопасно, малоли бд занята
            while True:
                try:
                    user_list = database.get_user_list()
                    break
                except Exception:
                    pass
            # создаем ячейку из каждой строки
            for row in user_list:
                user, time = row
                user = QStandardItem(user)  # создаем элемент
                user.setEditable(False)  # редактирование
                time = QStandardItem(str(time.replace(microsecond=0)))
                time.setEditable(False)
                users_table.appendRow([user, time])  # добавляем строку
        return users_table
    @staticmethod
    def login_history_list(database):
        """
        создаем таблицу с историй подключения к серверу
        :param database: используемая база данных
        :return: таблицу с историей
        """
        login_history_list = database.get_login_history_list()
        login_history_table = QStandardItemModel()
        login_history_table.setHorizontalHeaderLabels(['Username', 'Last login', 'IP', "Port"])
        for row in login_history_list:
            user, id, time, ip, port = row
            user = QStandardItem(user)  # создаем элемент
            user.setEditable(False)  # редактирование
            ip = QStandardItem(ip)
            ip.setEditable(False)
            port = QStandardItem(str(port))
            port.setEditable(False)
            # Уберём милисекунды из строки времени, т.к. такая точность не требуется.
            time = QStandardItem(str(time.replace(microsecond=0)))
            time.setEditable(False)
            login_history_table.appendRow([user, time, ip, port])  # добавляем строку
        return login_history_table

    @staticmethod
    def logs_list():
        """
        передаем логи в listview
        :return: логи или ошибку
        """
        logs_listview = QStandardItemModel()
        # пробуем открыть файл с логами
        try:
            with open('log/server.log') as logs_file:
                # построчно заполняем логи в модель
                for line in logs_file:
                    row = QStandardItem(line)
                    logs_listview.appendRow(row)
                return logs_listview
        # если ошибка, то выводим ее вместо логов
        except Exception as exception:
            row = QStandardItem(str(exception))
            logs_listview.appendRow(row)
            return logs_listview

    def save_settings(self):
        """
        сохраняем настройки с вкладки settings
        :return: -
        """

        try:
            self.address = self.lineEdit.text()
        except Exception as exception:
            print(exception)
            self.address = SERVER_IP
            self.lineEdit.setText(self.address)
        try:
            self.port = int(self.lineEdit_2.text())
        except Exception as exception:
            print(exception)
            self.port = SERVER_PORT
            self.lineEdit_2.setText(str(self.port))
        try:
            max_connections = int(self.lineEdit_3.text())
        except Exception as exception:
            print(exception)
            max_connections = SERVER_MAX_CONNECTIONS
            self.lineEdit_3.setText(str(max_connections))

        with open("server_settings.py", 'w') as settings_file:
            settings_file.write(
                f"SERVER_IP = '{self.address}' \nSERVER_PORT = {self.port} "
                f"\nSERVER_MAX_CONNECTIONS = {max_connections}"
            )
