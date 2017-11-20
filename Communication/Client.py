import socket
import threading
from threading import Thread, Event
import io
import pickle


class Client(Thread):


    def __init__(self, robot, lock, host="localhost", port=4000):
        Thread.__init__(self)
        # crea socket INET di tipo STREAM
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connessione al server web sulla porta 4000
        self.sock.connect((str(host), int(port)))

        # msg_recv thread daemon per la ricezione dei messaggi
        msg_recv = threading.Thread(target=self.msg_recv)

        msg_recv.daemon = True
        msg_recv.start()

        self.stopped = Event()

        self.robot = robot
        self.lock = lock
        #self.radius_list = [1, 2, 3, 4]

    def run(self):
        while not self.stopped.wait(5):
            #Nel momento in cui i robot devono scambiarsi la lista degli ostacoli è possibile
            #che tale lista venga utilizzata per altre attività e quindi i valori al suo interno
            #potrebbero cambiare. Per questo motivo lo stesso lock utilizzato sulla stessa risorsa
            #viene richiamato in questa funzione.
            self.lock.acquire()
            self.send_msg(self.robot.obstacles)
            self.lock.release()

    #funzione che permette di ricevere il messaggio inoltrato dal server, in pacchetti da 1024 byte, e che
    # richiama la funzione compare_obstacle di robot.
    def msg_recv(self):
        while True:
            try:
                data = b""
                while True:
                    chunk = self.sock.recv(1024)
                    print(chunk)
                    if chunk != b'end':
                        data += chunk
                    else:
                        break
                #data = self.sock.recv(1024)
                print(data)
                if data:
                    obstacles = pickle.loads(data)
                    self.lock.acquire()
                    self.robot.compare_obstacles(obstacles)
                    print(obstacles)
                    self.lock.release()
            except:
                pass
    #funzione che invia il messaggio del client(la lista degli ostacoli) in pacchetti da 1024 byte
    def send_msg(self, msg):
        data_send = pickle.dumps(msg)
        #self.sock.send(pickle.dumps(msg))
        data = io.BytesIO(data_send)
        while True:
            chunk = data.read(1024)
            if not chunk:
                self.sock.send(b'end')
                break
            self.sock.send(chunk)

