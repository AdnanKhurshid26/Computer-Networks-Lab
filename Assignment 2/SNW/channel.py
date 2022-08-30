import socket
import time

import random
import os 

def injectRandomError(frame):
	pos = random.randint(0, len(frame)-1)
	frame = frame[:pos]+'1'+frame[pos+1:]
	return frame
	
class Channel():
	
	def __init__(self):
		self.totalsender = 1
		self.senderhost = '127.0.0.1'
		self.senderport = 8080
		self.senderconn = []
		
		self.totalreceiver = 1
		self.receiverhost = '127.0.0.2'
		self.receiverport = 1234
		self.receiverconn = []
		
	def initSenders(self):
		senderSocket = socket.socket()
		senderSocket.bind((self.senderhost, self.senderport))
		senderSocket.listen(self.totalsender)
		for i in range(1, self.totalsender+1):
			conn = senderSocket.accept()
			self.senderconn.append(conn)
		print('Initiated sender connection')
		
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
		print('Initiated receiver connection')
		
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
				if not data:
					break
				if data == 'q0':
					break
				
				print('Received from Sender:',str(data))
				
				recvno = random.randint(0,len(self.receiverconn)-1) 
				print('Sending to Receiver')
				rconn = self.receiverconn[recvno]
				data = injectRandomError(data)
				rconn[0].sendto(data.encode(), rconn[1])
				
				
				rdata = rconn[0].recv(1024).decode()
				print('Received from Receiver:', str(rdata))
				
				print('Sending to Sender')
				conn[0].send(rdata.encode())
				
			
				while rdata=="TIMEOUT":
					print()
					data = conn[0].recv(1024).decode()
					print('Again Received from Sender:',str(data))
					data = injectRandomError(data)
					print('Again Sending to Receiver')
					rconn[0].sendto(data.encode(), rconn[1])
					rdata = rconn[0].recv(1024).decode()
					print('Again Received from Receiver:', str(rdata))
					print('Again Sending to Sender')
					conn[0].send(rdata.encode())
			
					
				
				
			if data == 'q0':
				break
		return

if __name__ == '__main__':
	#Main()
	ch = Channel()
	ch.initSenders()
	ch.initReceivers()
	ch.processData()
	ch.closeSenders()
	ch.closeReceivers()		
