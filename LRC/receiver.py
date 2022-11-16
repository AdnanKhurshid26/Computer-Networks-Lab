import socket
from LRC import strTobinary, BinaryToStr,lrcencode, lrcdecode
receiver = socket.socket()
print("Socket successfully created")

receiver.connect(('127.0.0.1',12345))

data = receiver.recv(1024).decode()

output, errorFound = lrcdecode(data, 8)

output = BinaryToStr(output)

print("Received data: ",end="")
print(output)
print("Error Found: ", errorFound)

exit = input("Press any key to exit: ")