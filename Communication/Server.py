import socket
import threading
import sys
import pickle


class Server():


    def __init__(self, host="localhost", port=4000):

        self.clients = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # associa il socket a un host e alla porta 4000
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)
        self.sock.setblocking(False)

        accept = threading.Thread(target=self.acceptCon)
        process = threading.Thread(target=self.processCon)

        accept.daemon = True
        accept.start()

        process.daemon = True
        process.start()

        while True:
            msg = input('->')
            if msg == 'esci':
                self.sock.close()
                sys.exit()
            else:
                pass

    def msg_to_all(self, msg, cliente):
        for c in self.clients:
            try:
                if c != cliente:
                    c.send(msg)
            except:
                self.clients.remove(c)

    def acceptCon(self):
        print("Accettazione")
        while True:
            try:
                conn, addr = self.sock.accept()
                conn.setblocking(False)
                self.clients.append(conn)
            except:
                pass

    def processCon(self):
        print("Processamento")
        while True:
            if len(self.clients) > 0:
                for c in self.clients:
                    try:
                        data = c.recv(1024)     #fino a 11 ostacoli
                        if data:
                            self.msg_to_all(data, c)
                    except:
                        pass


s = Server()