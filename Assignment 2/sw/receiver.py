import socket
import threading
import time
import random


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
        with open('output.txt', "w") as op:
            while True:
                data = self.mysocket.recv(1024).decode()
                print('-'*15)
                if (data == 'q'):
                    print("Receiver: Connection closed")
                    exit()
                print("received from channel: " + data)
                Sn = int(data[-1])
                frame = data[:-1]
                notCorrupt = CountOnes(frame)

                if notCorrupt:
                    if self.Rn == Sn:

                        print("Frame received : " + frame[:-1])
                        self.ack = '1'
                        self.sendAck()
                        op.write(frame[:-1] + '\n')
                        data = ""
                        frame = ""
                    else:
                        # print('-'*15)
                        print("Duplicate frame received and discarded")
                        self.ack = '1'
                        self.sendAck()
                        data = ""
                        frame = ""
                else:
                    print("Frame received is corrupted")
                    self.ack = '0'
                    self.sendAck()
                    data = ""
                    frame = ""

    def sendAck(self):
        if (self.ack == '1'):
            reply = '1'+str(self.Rn)
            self.mysocket.send(reply.encode())
            print("sent to channel: " + reply)
            self.Rn = 1-self.Rn
        else:
            reply = '0'+str(self.Rn)
            self.mysocket.send(reply.encode())
            print("sent to channel: " + reply)


receiver = Receiver()
receiver.receiver()

