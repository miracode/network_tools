#!/usr/bin/env python
import socket
import sys


class EchoClient(object):
    def __init__(self, msg):
        self.running = False
        self.msg = msg

    def start(self):
        "Socket client starting\n"
        client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_IP)
        client_socket.connect(('127.0.0.1', 50000))

        client_socket.sendall(self.msg)
        client_socket.shutdown(socket.SHUT_WR)

        client_socket.close()


if __name__ == '__main__':
    client = EchoClient(sys.argv[1])
    client.start()
