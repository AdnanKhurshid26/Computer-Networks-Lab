import socket

def senseCarrier():
    f=open("busy.txt","r")
    status = int(f.read())
    return status

class Sender():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8080
        self.mysocket = socket.socket()
        self.mysocket.connect((self.host, self.port))


        self.data = ['10100011', '10010011', '10100101',
                     '10110000', '10110001', '10010101', '00110011', '00110000',
        '00110010', '00110011', '00110100', '00110101', '00110110', '00110111', '00111000', '00111001', '00111010', '00111011',]

    def send(self):
        for i in range(0, len(self.data)):
            while senseCarrier() == 1:
                print("CHANNEL BUSY, SENSING CHANNEL AGAIN")
            print("CHANNEL IS IDLE NOW, SENDING FRAME")
            frame = self.data[i]
            self.mysocket.send(frame.encode())



sender = Sender()
inputt = input("press enter to start")
sender.send()


