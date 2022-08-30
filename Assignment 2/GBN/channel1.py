# import socket
# import time
# import random

# def injectRandomError(frame):
#     pos = random.randint(0, len(frame)-1)
#     frame = frame[:pos]+'1'+frame[pos+1:]
#     return frame



# class Channel():

#     def __init__(self, windowsize):
#         self.totalsender = 1
#         self.senderhost = '127.0.0.1'
#         self.senderport = 8080
#         self.senderconn = []

#         self.totalreceiver = 1
#         self.receiverhost = '127.0.0.2'
#         self.receiverport = 9090
#         self.receiverconn = []

#         self.windowsize = windowsize
#         self.slidingwindow = []
#         self.currentcount = 0
#         #self.statuswindow = []

#     def initSenders(self):
#         senderSocket = socket.socket()
#         senderSocket.bind((self.senderhost, self.senderport))
#         senderSocket.listen(self.totalsender)
#         for i in range(1, self.totalsender+1):
#             conn = senderSocket.accept()
#             self.senderconn.append(conn)
#         print('Started sender connection')

#     def closeSenders(self):
#         for conn in self.senderconn:
#             conn[0].close()
#         print('Closed sender connection')

#     def initReceivers(self):
#         receiverSocket = socket.socket()
#         receiverSocket.bind((self.receiverhost, self.receiverport))
#         receiverSocket.listen(self.totalreceiver)
#         for i in range(1, self.totalreceiver+1):
#             conn = receiverSocket.accept()
#             self.receiverconn.append(conn)
#         print('Started receiver connection')

#     def closeReceivers(self):
#         for conn in self.receiverconn:
#             conn[0].close()
#         print('Closed receiver connection')

#     def processData(self):
#         while True:
#             for i in range(len(self.senderconn)):
#                 print()

#                 conn = self.senderconn[i]
#                 data = conn[0].recv(1024).decode()
#                 prevtime = time.time()
#                 data = str(data)
#                 origmsg = extractData(data)
#                 if not origmsg:
#                     break
#                 if origmsg == 'q0':
#                     break
#                 print('Received from Sender:', str(data))

#                 recvno = random.randint(0, len(self.receiverconn)-1)
#                 print('Sending to Receiver')
#                 rconn = self.receiverconn[recvno]
#                 cnt = getCount(data)
#                 msg = injectRandomError(origmsg)
#                 newdata = msg+ str(cnt) + '/'
#                 rconn[0].sendto(newdata.encode(), rconn[1])

#                 # received from receiver
#                 rdata = rconn[0].recv(1024).decode()
#                 rdata = str(rdata)
#                 time.sleep(0.5)
#                 curtime = time.time()
#                 if curtime-prevtime > 2:
#                     timeout = 1
#                     newdata += 'TIMEOUT'
#                 else:
#                     timeout = 0
#                     newdata += rdata

#                 self.slidingwindow.append([data, newdata, i, recvno])

#                 msg = extractData(newdata)
#                 cnt = getCount(newdata,windowsize)
#                 status = extractStatus(newdata)
#                 print(msg, str(cnt), status)
#                 print('Round trip time: ', str(curtime-prevtime))
#                 print('Current frame no:', str(
#                     (self.currentcount % windowsize)+1))
#                 if (self.currentcount % windowsize)+1 == self.windowsize:
#                     idx = 0
#                     flag = 1

#                     while flag == 1:
#                         idx = 0
#                         flag = 0
#                         while idx < self.windowsize:
#                             currframe = self.slidingwindow[idx][1]
#                             msg = extractData(currframe)
#                             cnt = getCount(currframe)
#                             status = extractStatus(currframe)

#                             if status == 'NAK' or status == 'TIMEOUT':
#                                 flag = 1
#                                 break
#                             idx += 1
#                         print(' ------------------------------ ')
#                         if flag == 1:
#                             print('RESEND FROM FRAME NO:', str(idx+1))
#                         else:
#                             print('BLOCK OF WINDOW SIZE',
#                                   self.windowsize, 'SUCCESSFULLY SENT')
#                         print(' ------------------------------ ')

#                         while flag == 1 and idx < self.windowsize:
#                             print()
#                             prevtime = time.time()
#                             prevframe = self.slidingwindow[idx][0]
#                             currframe = self.slidingwindow[idx][1]
#                             sendno = self.slidingwindow[idx][2]
#                             recvno = self.slidingwindow[idx][3]
#                             conn = self.senderconn[sendno]
#                             rconn = self.receiverconn[recvno]

#                             # sending all frames to its sender from first NAK

#                             print('Current frame no:', str(idx+1))
#                             print('Again Sending to Receiver', recvno+1)

#                             msg = extractData(prevframe)
#                             msg = injectRandomError(msg)
#                             data = msg + '/' + str(cnt) + '/'
#                             rconn[0].sendto(data.encode(), rconn[1])

#                             # receiving ACK or NAK from receiver
#                             rdata = rconn[0].recv(1024).decode()
#                             rdata = str(rdata)
#                             data += rdata

#                             msg = extractData(data)
#                             cnt = getCount(data)
#                             stat = extractStatus(data)
#                             curtime = time.time()
#                             print(msg, str(cnt), stat)
#                             print('Round trip time: ', str(curtime-prevtime))
#                             self.slidingwindow[idx][1] = data
#                             idx += 1

#                 self.currentcount += 1
#             if origmsg == 'q0':
#                 break
#         return


# if __name__ == '__main__':
#     windowsize = int(input('Enter window size: '))

#     ch = Channel(windowsize)
#     ch.initSenders()
#     ch.initReceivers()
#     ch.processData()
#     ch.closeSenders()
#     ch.closeReceivers()
