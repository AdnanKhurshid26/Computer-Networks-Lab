from operator import le
import socket
import sys
def createFrame(data):
	countOnes = 0
	for ch in data:
		if ch == '1':
			countOnes += 1
	data += str(countOnes%2)
	return data

def extractMessage(frame,sn):
	msgend = len(frame) - len(sn)
	return frame[:msgend]
	
def extractCount(frame):
	startidx = -1
	endidx = -1
	for i in range(len(frame)-1):
		if frame[i] == '/':
			if startidx == -1:
				startidx = i+1
			else:
				endidx = i
	cnt = frame[startidx:endidx]
	return int(cnt)
	
	
def Main():
	count = 0
	sentframes = []
	print('Initiating Sender')
	host = '127.0.0.1'
	port = 8080
	
	mySocket = socket.socket()
	mySocket.connect((host, port))
	
	while True:
		print()
		data = input("Enter data to send, enter q to quit: ")
		data = createFrame(data)
		print('Sending to channel :',str(data))
		mySocket.send(data.encode())
		sentframes.append(data)
		count += 1
		
		if not data:
			break
		if data == 'q0':
			break
	
	mySocket.close()
	
if __name__ == '__main__':
	Main()
	
		