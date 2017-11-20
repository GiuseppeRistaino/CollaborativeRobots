from threading import Lock, Event
from Communication.Client import Client

if __name__ == '__main__':
    c1 = Client("ok", Event(), Lock()).start()