#!/usr/bin/env python
import socket


class EchoServer(object):
    def __init__(self):
        self.running = False

    def start(self):
        self.running = True
        print "Socket server starting\n"
        server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_IP)
        server_socket.bind(('127.0.0.1', 50000))
        server_socket.listen(1)
        while self.running:
            conn, addr = server_socket.accept()
            message = conn.recv(32)
            print message
            conn.close()
        server_socket.close()
        print "Socket server dying\n"

    def stop(self):
        self.running = False


if __name__ == '__main__':
    server = EchoServer()
    server.start()
