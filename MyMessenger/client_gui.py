from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, qApp

from descriptor import ServerPort, ServerHost
from server_settings import SERVER_PORT, SERVER_MAX_CONNECTIONS, SERVER_IP


class ClientGui(QWidget):
    '''
    gui of client
    '''

    def __init__(self, parent=None):
        super().__init__()
        # usage of loadUi()
        uic.loadUi('gui_client.ui', self)  # load client window
        # local database
        self.database = None

        self.client_obj = None
        # active contact
        self.active_contact = ''

        # client events processing
        self.actionExit.triggered.connect(qApp.quit)
        self.pushButton.clicked.connect(self.send_message)
        # self.pushButton_2.clicked.connect(self.save_settings)
        self.pushButton_3.clicked.connect(self.add_contact)
        self.pushButton_4.clicked.connect(self.delete_contact)
        self.listView.doubleClicked.connect(self.refresh_messages_history)

    def contact_list(self):
        """
        make a contact list for a client
        :param database: local client db
        :return: list of clients
        """
        contact_list_result = QStandardItemModel()

        # проверяем онлайн или нет
        while True:
            try:
                contacts_list = self.database.get_contact_list()
                break
            except:
                pass
        for contact in contacts_list:
            row = QStandardItem(contact)
            contact_list_result.appendRow(row)
        return contact_list_result

    def set_database(self, database):
        self.database = database

    def set_client_obj(self, client_obj):
        self.client_obj = client_obj

    def refresh_contact_list(self):
        contact_for_model = QStandardItemModel()
        for contact in self.database.get_contact_list():
            row = QStandardItem(contact)
            contact_for_model.appendRow(row)
        self.listView.setModel(contact_for_model)

    def add_contact(self):
        """
        adding contact to database
        """
        new_contact = self.lineEdit_4.text()
        if new_contact != '':
            result = self.database.add_contact(new_contact)
            if result:
                self.refresh_contact_list()

    def delete_contact(self):
        """
        deleting contact from database
        """

        selected_contact = self.listView.currentIndex().data()
        result = self.database.delete_contact(selected_contact)
        if result:
            self.refresh_contact_list()

    def refresh_messages_history(self):
        """
        refresh message history in a chat
        """
        messages_for_model = QStandardItemModel()
        for message in self.database.get_messages_history(self.listView.currentIndex().data()):
            row = QStandardItem(message[0])
            if not message[1]:
                row.setTextAlignment(QtCore.Qt.AlignRight)
            messages_for_model.appendRow(row)
        self.listView_2.setModel(messages_for_model)
        self.listView_2.scrollToBottom()
        self.label_2.setText(f'Chat with:   {self.listView.currentIndex().data()}')
        self.active_contact = self.listView.currentIndex().data()

    def send_message(self):
        """
        send message to active contact
        """

        # checking that message is not empty
        if self.textEdit.toPlainText() != '' and self.active_contact != '':
            self.client_obj.client_send_message('message',
                                                self.textEdit.toPlainText(),
                                                self.active_contact)

            self.refresh_messages_history()
            self.textEdit.clear()


def login_history_list(self, database):
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


def logs_list(self):
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
    except Exception as e:
        row = QStandardItem(str(e))
        logs_listview.appendRow(row)
        return logs_listview


def save_settings(self):
    """
    сохраняем настройки с вкладки settings
    :return: -
    """

    try:
        self.address = self.lineEdit.text()
    except Exception as e:
        print(e)
        self.address = SERVER_IP
        self.lineEdit.setText(self.address)
    try:
        self.port = int(self.lineEdit_2.text())
    except Exception as e:
        print(e)
        self.port = SERVER_PORT
        self.lineEdit_2.setText(str(self.port))
    try:
        max_connections = int(self.lineEdit_3.text())
    except Exception as e:
        print(e)
        max_connections = SERVER_MAX_CONNECTIONS
        self.lineEdit_3.setText(str(max_connections))

    with open("server_settings.py", 'w') as settings_file:
        settings_file.write(
            f"SERVER_IP = '{self.address}' \nSERVER_PORT = {self.port} \nSERVER_MAX_CONNECTIONS = {max_connections}"
        )
