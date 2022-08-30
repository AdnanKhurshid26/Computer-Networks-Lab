import socket
import time
import random


def injectRandomError(frame):
    pos = random.randint(0, len(frame)-1)
    frame = frame[:pos]+'1'+frame[pos+1:]
    return frame


def extractMessage(frame, sn):
    msgend = len(frame) - len(sn)
    return frame[:msgend]


def getCount(frame, window):
    b = format(window, "b")
    return frame[-len(b):]


class Channel():

    def __init__(self, windowsize):
        self.totalsender = 1
        self.senderhost = '127.0.0.1'
        self.senderport = 8080
        self.senderconn = []

        self.totalreceiver = 1
        self.receiverhost = '127.0.0.2'
        self.receiverport = 9090
        self.receiverconn = []

        self.windowsize = windowsize
        self.slidingwindow = []
        self.status = []
        self.currentcount = 0

    def initSenders(self):
        senderSocket = socket.socket()
        senderSocket.bind((self.senderhost, self.senderport))
        senderSocket.listen(self.totalsender)
        for i in range(1, self.totalsender+1):
            conn = senderSocket.accept()
            self.senderconn.append(conn)
        print('Started sender connection')

    def closeSenders(self):
        for conn in self.senderconn:
            conn[0].close()
        print('Closed sender connection')

    def initReceivers(self):
        receiverSocket = socket.socket()
        receiverSocket.bind((self.receiverhost, self.receiverport))
        receiverSocket.listen(self.totalreceiver)
        for i in range(1, self.totalreceiver+1):
            conn = receiverSocket.accept()
            self.receiverconn.append(conn)
        print('Started receiver connection')

    def closeReceivers(self):
        for conn in self.receiverconn:
            conn[0].close()
        print('Closed receiver connection')

    def processData(self):
        while True:
            for i in range(len(self.senderconn)):
                print()

                conn = self.senderconn[i]
                data = conn[0].recv(1024).decode()
                prevtime = time.time()
                data = str(data)
                sn = format((self.currentcount % windowsize), "b").zfill(
                    len(format(self.windowsize, "b")))
                origmsg = data
                if not origmsg:
                    break
                if origmsg == 'q0':
                    break
                print('Received from Sender:', str(data))

                recvno = random.randint(0, len(self.receiverconn)-1)
                print('Sending to Receiver')
                rconn = self.receiverconn[recvno]
                # cnt = getCount(data,self.windowsize)
                msg = injectRandomError(origmsg)
                newdata = msg
                self.slidingwindow.append([origmsg, sn])
                rconn[0].sendto(newdata.encode(), rconn[1])

                # received from receiver
                rdata = rconn[0].recv(1024).decode()
                rdata = str(rdata)
                time.sleep(0.5)
                curtime = time.time()
                if curtime-prevtime > 2 or rdata == "NAK":

                    self.status.append(-1)
                else:
                    self.status.append(0)

                roundtime = curtime-prevtime
                print('DATA\tSn\tSTATUS')
                if roundtime > 2:
                    print(msg, sn, "TIMEOUT")
                else:
                    print(msg, sn, rdata)
                print('Round trip time: ', str(curtime-prevtime))
                print('Current frame no:', str(
                    (self.currentcount % windowsize)+1))
                if (self.currentcount % windowsize)+1 == self.windowsize:
                    idx = 0
                    

                    while sum(self.status) != 0:
                        
                        
                            for i in range(len(self.status)):
                                if self.status[i] == -1:
                                    idx = i
                                    while self.status[idx] !=0 :
                                         print()
                                         print(15*'-')
                                         print('Resending Frame No :', str(idx+1))
                                         prevtime = time.time()
                                         prevdata = self.slidingwindow[idx][0]
                                         cnt = self.slidingwindow[idx][1]
                                         msg = injectRandomError(prevdata)
                                         data = msg
                                         rconn[0].sendto(data.encode(), rconn[1])
                                         
                                         rdata = rconn[0].recv(1024).decode()
                                         rdata = str(rdata)
                                         if rdata == "NAK" or curtime-prevtime > 2:
                                             self.status[idx] = -1
                                         else:
                                             self.status[idx] = 0
                                         curtime = time.time()
                                         roundtime = curtime-prevtime
                                         print('DATA\t\t Sn\t\tSTATUS')
                                         if roundtime > 2:
                                             print(msg, cnt, "TIMEOUT")
                                         else:
                                             print(msg,cnt, rdata)
                                         print('Round trip time: ', str(curtime-prevtime))
                                         print(15*'-')
                
                    print('--------Block of size ',self.windowsize, 'successfully sent----------')
                            
                            
                                
                            
                                
                            
                                
                            
                                
                                         
                                         
                            			 
                                         

                           
                            
                        
				
                self.currentcount += 1
            if origmsg == 'q0':
                break
        return


if __name__ == '__main__':
    windowsize = int(input('Enter window size: '))

    ch = Channel(windowsize)
    ch.initSenders()
    ch.initReceivers()
    ch.processData()
    ch.closeSenders()
    ch.closeReceivers()
