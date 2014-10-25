#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from threading import Thread
import Queue
import time
#import urllib2
#import BaseHTTPServer


class HttpServer(Thread):
    def __init__(self, conn_queue, ip="127.0.0.1", port=50000):
        Thread.__init__(self, name="HttpServerThread")
        self.conn_queue = conn_queue
        self.ip = ip
        self.port = port
        self.running = False

    def start(self):
        self.running = True
        Thread.start(self)

    def run(self):
        print "Socket server starting server run loop\n"
        address = (self.ip, self.port)
        http_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_IP)
        http_socket.bind(address)
        http_socket.listen(1)
        while self.running:
            print "Socket server waiting to accept new connection\n"
            conn, addr = http_socket.accept()
            self.conn_queue.put((conn, addr))

        print "Socket server shutting down\n"
        http_socket.shutdown()
        http_socket.close()

    def stop(self):
        self.running = False


class ProtocolWorker(Thread):
    def __init__(self, conn_queue):
        Thread.__init__(self, name="WorkerThread")
        self.conn_queue = conn_queue
        self.running = False

    def execute_protocol_logic(self, conn, client_addr):
        pass

    def start(self):
        self.running = True
        Thread.start(self)

    def stop(self):
        self.running = False

    def run(self):
        print "ProtocolWorker scanning connection queue for new work"
        while self.running:
            conn = None
            try:
                conn, client_addr = self.conn_queue.get_nowait()
                self.execute_protocol_logic(conn, client_addr)
            except Queue.Empty:
                time.sleep(1)
            except Exception as ex:
                print "ProtocolWorker got an exception - %s" % ex
            finally:
                if conn is not None:
                    conn.shutdown(socket.SHUT_RDWR)
                    conn.close()

    def receive_message(self, conn):
        message = ""
        while not message.endswith("\r\n"):
            received = conn.recv(1024)
            message += received
        return message

    def parse_message(self, message):
        parsed = message.split()
        method = parsed[0]
        protocol = parsed[2]
        return method, protocol

    def return_response(self, method, protocol):
        if method == 'GET':
            if protocol == 'HTTP/1.1':
                return '%s 200 OK\r\n\r\n' % protocol
            else:
                return '%s 505 HTTP Version Not Supported\r\n\r\n' % protocol
        else:
            return '%s 405 Method Not Allowed\r\n\r\n' % method


class HttpProtocolWorker(ProtocolWorker):
    def __init__(self, conn_queue):
        ProtocolWorker.__init__(self, conn_queue)

    def execute_protocol_logic(self, conn, client_addr):
        print "HttpProtocolWorker handling new HTTP connection"
        message = self.receive_message(conn)
        print "HttpProtocolWorker got all data:"
        method, protocol = self.parse_message(message)
        response = self.return_response(method, protocol)
        print "response:" + response  # cut off return lines
        conn.sendall(response)
        print "HttpProtocolWorker done"


if __name__ == '__main__':
    global_conn_queue = Queue.Queue()
    worker = HttpProtocolWorker(global_conn_queue)
    server = HttpServer(global_conn_queue)
    try:
        worker.start()
        server.start()
    except KeyboardInterrupt:
        server.running = False
        server.close()
        print "Exiting"
