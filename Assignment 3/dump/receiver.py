import socket

class Receiver():
    def __init__(self):
        self.host = '127.0.0.2'
        self.port = 9090
        self.mysocket = socket.socket()
        self.mysocket.connect((self.host, self.port))
        
    def receiver(self):
        while True:
            data = self.mysocket.recv(1024).decode()
            print("Received data: ", data)
            
receiver = Receiver()
receiver.receiver()

