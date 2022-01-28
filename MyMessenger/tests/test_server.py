import datetime
import unittest

from server import MessengerServer


class TestServer(unittest.TestCase):
    def test_answer_1(self):
        self.assertEqual(MessengerServer().answer({
            "action": 'presence',
            "time": datetime.datetime.utcnow(),
            "user": 'Guest',
            "data": 'data'
        }), MessengerServer().server_response(200))

    def test_answer_2(self):
        self.assertEqual(MessengerServer().answer({
            "action": 'not_presence',
            "time": datetime.datetime.utcnow(),
            "user": 'Guest',
            "data": 'data'
        }), MessengerServer().server_response(400))


    def test_answer_3(self):
        self.assertEqual(MessengerServer().answer({
            "action": 'presence',
            "time": datetime.datetime.utcnow(),
            "user": 'notGuest',
        }), MessengerServer().server_response(400))


if __name__ == '__main__':
    unittest.main()