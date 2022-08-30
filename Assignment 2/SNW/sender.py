import socket
import sys
import time
def createFrame(data):
	countOnes = 0
	for ch in data:
		if ch == '1':
			countOnes += 1
	data += str(countOnes%2)
	return data
	
def Main(senderno):
	print('Initiating Sender #',senderno)
	host = '127.0.0.1'
	port = 8080
	
	mySocket = socket.socket()
	mySocket.connect((host, port))
	
	while True:
		print()
		data = input("Enter data to send: ")
		prevtime = time.time()
		data = createFrame(data)
		print('Sending to channel :',str(data))
		mySocket.send(data.encode())
		if not data:
			break
		if data == 'q0':
			break
		rdata = mySocket.recv(1024).decode()
		print('Received from channel :',str(rdata))
		curtime = time.time()
		print('Round trip time: ',str(curtime-prevtime))
		if curtime-prevtime > 2:
			timeout = 1
		else:
			timeout = 0
		while timeout==1:
			print()
			prevtime = time.time()
			if timeout == 1:
				print('TIMEOUT of 2s EXPIRED')
			else:
				print('THE FRAME GOT CORRUPTED !!!')
			print('Again Sending to channel :',str(data))
			mySocket.send(data.encode())
			rdata = mySocket.recv(1024).decode()
			print('Again Received from channel :',str(rdata))
			curtime = time.time()
			print('Round trip time:',str(curtime-prevtime),'seconds')
			if curtime-prevtime > 2:
				timeout = 1
			else:
				timeout = 0
	
	mySocket.close()
	
if __name__ == '__main__':
	if len(sys.argv) > 1:
		senderno = int(sys.argv[1])
	else:
		senderno = 1
	Main(senderno)
	
		