#!/usr/bin/env python
import socket
from threading import Thread
import Queue
import time


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
            try:
                self.conn_queue.put(http_socket.accept())
                conn, addr = http_socket.accept()
            except KeyboardInterrupt:
                "exit"
                http_socket.shutdown()
                http_socket.close()
                self.running = False

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


class HttpProtocolWorker(ProtocolWorker):
    def __init__(self, conn_queue):
        ProtocolWorker.__init__(self, conn_queue)

    def execute_protocol_logic(self, conn, client_addr):
        print "HttpProtocolWorker handling new HTTP connection"
        http_req = ""
        data = bytearray(1024)
        while not http_req.endswith("\r\n\r\n"):
            print "HttpProtocolWorker reading data from client"
            read_bytes = conn.recv_into(data, 1024)
            if read_bytes == 0:
                print "HttpProtocolWorker connection lost"
                return None
            http_req += data[:read_bytes]
        print "HttpProtocolWorker got all data"
        conn.sendall("HTTP/1.1 200 OK\r\nYou said: " + http_req + "\r\n\r\n")
        print "HttpProtocolWorker done"


if __name__ == '__main__':
    global_conn_queue = Queue.Queue()
    worker = HttpProtocolWorker(global_conn_queue)
    server = HttpServer(global_conn_queue)
    worker.start()
    server.start()
