"""module for work with client local database"""
import datetime
import os

from sqlalchemy import __version__, create_engine, Table, Column, MetaData,\
    Integer, String, Boolean, DateTime
from sqlalchemy.orm import mapper, sessionmaker


class ClientStorage:
    """main class for client local database"""
    print(f"Version of SQLAlchemy: {__version__}")

    class ContactList:
        """
        local copy of client list
        """

        def __init__(self, contact_username):
            self.id = None
            self.contact_username = contact_username

    class MessageHistory:
        """
        local message history
        """

        def __init__(self, contact_username, from_or_to, message, date_time):
            self.id = None
            self.contact_username = contact_username
            self.from_or_to = from_or_to
            self.message = message
            self.datetime = date_time

    def __init__(self, username):
        # each client will have local db
        path = os.path.dirname(os.path.realpath(__file__))
        filename = f'db_{username}.db3'
        self.engine = create_engine(f'sqlite:///{os.path.join(path, filename)}',
                                    echo=False,
                                    pool_recycle=7200,
                                    connect_args={'check_same_thread': False})
        # create metadata
        self.metadata = MetaData()

        # table with contacts
        self.contact_list_table = Table('Contact_list',
                                        self.metadata,
                                        Column('id', Integer, primary_key=True),
                                        Column('contact_username', String, unique=True))

        # table for message history
        self.message_history_table = Table('Message_history',
                                           self.metadata,
                                           Column('id', Integer, primary_key=True),
                                           Column('contact_username', String),
                                           Column('from_or_to', Boolean),
                                           Column('message', String),
                                           Column('datetime', DateTime))

        # create tables
        self.metadata.create_all(self.engine)
        # connect classes with tables
        mapper(self.ContactList, self.contact_list_table)
        mapper(self.MessageHistory, self.message_history_table)

        # create session
        server_session = sessionmaker(bind=self.engine)
        self.session = server_session()
        # saves all changes
        self.session.commit()

    # getters
    def get_message_history(self, contact_username):
        """
        getter history of messages
        :return: (contact_username, from_or_to, message, datetime)
        """
        query = self.session.query(self.MessageHistory).filter_by(contact_username=contact_username)
        return [(history_row.contact_username,
                 history_row.from_or_to,
                 history_row.message,
                 history_row.datetime) for history_row in query.all()]

    def get_contact_list(self):
        """
        getter al user's contacts
        :return: (username)
        """
        query = self.session.query(self.ContactList)
        return [contact.contact_username for contact in query.all()]

    def add_contact(self, contact_username):
        """
        add contact to contact list table
        """
        try:
            new_contact = self.ContactList(contact_username)
            self.session.add(new_contact)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            return False

    def delete_contact(self, contact_username):
        """
        delete contact from contact list table
        """
        try:
            self.session.query(self.ContactList).filter(
                self.ContactList.contact_username == contact_username).delete()
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            return False

    def add_message(self, contact_username, from_or_to, message):
        """
        add message to local message history table
        """
        try:
            new_message = self.MessageHistory(contact_username,
                                              from_or_to,
                                              message,
                                              datetime.datetime.utcnow())
            self.session.add(new_message)
            self.session.commit()
        except Exception:
            self.session.rollback()

    def get_messages_history(self, contact_username):
        """
        get message history for selected contact
        """
        try:
            messages_history = self.session.query(self.MessageHistory).filter(
                self.MessageHistory.contact_username == contact_username).all()
            return [(f'{row.message} \n {row.datetime.replace(microsecond=0)}',
                     row.from_or_to) for row in
                    messages_history]
        except Exception:
            return []
