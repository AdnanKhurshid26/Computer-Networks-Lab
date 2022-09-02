import time
import socket
import threading



timeout=2

def CountOnes(input):
    noOfOnes = 0

    for i in input:
        if i == '1':
            noOfOnes += 1
  
    return noOfOnes


class Sender():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8080
        self.mysocket = socket.socket()
        self.mysocket.connect((self.host, self.port))
        self.ackRecv = threading.Event()
        self.ackRecv.clear()
        
        self.data = ['10100011']
        self.frameInd = 0
        self.Sn=0;
        self.timeout=2
    
    def startProcess(self):
        self.sendThread = threading.Thread(target=self.send)
        self.recvAckThread = threading.Thread(target=self.recvAck)
        self.sendThread.start()
        self.recvAckThread.start()
        
    def send(self):
        while self.frameInd<len(self.data):
            frame = self.data[self.frameInd]
            if CountOnes(frame)%2 == 0:
                frame = frame+'0'
            else:
                frame = frame+'1'
            
            frame = frame + str((self.Sn)%2)
            time.sleep(0.1)
            self.mysocket.send(frame.encode())
            self.ackRecv.clear()
            isNotified = self.ackRecv.wait(timeout=self.timeout)
            if not isNotified:
                print("Timeout")
                print("Resending frame")
    
    def recvAck(self):
        while True:
            flag = self.mysocket.recv(1024).decode()
            self.ackRecv.set()
            if flag[0] == '1':
                print("Ack received")
                if self.Sn == int(flag[1]):
                    self.frameInd += 1
                    self.Sn+=1;
                else:
                    print("Wrong ACK received")
                    self.frameInd += 1
                    self.Sn+=1;
            else:
                print("NACK received")
                print("Resending frame")
            
sender = Sender()
input = input("press enter to start")
sender.startProcess()