import socket
import pickle
from threading import Thread, Event

class Client(Thread):

    def __init__(self, robot):
        Thread.__init__(self)
        self.robot = robot
        self.stopped = Event()

    def run(self):
        while not self.stopped.wait(5):
            file = open("address_list", 'r')
            for line in file:
                address = line.strip().split(',')
                if(address[0] != self.robot.address[0] or address[1] != self.robot.address[1]):
                    Connection(address, self.robot).start()
            #exit()

class Connection(Thread):

    def __init__(self, address, robot):
        Thread.__init__(self)
        self.robot = robot
        self.address = address

    def run(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.address[0], int(self.address[1])))

        data = b""
        while True:
            chunk = client_socket.recv(1024)
            if chunk:
                data += chunk
            else:
                break
        if data:
            data = pickle.loads(data)
            print("Ricevuto: ", data)
            self.robot.compare_obstacles(data)
