import socket
import random

class Channel():
    
    def __init__(self):
        self.senderhost = '127.0.0.1'
        self.senderport = 8080
        
        self.receiverhost = '127.0.0.2'
        self.receiverport = 9090
        
        self.sendersock = socket.socket()
        self.receiversock = socket.socket()
        
        self.sendconn = None
        self.recvconn = None
        
    def initSenders(self):
        self.sendersock.bind((self.senderhost, self.senderport))
        self.sendersock.listen(1)
        self.sendconn,_ = self.sendersock.accept()
    
    def initReceivers(self):
        self.receiversock.bind((self.receiverhost, self.receiverport))
        self.receiversock.listen(1)
        self.recvconn,_ = self.receiversock.accept()
    
    def Medium(self):
        while True:
            a = self.sendconn.recv(1024).decode()
            print("received from sender: " + a)
            self.recvconn.send(a.encode())
            print("sent to receiver: " + a)
            b = self.recvconn.recv(1024).decode()
            print("received from receiver: " + b)
            self.sendconn.send(b.encode())
            print("sent to sender: " + b)
        

if __name__ == '__main__':
    channel = Channel()
    channel.initSenders()
    channel.initReceivers()
    channel.Medium()
    channel.sendersock.close()
    channel.receiversock.close()
    print("done") 
        
        
    