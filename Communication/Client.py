import socket
import threading
from threading import Thread, Event
import sys
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
                data = self.sock.recv(1024) #fino a 11 ostacoli
                if data:
                    obstacles = pickle.loads(data)
                    self.lock.acquire()
                    self.robot.compare_obstacles(obstacles)
                    print(obstacles)
                    self.lock.release()
            except:
                pass

    def send_msg(self, msg):
        self.sock.send(pickle.dumps(msg))
