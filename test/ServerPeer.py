import socket
from threading import Thread
import pickle

class Server(Thread):

    def __init__(self, address):
        Thread.__init__(self)
        # Per Protocollo UDP utilizzare - socket.SOCK_DGRAM
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.bind(address)
        self.server_socket.listen(2)

    def run(self):
        while True:
            conn, addr = self.server_socket.accept()
            Connection_Thread(conn, addr).start()


class Connection_Thread(Thread):
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def run(self):
        print("sto inviando la lista a " +str(self.addr))
        lista = [1, 2, 3, 4]
        data_send = pickle.dumps(lista)
        self.conn.send(bytes(data_send))
        self.conn.close()


s1 = Server(('127.0.0.1', 8080))
s1.start()
s2 = Server(('127.0.0.1', 8081))
s2.start()