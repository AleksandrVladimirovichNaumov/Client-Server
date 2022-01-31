from datetime import datetime
import unittest

from jim import JIM, JIMClient, JIMServer


class TestJIM(unittest.TestCase):
    def test_response(self):
        self.assertEqual(JIM().get_jim_responses(), {
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
            500: 'ошибка сервера',
        })

    def test_action(self):
        self.assertEqual(JIM().get_jim_action(), 'action')

    def test_user(self):
        self.assertEqual(JIM().get_jim_user(), 'user')

    def test_time(self):
        self.assertEqual(JIM().get_jim_time(), 'time')

    def test_serverresponse(self):
        method_result = JIMClient().server_request('action', 'username', 'data')
        self.assertEqual(method_result, {
            "action": 'action',
            "time": method_result.get('time'),
            "user": 'username',
            "data": 'data'

        })

    def test_clientresponse(self):
        self.assertEqual(JIMServer().server_response('response', 'alert'), {
            "response": 'response',
            "alert": 'alert',

        })


if __name__ == '__main__':
    unittest.main()
