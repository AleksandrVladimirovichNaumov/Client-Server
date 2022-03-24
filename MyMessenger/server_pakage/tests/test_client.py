import unittest

from client_package.client import MyMessengerClient


class TestClient(unittest.TestCase):
    def test_respons_meaning(self):
        """
        Тест на проверку расшифровки ответа от сервера
        :return:
        """
        self.assertEqual(MyMessengerClient().response_meaning(b'{"response":200}'),f'ответ сервера [200]: OK')

if __name__ == '__main__':
    unittest.main()