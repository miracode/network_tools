"""Run http_server.py in another terminal to run tests"""

import socket
import unittest
#import http_server


class TestHttpServer(unittest.TestCase):

    def start_client(self):
        self.client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_IP)

        self.client_socket.connect(('127.0.0.1', 50000))

    def test_OK(self):
        self.start_client()

        self.client_socket.sendall("GET / HTTP/1.1\r\n\r\n")
        received = self.client_socket.recv(1024)
        self.client_socket.shutdown(socket.SHUT_WR)
        self.client_socket.close()
        self.assertEquals(received, "HTTP/1.1 200 OK\r\n\r\n")

    def test_bad_method(self):
        self.start_client()

        self.client_socket.sendall("POST / HTTP/1.1\r\n\r\n")
        received = self.client_socket.recv(1024)
        self.client_socket.shutdown(socket.SHUT_WR)
        self.client_socket.close()
        self.assertEquals(received, "HTTP/1.1 405 Method Not Allowed\r\n\r\n")

    def test_bad_version(self):
        self.start_client()

        self.client_socket.sendall("GET / HTTP/1.0\r\n\r\n")
        received = self.client_socket.recv(1024)
        self.client_socket.shutdown(socket.SHUT_WR)
        self.client_socket.close()
        self.assertEquals(received, "HTTP/1.1 505 HTTP Version Not \
Supported\r\n\r\n")

    def test_bad_input(self):
        self.start_client()
        self.client_socket.sendall("Bad Request\r\n\r\n")
        received = self.client_socket.recv(1024)
        self.client_socket.shutdown(socket.SHUT_WR)
        self.client_socket.close()
        self.assertEquals(received, "HTTP/1.1 400 Bad Request\r\n\r\n")

if __name__ == '__main__':
    unittest.main()
