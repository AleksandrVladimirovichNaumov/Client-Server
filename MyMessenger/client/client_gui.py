"""Module for client GUI"""
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, qApp


class ClientGui(QWidget):
    '''
    class for gui client
    '''

    def __init__(self):
        super().__init__()
        # usage of loadUi()
        uic.loadUi('client/gui_client.ui', self)  # load client window
        # local database
        self.database = None

        self.client_obj = None
        # active contact
        self.active_contact = ''

        # client events processing
        self.actionExit.triggered.connect(qApp.quit)
        self.pushButton.clicked.connect(self.send_message)
        self.pushButton_2.clicked.connect(self.save_settings)
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
            except Exception:
                pass
        for contact in contacts_list:
            row = QStandardItem(contact)
            contact_list_result.appendRow(row)
        return contact_list_result

    def set_database(self, database):
        """
        set database object to work with it
        """
        self.database = database

    def set_client_obj(self, client_obj):
        """
        set client object to work with client.py
        """
        self.client_obj = client_obj
        self.lineEdit_2.setText(self.client_obj.username)

    def refresh_contact_list(self):
        """
        updating visible contacts in main window
        """
        contact_for_model = QStandardItemModel()
        for contact in self.database.get_contact_list():
            row = QStandardItem(contact)
            contact_for_model.appendRow(row)
        self.listView.setModel(contact_for_model)

    def add_contact(self):
        """
        adding contact to database local and server
        """
        new_contact = self.lineEdit_4.text()
        if new_contact != '':
            result = self.database.add_contact(new_contact)
            self.client_obj.client_send_message('add',
                                                self.client_obj.username,
                                                new_contact
                                                )
            if result:
                self.refresh_contact_list()

    def delete_contact(self):
        """
        deleting contact from database local and server
        """

        selected_contact = self.listView.currentIndex().data()
        result = self.database.delete_contact(selected_contact)
        self.client_obj.client_send_message('delete',
                                            self.client_obj.username,
                                            selected_contact
                                            )
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

    def save_settings(self):

        """
        save settings from settings tab
        сохраняем настройки с вкладки settings
        :return: -
        """

        username = self.lineEdit_2.text()

        with open("client_settings.py", 'w') as settings_file:
            settings_file.write(
                f"CLIENT_USERNAME = '{username}'"
            )


class ClientLoginGui(QtWidgets.QDialog):
    """
    class for login dialog
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # create contect of dialog
        self.spacer = QtWidgets.QLabel(' ')
        self.login_title = QtWidgets.QLabel('Username')
        self.text_name = QtWidgets.QLineEdit(self)
        self.password_title = QtWidgets.QLabel('Password')
        self.text_pass = QtWidgets.QLineEdit(self)
        self.button_login = QtWidgets.QPushButton('Login', self)
        self.button_login.clicked.connect(self.handle_login)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.login_title)
        layout.addWidget(self.text_name)
        layout.addWidget(self.password_title)
        layout.addWidget(self.text_pass)
        layout.addWidget(self.spacer)
        layout.addWidget(self.button_login)
        self.setWindowTitle('Registration / Authentication')
        self.setFixedWidth(400)

        # adding client_obj to work with client.py

        self.client_object = None

    def set_client_obj(self, client_obj):
        """
        set client object to work with client.py
        """
        self.client_object = client_obj

    def handle_login(self):
        """
        trying to login / create new account
        """
        server_response = self.client_object.login(
            self.text_name.text(),
            self.text_pass.text()
        )

        if server_response == 'OK':
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', server_response)
