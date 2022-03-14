"""module for jim protocol"""
from datetime import datetime


class JIM():
    """
    протокол структуры сообщений и отправки ответов от сервера
    """

    def __init__(self):
        self.response = {
            100: 'базовое уведомление',
            101: 'важное уведомление',
            200: 'OK',
            201: 'объект создан',
            202: 'список контактов',
            203: 'контакт удален',
            204: 'контакт создан',
            205: 'отправлен запрос на аунтефикацию',
            400: 'неправильный запрос/JSON-объект',
            401: 'не авторизован',
            402: 'неправильный логин/пароль',
            403: 'пользователь заблокирован',
            404: 'пользователь/чат отсутствует на сервере',
            409: 'уже имеется подключение с указанным логином',
            410: 'адресат существует, но недоступен (offline)',
            500: 'ошибка сервера',
        }
        self.jim_action = 'action'
        self.jim_user = 'user'
        self.jim_time = 'time'
        self.jim_data = 'data'
        self.jim_to_user = 'to_user'

    @staticmethod
    def get_jim_data():
        """data getter"""
        return JIM().jim_data

    @staticmethod
    def get_jim_responses():
        """response getter"""
        return JIM().response

    @staticmethod
    def get_jim_action():
        """action getter"""
        return JIM().jim_action

    @staticmethod
    def get_jim_user():
        """user getter"""
        return JIM().jim_user

    @staticmethod
    def get_jim_time():
        """time getter"""
        return JIM().jim_time

    @staticmethod
    def get_jim_to_user():
        """to_user getter"""
        return JIM().jim_to_user

    @staticmethod
    def jim_create_message(action, username, data='', to_user=''):
        """
        шаблон для отправки сообщения
        :param action: тип запроса
        :param user: от кого
        :param data: что отправляем
        :param to_user: от кому
        :return: словарь для отправки на сервер
        """
        return {
            "action": action,
            "time": str(datetime.utcnow()),
            "user": username,
            "to_user": to_user,
            "data": data

        }


class JIMClient(JIM):
    """
    протокол для клиентов. пока что функционал базового протокола JIM
    """

    def __init__(self):
        super().__init__()


class JIMServer(JIM):
    """
    протокол для сервера
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def jim_create_server_response(response, alert=''):
        """
        шаблон ответа сервера
        :param response: ответ
        :param alert: код ошибки
        :return:
        """
        return {
            "response": response,
            "alert": alert,
        }
