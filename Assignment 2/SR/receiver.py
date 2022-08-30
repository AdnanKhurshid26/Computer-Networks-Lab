import socket
import time
import random


def waitRandomtime():
    x = random.randint(0, 5)
    if x <= 1:
        time.sleep(2)


def checkError(frame):
    countOnes = 0
    for ch in frame:
        if ch == '1':
            countOnes += 1
    return countOnes % 2


def extractMessage(frame, sn):
    msgend = len(frame) - len(sn)
    return frame[:msgend]


def getCount(frame, window):

    b = format(window, "b")

    return frame[-len(b):]


def Main():
    print('Initiating Receiver')
    host = '127.0.0.2'
    port = 9090

    mySocket = socket.socket()
    mySocket.connect((host, port))

    while True:
        print()
        data = mySocket.recv(1024).decode()
        msg = str(data)
        if not msg:
            break
        if msg == 'q0':
            break

        print('Received from channel :', str(data))
        waitRandomtime()
        if checkError(msg) == 0:
            rdata = 'ACK'
        else:
            rdata = 'NAK'

        print('Sending to channel :', str(rdata))
        mySocket.send(rdata.encode())

    mySocket.close()


if __name__ == '__main__':
    Main()
