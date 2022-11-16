#python stelnet.py 

from socket import *
import ftplib
from ftplib import FTP
import os
import stat
import sys
import shutil
import requests
import subprocess
import httplib2

serverName = "localhost"
serverPort = 10100
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

ftp = FTP(serverName)

ftp.login("seed","dees")

print ('The server is ready to receive')
while 1:
	connectionSocket, addr = serverSocket.accept()
	input1 = connectionSocket.recv(1024).decode()
	if (input1 == "ls"):
		output = ftp.nlst()
		print(output)
		output1 = "Contents Listed"
		connectionSocket.send(output1.encode())

	elif (input1 == "ls -la"): 
		output = ftp.retrlines('LIST')
		print(output)
		connectionSocket.send(output.encode())

	elif(input1== "pwd"):
		currentDirectory = os.getcwd()
		print(currentDirectory)
		connectionSocket.send(currentDirectory.encode())

	elif(input1.startswith('mkdir')):
		# Directory 
		print("input",input1[6:])
		directory = input1[6:]

		# Parent Directory path 
		parent_dir = "/home/seed/Networks_Project"
  
		# Path 
		path = os.path.join(parent_dir, directory) 
  
		# Create the directory 
		os.mkdir(path) 
		print("Directory '%s' created" %directory) 
		connectionSocket.send(directory.encode())

	elif(input1.startswith('rmdir')):
		# Directory name 
		print("input",input1[6:])
		directory = input1[6:]

		# Parent Directory 
		parent = "/home/seed/Networks_Project"
  
		# Path 
		path = os.path.join(parent, directory) 
  
		# Remove the Directory 
		os.rmdir(path) 
		print("Directory '%s' has been removed successfully" %directory) 
		connectionSocket.send(directory.encode())

	elif(input1.startswith('cd')):
		print("input",input1[3:])
		output = os.chdir(input1[3:])
		output1 = "Directory Changed"
		connectionSocket.send(output1.encode())

	elif(input1.startswith('cat')):	
		print("input", input1[4:])
		with open(input1[4:], 'r') as f:
    			contents = f.read()
		print(contents)
		connectionSocket.send(contents.encode())

	elif(input1.startswith('rm')):
		print("input", input1[3:])
		os.remove(input1[3:])
		output = "File Successfully Removed"
		print(output)
		connectionSocket.send(output.encode())	
		
	elif(input1.startswith('mv1')):
		print("input",input1[4:])
		st = input1[4:]
		print("st",st)
		m = st.index(" ")
		source = st[:m]
		n = st[m:]
		print("source",source)
		destination = n[1:]
		print("destination",destination)
		os.rename(source,destination)
		output = "File Successfully Moved"
		print(output)
		connectionSocket.send(output.encode())


	elif(input1.startswith('mv2')):
		print("input",input1[4:])
		st = input1[4:]
		print("st",st)
		m = st.index(" ")
		source = st[:m]
		n = st[m:]
		print("source",source)
		destination = n[1:]
		print("destination",destination)
		shutil.move(source,destination)
		output = "File Successfully Moved"
		print(output)
		connectionSocket.send(output.encode())

	elif(input1 == "cd .."):
		output = os.chdir('..')	
		output = "Directory Changed"
		connectionSocket.send(output.encode())

	
	elif(input1.startswith('echo')):
		print(input1[5:])
		st = input1[5:]
		print("st",st)
		m = st.index(">")
		text = st[:m]
		n = st[m:]
		print("text",text) #text
		print("n",n)
		filename = n[2:]
		print("filename",filename) #file
        with open(filename, 'w') as f:
            f.write(text)
            f.close()
		with open(filename, "w") as f:
   			f.write(text)
			f.close()
		output = "Echoed Successfully onto the text file"
		print(output)
		connectionSocket.send(output.encode())
		
	elif(input1.startswith("GET /HTTP/")):
		http = httplib2.Http()
		contents = http.request("http://localhost")[1]
		print(contents)
		connectionSocket.send(contents)

	elif(input1.startswith("HEAD /HTTP")):
		http = httplib2.Http()
		resp = http.request("http://localhost","HEAD")[0]
		print(resp)
		output = "Response Received"
		connectionSocket.send(output.encode())

	elif(input1 == "GET /home/seed/Networks_Project/abc.txt"):
		try:		
			receive = requests.get("http://localhost")
			with open("/home/seed/Networks_Project/abc.txt", "r") as f:
				f.write(receive.content)
				print(receive.content)
				connectionSocket.send(receive.content)
		except Exception as e:
			template = "An exception of type {0} occured. Arguments:\n{1!r}"
			message = template.format(type(e).__name__, e.args)
			print(message)
			connectionSocket.send(message.encode('utf-8'))

	op = subprocess.Popen(str(input1), shell=True, stderr=subprocess.PIPE,stdout=subprocess.PIPE)
	p1 = op.stdout.read()
	connectionSocket.sendall(p1)
		
connectionSocket.close() 