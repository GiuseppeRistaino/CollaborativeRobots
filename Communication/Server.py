import socket
import threading
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
        self.sock.setblocking(False)

        # Thread per accettare connessioni
        accept = threading.Thread(target=self.acceptCon)
        # Thread che riceve la lista degli ostacoli e li rinvia ai client della rete
        process = threading.Thread(target=self.processCon)

        #Il thread accept e proccess vengono dichiarati daemon e runnati
        accept.daemon = True
        accept.start()

        process.daemon = True
        process.start()

        #La condizione per fermare il server è digitare esci
        while True:
            msg = input('->')
            if msg == 'esci':
                self.sock.close()
                sys.exit()
            else:
                pass


    #funzione che permette di inviare il messaggio di un client, in pacchetti di 1024 byte, a tutti gli
    #altri client della rete
    def msg_to_all(self, msg, cliente):
        for c in self.clients:
            try:
                if c != cliente:
                    #c.send(msg)
                    msg = io.BytesIO(msg)
                    while True:
                        chunk = msg.read(1024)
                        if not chunk:
                            c.send(b'end')
                            break
                        c.send(chunk)
            except:
                self.clients.remove(c)

    #funzione che accetta le connessioni
    def acceptCon(self):
        print("Accettazione")
        while True:
            try:
                conn, addr = self.sock.accept()
                conn.setblocking(False)
                self.clients.append(conn)
            except:
                pass

    #funzione che permette di ricevere il messaggio di un client, in pacchetti di 1024 byte, e
    #richiama la funzione msg_to_all
    def processCon(self):
        print("Processamento")
        data = b""
        while True:
            if len(self.clients) > 0:
                for c in self.clients:
                    try:
                        #data = c.recv(1024)
                        while True:
                            chunk = c.recv(1024)
                            if chunk != b'end':
                                data += chunk
                            else:
                                self.msg_to_all(data, c)
                                data = b""
                                break
                    except:
                        pass


s = Server()