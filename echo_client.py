import socket


class Echo_Client:

    def __init__(self):
        self.client_socket = None

    def create_socket(self):
        self.client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_IP)
