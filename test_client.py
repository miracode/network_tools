# -*- coding: utf-8 -*-
import unittest
import echo_client


class MyTest(unittest.TestCase):
    def test_socket(self):
        client = echo_client.Echo_Client()
        client.create_socket()
        assert client.client_socket.family == 2
        assert client.client_socket.type == 1
        assert client.client_socket.proto == 0

if __name__ == '__main__':
    unittest.main()
