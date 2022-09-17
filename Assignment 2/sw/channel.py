
import socket
import random
import time

def injectErrorRandomly(frame):
    if random.randint(0,99)%2 == 0: # 50% chance of error
        pos = random.randint(0, len(frame)-1)
        frame = frame[:pos]+'1'+frame[pos+1:]
        return frame
    else:
        return frame

def waitRandomTime():
    time.sleep(random.randint(0, 2))

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
            print('-'*20)
            a = self.sendconn.recv(1024).decode()
            if a == 'q':
                self.recvconn.send('q'.encode())
                print("Channel: Connection closed")
                break
            print("received from sender: " + a)
            frame = injectErrorRandomly(a[:-2])
            frame = frame + a[-2:]
            self.recvconn.send(frame.encode())
            print("sent to receiver: " + frame)
            a=""
            waitRandomTime()
            b = self.recvconn.recv(1024).decode()
            print("received from receiver: " + b)
            self.sendconn.send(b.encode())
            print("sent to sender: " + b)
            print('-'*20)
            b=""
        

if __name__ == '__main__':
    channel = Channel()
    channel.initSenders()
    channel.initReceivers()
    channel.Medium()
    channel.sendersock.close()
    channel.receiversock.close()
    print("done") 
        

    