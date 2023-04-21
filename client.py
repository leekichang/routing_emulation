#client.py
import config as cfg
import time
from socket import *
import pickle
import numpy as np
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Socket Programming')
    parser.add_argument('--ip', default='127.0.0.1', type=str)
    parser.add_argument('--p', default=cfg.R_PORT, type=int)
    args = parser.parse_args()
    return args

class Client:
    def __init__(self, SERVER_ADDRESS):
        self.SERVER_ADDRESS = SERVER_ADDRESS
        self.socket = None
        self.connect()
        self.connected = True
        print("Client Connected!")

    def send(self):
        data = int(input('>>>'))
        self.socket.sendall(pickle.dumps(data))
        print('SENT!')
        if data == 0:
            print("DISCONNECTED!")
            self.connected = False
            self.socket.close()

    def recv(self):
        data_total_len = int(self.socket.recv(1024))
        left_recv_len  = data_total_len
        buffer_size    = data_total_len

        recv_data = []
        while True:
            chunk = self.socket.recv(buffer_size)
            recv_data.append(chunk)
            left_recv_len -= len(chunk)
            if left_recv_len <= 0:
                break
        if not left_recv_len == 0:
            print("Packet Loss!")
            return -1
        else:
            recv_data = pickle.loads(b"".join(recv_data))
            print(f'받은 데이터:{recv_data}\n\n{data_total_len}')
            return recv_data
    
    def run(self):
        while True:
            self.send()
            if not self.check_connection():break
            self.recv()
            if not self.check_connection():break

    def connect(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect(self.SERVER_ADDRESS)
        self.connected = True
        
    def check_connection(self):
        return self.connected

if __name__ == '__main__':
    args = parse_args()
    SERVER_ADDRESS = (args.ip, args.p)
    client = Client(SERVER_ADDRESS)
    client.run()