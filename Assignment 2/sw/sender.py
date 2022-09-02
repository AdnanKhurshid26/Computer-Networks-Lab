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
        '10110000', '10110001', '10010101', '00110011', '00110000', '00110001', 
        '00110010', '00110011', '00110100', '00110101', '00110110', '00110111', '00111000', '00111001', '00111010', '00111011', '00111100', '00111101', '00111110', '00111111', '01000000', '01000001', '01000010', '01000011', '01000100', '01000101', '01000110', '01000111', '01001000', '01001001', '01001010', '01001011', '01001100', '01001101', '01001110', '01001111', '01010000', '01010001', '01010010', '01010011', '01010100', '01010101', '01010110', '01010111', '01011000', '01011001', '01011010', '01011011', '01011100', '01011101', '01011110', '01011111', '01100000', '01100001', '01100010', '01100011', '01100100', '01100101', '01100110', '01100111', '01101000', '01101001', '01101010', '01101011', '01101100', '01101101', '01101110', '01101111', '01110000', '01110001', '01110010', '01110011', '01110100', '01110101', '01110110', '01110111', '01111000', '01111001', '01111010', '01111011', '01111100', '01111101', '01111110', '01111111', '10000000', '10000001', '10000010', '10000011', '10000100', '10000101', '10000110', '10000111', '10001000', '10001001', '10001010', '10001011', '10001100', '10001101', '10001110', '10001111', '10010000', '10010001', '10010010', '10010011',]
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
                print('-'*15)
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
                    print("Wrong ACK received")
                    self.frameInd += 1
                    self.Sn = 1-self.Sn
            else:
                print("NACK received")
                print("Resending frame")
            self.e1.clear()
            self.e2.set()


sender = Sender()
input = input("press enter to start")
sender.startProcess()
