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

        msg_recv = threading.Thread(target=self.msg_recv)

        msg_recv.daemon = True
        msg_recv.start()

        self.stopped = Event()

        self.robot = robot
        self.lock = lock
        #self.radius_list = [1, 2, 3, 4]

    def run(self):
        while not self.stopped.wait(5):
            self.lock.acquire()
            self.send_msg(self.robot.obstacles)
            self.lock.release()

    def msg_recv(self):
        while True:
            try:
                data = b""
                while True:
                    chunk = self.sock.recv(1024)
                    print("bhoooooooooooooooooooooooooooooooooooo")
                    print(chunk)
                    if chunk != b'end':
                        data += chunk
                    else:
                        break
                #data = self.sock.recv(1024)
                print("DATA FINALLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
                print(data)
                if data:
                    obstacles = pickle.loads(data)
                    self.lock.acquire()
                    self.robot.compare_obstacles(obstacles)
                    print(obstacles)
                    self.lock.release()
            except:
                pass

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

