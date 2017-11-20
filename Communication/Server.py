import socket
import threading
from threading import Thread
import sys
import pickle
import io


class Server():


    def __init__(self, host="localhost", port=4000):

        self.clients = []
        #crea una socket inet di tipo sock_stream
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # associa il socket a un host e alla porta 4000
        self.sock.bind((str(host), int(port)))
        # Il server é in ascolto e vengono messe in coda al massimo 10 richieste di connessione
        self.sock.listen(10)
        # rende la socket non bloccante
        self.sock.setblocking(True)

        # Thread per accettare connessioni
        accept = threading.Thread(target=self.acceptCon)
        # Thread che riceve la lista degli ostacoli e li rinvia ai client della rete

        #Il thread accept e proccess vengono dichiarati daemon e runnati
        accept.daemon = True
        accept.start()


        #La condizione per fermare il server è digitare esci
        while True:
            msg = input('->')
            if msg == 'esci':
                self.sock.close()
                sys.exit()
            else:
                pass

    #funzione che accetta le connessioni
    def acceptCon(self):
        print("Accettazione")
        while True:
            try:
                conn, addr = self.sock.accept()
                conn.setblocking(True)
                self.clients.append(conn)
                self.Connection(conn, self.clients).start()

            except:
                pass


    class Connection(Thread):

        def __init__(self, conn, clients):
            Thread.__init__(self)
            self.conn = conn
            self.clients = clients

        def run(self):
            while True:
                data = b''
                try:
                    chunk = self.conn.recv(1024)
                    while chunk != b'end':
                        data += chunk
                        chunk = self.conn.recv(1024)
                    data = pickle.loads(data)
                    self.msg_to_all(data, self.conn)
                except:
                    pass

        # funzione che permette di inviare il messaggio di un client, in pacchetti di 1024 byte, a tutti gli
        # altri client della rete
        def msg_to_all(self, msg, cliente):

            sending = pickle.dumps(msg)
            for c in self.clients:
                try:
                    if c != cliente:
                        msg = io.BytesIO(sending)
                        while True:
                            chunk = msg.read(1024)
                            if not chunk:
                                c.send(b'end')
                                break
                            c.send(chunk)
                except BaseException as e:
                    print(e)
                    self.clients.remove(c)


s = Server()