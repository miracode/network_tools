"""Run echo_server in another terminal and run this to test"""
import echo_client
import unittest

class TestServer(unittest.TestCase):
    def start_client(self):
        client = echo_client.EchoClient("Hello World")
        client.start()
        # still can't figure this out