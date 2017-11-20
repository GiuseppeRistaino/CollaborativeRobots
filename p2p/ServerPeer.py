import socket
from threading import Thread
import pickle
import io

class Server(Thread):

    def __init__(self, robot):
        Thread.__init__(self)
        self.robot = robot
        # Per Protocollo UDP utilizzare - socket.SOCK_DGRAM
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.bind(self.robot.address)
        self.server_socket.listen(2)

    # Per ogni connessione accettata fa partire il Thread Connection_Thread
    def run(self):
        while True:
            conn, addr = self.server_socket.accept()
            Connection_Thread(conn, addr, self.robot).start()


class Connection_Thread(Thread):
    def __init__(self, conn, addr, robot):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.robot = robot

    # Invia la lista degli ostacoli agli altri peer attraverso pacchetti da 1024 byte
    def run(self):
        print("sto inviando la lista a " +str(self.addr))
        data_send = pickle.dumps(self.robot.obstacles)
        data = io.BytesIO(data_send)
        while True:
            chunk = data.read(1024)
            if not chunk:
                break
            self.conn.send(chunk)
        self.conn.close()

