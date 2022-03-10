import time
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

    def get_jim_data(self):
        return JIM().jim_data

    def get_jim_responses(self):
        return JIM().response

    def get_jim_action(self):
        return JIM().jim_action

    def get_jim_user(self):
        return JIM().jim_user

    def get_jim_time(self):
        return JIM().jim_time

    def get_jim_to_user(self):
        return JIM().jim_to_user

    def jim_create_message(self, action, username, data='', to_user=''):
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

    def jim_create_server_response(self, response, alert=''):
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
