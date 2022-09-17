import time
import socket
import threading


timeout = 2


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
        self.e1 = threading.Event()
        self.e1.clear()
        self.e2 = threading.Event()
        self.e2.clear()
        self.e3 = threading.Event()
        self.e3.clear()

        self.data = ['10100011', '10010011', '10100101',
                     '10110000', '10110001', '10010101', '00110011', '00110000',
        '00110010', '00110011', '00110100', '00110101', '00110110', '00110111', '00111000', '00111001', '00111010', '00111011',]
        self.frameInd = 0
        self.Sn = 0
        self.timeout = 2

    def startProcess(self):
        self.sendThread = threading.Thread(target=self.send)
        self.recvAckThread = threading.Thread(target=self.recvAck)
        self.sendThread.start()
        self.recvAckThread.start()

    def send(self):
        while self.frameInd < len(self.data):
            self.e2.clear()
            frame = self.data[self.frameInd]
            if CountOnes(frame) % 2 == 0:
                frame = frame+'0'
            else:
                frame = frame+'1'

            frame = frame + str((self.Sn))
            time.sleep(0.1)
            self.mysocket.send(frame.encode())
            print('-'*15)
            print("sent to channel: " + frame)
            self.ackRecv.clear()
            self.e1.set()
            isNotified = self.ackRecv.wait(timeout=self.timeout)
            if not isNotified:
                print("Timeout")
                print("Resending frame")
                time.sleep(0.5)
                self.e2.set()

            self.e2.wait()

        self.mysocket.send('q'.encode())

    def recvAck(self):
        while True:
            self.e1.wait()
            flag = self.mysocket.recv(1024).decode()
            print("received from channel: " + flag)
            self.ackRecv.set()
            if flag[0] == '1':
                if self.Sn == int(flag[1]):

                    print("Ack received")
                    self.frameInd += 1
                    self.Sn = 1-self.Sn
                else:
                    print("Wrong ACK received. Discarded")
                    # self.frameInd += 1
                    # self.Sn = 1-self.Sn
                    
            else:
                print("NACK received")
                print("Resending frame")
            self.e1.clear()
            self.e2.set()


sender = Sender()
input = input("press enter to start")
sender.startProcess()
