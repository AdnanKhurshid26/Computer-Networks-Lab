import socket
import threading
import time


def CountOnes(input):
    noOfOnes = 0

    for i in input:
        if i == '1':
            noOfOnes += 1
        
    return (int)(noOfOnes % 2 == 0)


class Receiver():
    def __init__(self):
        self.host = '127.0.0.2'
        self.port = 9090
        self.mysocket = socket.socket()
        self.mysocket.connect((self.host, self.port))
        self.ack = None
        self.Rn = 0


    def receiver(self):
        while True:
            data = self.mysocket.recv(1024).decode()
            Sn = int(data[-1])
            frame = data[:-1]
            notCorrupt = CountOnes(frame)

            if notCorrupt:
                if self.Rn == Sn:
                    print("Frame received : " + frame[:-1])
                    self.ack = '1'
                    self.sendAck()
                else:
                    print("Duplicate frame received and discarded")
                    self.ack = '1'
                    self.sendAck()
            else:
                print("Frame received is corrupted")
                self.ack = '0'
                self.sendAck()

    def sendAck(self):
        if (self.ack == '1'):
            reply = '1'+str(self.Rn)
            self.mysocket.send(reply.encode())
            self.Rn = (self.Rn+1) % 2
        else:
            reply = '0'+str(self.Rn)
            self.mysocket.send(reply.encode())


receiver = Receiver()
receiver.receiver()
