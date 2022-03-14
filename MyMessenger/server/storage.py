import datetime

from sqlalchemy import __version__, create_engine, Table, Column, MetaData, Integer,\
    String, DateTime, ForeignKey, UniqueConstraint, Text
from sqlalchemy.orm import mapper, sessionmaker


class MessengerStorage:
    print(f"Версия SQLAlchemy: {__version__}")

    class AllUsers:
        """
        класс для таблицы со всеми пользователями
        """

        def __init__(self, username, password, public_key):
            self.id = None
            self.username = username
            self.password = password
            self.public_key = public_key
            self.last_login = datetime.datetime.utcnow()

    class OnlineUsers():
        """
        класс для таблицы с онлайн пользователями.
        """

        def __init__(self, user_id, datetime, ip, port):
            self.user_id = user_id
            self.last_login = datetime
            self.ip = ip
            self.port = port

    class LoginHistory(OnlineUsers):
        """
        класс для таблицы с историей последнего подключения к серверу
        """

        def __init__(self, user_id, datetime, ip, port):
            super().__init__(user_id, datetime, ip, port)

    class ContactList():
        """
        класс для таблицы со cписком контактов
        """

        def __init__(self, owner_id, contact_id):
            self.owner_id = owner_id
            self.contact_id = contact_id

    def __init__(self):
        self.engine = create_engine('sqlite:///server/messenger_db.sqlite',
                                    echo=False,
                                    connect_args={'check_same_thread': False})
        self.metadata = MetaData()
        # таблица со всеми пользователями
        self.user_table = Table('Users', self.metadata,
                                Column('id', Integer, primary_key=True),
                                Column('username', String),
                                Column('last_login', DateTime),
                                Column('password', String),
                                Column('public_key', Text))
        # таблица с пользователями онлайн
        self.online_user_table = Table('Online_users', self.metadata,
                                       Column('id', Integer, primary_key=True),
                                       Column('user_id', ForeignKey('Users.id'), unique=True),
                                       Column('last_login', DateTime),
                                       Column('port', Integer),
                                       Column('ip', String))
        # таблица с историями подключений
        self.login_history_table = Table('Login_history', self.metadata,
                                         Column('id', Integer, primary_key=True),
                                         Column('user_id', ForeignKey('Users.id')),
                                         Column('last_login', DateTime),
                                         Column('port', Integer),
                                         Column('ip', String))

        # таблица со списком контактов
        self.contacts_table = Table('Contacts', self.metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('owner_id', ForeignKey('Users.id')),
                                    Column('contact_id', ForeignKey('Users.id')),
                                    UniqueConstraint('owner_id', 'contact_id')

                                    )
        # создание таблиц
        self.metadata.create_all(self.engine)
        # связываем классы с таблицами
        mapper(self.AllUsers, self.user_table)
        mapper(self.OnlineUsers, self.online_user_table)
        mapper(self.LoginHistory, self.login_history_table)
        mapper(self.ContactList, self.contacts_table)
        # создаем сессию
        server_session = sessionmaker(bind=self.engine)
        self.session = server_session()
        # обнуляем таблицу с активными юзерами при запуске сервера и сохраняем
        self.session.query(self.OnlineUsers).delete()
        self.session.commit()

    # геттеры
    def get_only_usernames(self):
        """
        list with only usernames
        """
        list_of_usernames = []
        query = self.session.query(self.AllUsers.username)
        for username in query.all():
            list_of_usernames.append(username[0])
        return list_of_usernames

    def get_user_list(self):
        """
        геттер списка всех пользователей
        :return: список (username, last_login)
        """
        query = self.session.query(
            self.AllUsers.username,
            self.AllUsers.last_login
        )
        return query.all()

    def get_online_user_list(self):
        """
        геттер списка онлайн пользователей
        :return: список (username, last_login, ip, port)
        """
        query = self.session.query(
            self.AllUsers.username,
            self.OnlineUsers.user_id,
            self.OnlineUsers.last_login,
            self.OnlineUsers.ip,
            self.OnlineUsers.port
        ).join(self.AllUsers)
        return query.all()

    def get_login_history_list(self):
        """
        геттер истории подключений
        :return: список (username, last_login, ip, port)
        """
        query = self.session.query(
            self.AllUsers.username,
            self.LoginHistory.user_id,
            self.LoginHistory.last_login,
            self.LoginHistory.ip,
            self.LoginHistory.port
        ).join(self.AllUsers)
        return query.all()

    def get_contacts_list(self, username):
        """
        геттер контактов
        :return: список (username)
        """
        # определяем id владельца
        owner_id = self.session.query(self.AllUsers).filter_by(username=username).first().id
        # определяем id всех контактов
        query = self.session.query(self.ContactList.contact_id).filter_by(owner_id=owner_id)
        contact_list = []
        # находим имя для каждого id
        try:
            for i in query.all():
                # получаем контакт
                contact = self.session.query(self.AllUsers.username).filter_by(id=i[0]).first()
                # так как контакт получен как кортеж, берем его первый элемент
                contact_list.append(contact[0])
        except Exception as exception:
            print(exception)
        return contact_list

    def get_password(self, username):
        """
        get password of a contact
        :return: hash
        """

        # определяем id всех контактов
        query = self.session.query(self.AllUsers.password).filter_by(username=username).first()
        return query[0]

    def login(self, username, ip, port, password=None, publick_key=None):
        """
        обновление таблиц при подключении пользователя
        :param username: имя
        :param ip: ip
        :param port: порт
        :return: -
        """

        # пробуем достать юзера
        login_user = self.session.query(self.AllUsers).filter_by(username=username).first()
        # если юзер подключается впервые создаем запись в таблицу всех изеров
        try:
            if login_user is None:
                login_user = self.AllUsers(username, password, publick_key)
                self.session.add(login_user)
                self.session.commit()
            # если юзер подключается не впервые - обновляем дату входа
            else:
                login_user.last_login = datetime.datetime.utcnow()
                self.session.commit()
                # добавляем в таблицу юзеров онлайн
                new_online_user = self.OnlineUsers(login_user.id,
                                                   datetime.datetime.utcnow(),
                                                   ip,
                                                   port)
                self.session.add(new_online_user)
                # добавляем в таблицу историй подключений
                new_login_history_item = self.LoginHistory(login_user.id,
                                                           datetime.datetime.utcnow(),
                                                           ip,
                                                           port)
                self.session.add(new_login_history_item)

                # сохраняем изменения
                self.session.commit()
        except Exception as exception:
            self.session.rollback()
            print(exception)


    def logout(self, username):
        """
        удаляем пользователя из таблицы онлайн пользователей при отключении
        :param username: имя пользователя
        :return: -
        """
        user = self.session.query(self.AllUsers).filter_by(username=username).first()
        self.session.query(self.OnlineUsers).filter_by(user_id=user.id).delete()
        # сохраняем изменения
        self.session.commit()

    def add_contact(self, owner_name, contact_name):
        """
        добавляем контакт
        :param owner_name: владелец контакта
        :param contact_name: имя контакта
        :return: -
        """
        # находим id
        owner_id = self.session.query(self.AllUsers).filter_by(username=owner_name).first().id
        contact_id = self.session.query(self.AllUsers).filter_by(username=contact_name).first().id
        # добавляем запись в таблицу
        try:
            new_contact = self.ContactList(owner_id, contact_id)
            self.session.add(new_contact)
            self.session.commit()
        except Exception as exception:
            self.session.rollback()
            print(exception)

    def delete_contact(self, owner_name, contact_name):
        """
        удаляем контакт
        :param owner_name: владелец контакта
        :param contact_name: имя контакта
        :return: -
        """
        # находим id
        owner_id = self.session.query(self.AllUsers).filter_by(username=owner_name).first().id
        contact_id = self.session.query(self.AllUsers).filter_by(username=contact_name).first().id
        # добавляем запись в таблицу
        try:
            self.session.query(self.ContactList).filter(
                self.ContactList.owner_id == owner_id,
                self.ContactList.contact_id == contact_id
            ).delete()
            self.session.commit()
        except Exception as exception:
            self.session.rollback()
            print(exception)


# Отладка
if __name__ == '__main__':
    test_db = MessengerStorage()
    # выполняем 'подключение' пользователя
    test_db.login('client_1', '192.168.1.4', 8888)
    test_db.login('client_2', '192.168.1.5', 7777)
    # выводим список кортежей - активных пользователей
    print(test_db.get_online_user_list())
    # выполянем 'отключение' пользователя
    test_db.logout('client_1')

    # выводим список активных пользователей
    print(test_db.get_online_user_list())
    # запрашиваем историю входов по пользователю
    test_db.get_login_history_list()
    # выводим список известных пользователей
    print(test_db.get_user_list())

    test_db.add_contact('client_1', 'client_2')
    print(test_db.get_contacts_list('client_1'))
