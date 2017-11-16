import socket
import pickle

class Client():

    def start(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1", 8080))

        while True:
            data = client_socket.recv(512)
            data = pickle.loads(data)
            print ("Ricevuto: " , data)

            print("Data send successfully")
            exit()


c = Client()
c.start()