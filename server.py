#server.py
import time
from socket import *
import pickle
import numpy as np
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Socket Programming')
    parser.add_argument('--p', default=9784, type=int)
    args = parser.parse_args()
    return args

class Server:
    def __init__(self, SERVER_ADDRESS):
        self.address  = SERVER_ADDRESS
        self.socket   = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(self.address)
        self.socket.listen(1)
        print("server is ready")
        self.client_socket, self.client_addr = self.socket.accept()
        print(f"server connected by {self.client_addr}")
        self.request = None
        self.connected = True

    def send(self):
        if self.request != None and self.request != 0:
            data = np.random.rand(self.request)
            data_byte = pickle.dumps(data)
            self.client_socket.sendall(str(len(data_byte)).encode())

            self.client_socket.sendall(data_byte)
            print(f"DATA SENT")
            print(f"np.shape(data_byte):{np.shape(data_byte)}")
            print(f"len(data_byte):{len(data_byte)}")
            self.request = None
        
    def recv(self):
        recv_data = []
        while True:
            chunk = self.client_socket.recv(4096)
            recv_data.append(chunk)
            if len(chunk) < 4096:
                break
        self.request = pickle.loads(b''.join(recv_data))
        if self.request == 0:
            self.client_socket.close()
            self.connected = False
            print("DISCONNECTED")
            self.connect()
            return
        
        print(f"RECEIVCED DATA: {self.request}")
        
    def connect(self):
        print("WAITING FOR NEW CONNECTION")
        self.socket.listen(1)
        self.client_socket, self.client_addr = self.socket.accept()
        print(f"server connected by {self.client_addr}")
        self.is_connected = True
    
    def run(self):
        while True:
            self.recv()
            self.send()

if __name__ == '__main__':
    args = parse_args()
    SERVER_ADDRESS = ('0.0.0.0', args.p)
    server = Server(SERVER_ADDRESS)
    server.run()