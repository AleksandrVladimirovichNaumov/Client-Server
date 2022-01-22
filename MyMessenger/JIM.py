import datetime


class JIM():

    def __init__(self):
        errors = {
            100: 'базовое уведомление',
            101: 'важное уведомление',
            200: 'OK',
            201: 'объект создан',
            202: 'подтверждение',
            400: 'неправильный запрос/JSON-объект',
            401: 'не авторизован',
            402: 'неправильный логин/пароль',
            403: 'пользователь заблокирован',
            404: 'пользователь/чат отсутствует на сервере',
            409: 'уже имеется подключение с указанным логином',
            410: 'адресат существует, но недоступен (offline)',
            500: 'ошибка сервера'
        }


class JIMClient(JIM):

    def __init__(self):
        super.__init__()


    def server_request(self, action, userdata, data=None):
        """
        шаблон для отправки запроса на сервер
        :param action: тип запроса
        :param userdata: от кого
        :param data: что отправляем
        :return: словарь для отправки на сервер
        """
        return {
            "action": action,
            "time": datetime.datetime,
            "user": userdata,
            "data": data

        }

    def presence(self, name='username'):
        """
        первичный запрос на подключение к серверу
        :param name: пользователь
        :return: словарь для отправки на сервер
        """
        return self.server_request('presence', name)


class JIMServer(JIM):

    def __init__(self):
        super.__init__()

    def server_response(self, response, alert=None):
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
