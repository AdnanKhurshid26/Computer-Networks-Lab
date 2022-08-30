import socket
import sys
import time
import random

def waitRandomTime():
	x = random.randint(0,5)
	if x <= 1:
		time.sleep(2)
		
def checkError(frame):
	countOnes = 0
	for ch in frame:
		if ch == '1':
			countOnes += 1
	return countOnes%2
		
def Main():
	print('Initiating Receiver')
	host = '127.0.0.2'
	port = 1234
	
	mySocket = socket.socket()
	mySocket.connect((host, port))
	
	while True:
		print()
		data = mySocket.recv(1024).decode()
		if not data:
			break
		if data == 'q0':
			break
		
		print('Received from channel :', str(data))
		
		if checkError(data) == 0:
			rdata = 'ACK'
		else:
			time.sleep(2)
			rdata = 'TIMEOUT'
		
		print('Sending to channel :',str(rdata))
		mySocket.send(rdata.encode())
		
		
		
	mySocket.close()
	
if __name__ == '__main__':
	
	Main()
	
		