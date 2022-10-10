import socket
import threading
import time

data = None

class Channel():
    def __init__(self, senders, receivers):
        self.senders = senders
        self.senderhost = '127.0.0.1'
        self.senderport = 8080
        
        self.receivers = receivers
        self.receiverhost = '127.0.0.2'
        self.receiverport = 9090
        
        self.sendersock = socket.socket()
        self.receiversock = socket.socket()
        
        self.sendconn = []
        self.recvconn = None
        
        self.e1 = threading.Event()
        self.e2 = threading.Event()
        
    def InitSenders(self):
        self.sendersock.bind((self.senderhost, self.senderport))
        self.sendersock.listen(self.senders)
        
        for i in range(0,self.senders):
            conn = self.sendersock.accept()
            self.sendconn.append(conn)
            print("Initiated sender ", i+1)
        
        print("All senders initiated")
        
    
    def InitReceivers(self):
        self.receiversock.bind((self.receiverhost, self.receiverport))
        self.receiversock.listen(1)
        self.recvconn = self.receiversock.accept()
        
        print("Receiver initiated")
    
    def StartChannel(self):
        self.receiverthread = threading.Thread(target=self.Receive)
        self.statusthread = threading.Thread(target=self.statusHandler)
        self.receiverthread.start()
        self.statusthread.start()
    
    def Receive(self):
        while True:
            for i in range(0, self.senders):
                data = self.sendconn[i][0].recv(1024).decode()
                print("Received data from sender ", i+1, " : ", data)
                self.e1.set()
            
    
    def statusHandler(self):
        file = open("busy.txt", "w")
        file.write("0")
        file.close()
        while True:
            self.e1.wait()
            fileout = open('busy.txt',"w")
            fileout.write(str(1))
            fileout.close()
            print("Sending data to receiver, Transmission time = 3 seconds")
            time.sleep(3)
            self.recvconn[0].send(data.encode())
            fileout = open('busy.txt',"w")
            fileout.write(str(1))
            fileout.close()
            self.e1.clear()
            

senders = int(input("Enter number of senders: "))
recvrs = int(input("Enter number of receivers: "))

channel = Channel(senders, recvrs)

channel.InitSenders()
channel.InitReceivers()
channel.StartChannel()