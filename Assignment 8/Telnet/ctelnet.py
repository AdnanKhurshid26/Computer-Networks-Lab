#python ctelnet.py 127.0.0.1 10100

from socket import *
import sys
from ftplib import FTP

clientsys = sys.argv

if(clientsys < 3) :
		print ('Usage.. : python telnet.py hostname port')
		sys.exit()
serverName = clientsys[1] #127.0.0.1
serverPort = int(clientsys[2]) #10100
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

ftp = FTP(serverName)
ftp.login("seed","dees") 

input1 = input("Enter a command:")

clientSocket.send(input1.encode())
modifiedSentence = clientSocket.recv(1024)
outputF = modifiedSentence.decode()
print ('From Server:', outputF)
clientSocket.close()