#router.py
import time
import pickle
import numpy as np
import threading
from socket import *
from server import *
from client import *

class Receiver(Server):
    def __init__(self, SERVER_ADDRESS):
        super().__init__(SERVER_ADDRESS)
    
    def send(self, data):
        data_byte = pickle.dumps(data)
        self.client_socket.sendall(str(len(data_byte)).encode())
        time.sleep(1)

        self.client_socket.sendall(data_byte)
        print(f"DATA SENT")
        print(f"np.shape(data_byte):{np.shape(data_byte)}")
        print(f"len(data_byte):{len(data_byte)}")

class Sender(Client):
    def __init__(self, SERVER_ADDRESS):
        super().__init__(SERVER_ADDRESS)
    
    def send(self, data):
        self.socket.sendall(pickle.dumps(data))
        print('SENT!')
        if data == 0:
            print("DISCONNECTED!")
            self.connected = False
            self.socket.close()
        

class Router:
    def __init__(self, ROUTER_ADDRESS, SERVER_ADDRESS):
        self.receiver = Receiver(ROUTER_ADDRESS)
        self.sender   = Sender(SERVER_ADDRESS)

    def run(self):
        while True:
            self.receiver.recv()
            request  = self.receiver.request
            if request == 0 or request == None:
                self.receiver.recv()
                request  = self.receiver.request
            self.sender.send(data=request)
            response = self.sender.recv()
            self.receiver.send(data=response)
        

if __name__ == '__main__':
    RA = ('0.0.0.0', 9000)
    SA = ('127.0.0.1', 9001)
    router = Router(RA, SA)
    router.run()