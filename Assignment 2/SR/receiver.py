import socket
import time
import random

def VRC(val):
    odd = 0
    for i in val:
        if(i=='1'):
            odd+=1
        
    return str(odd%2)+val


reciever = socket.socket()
port = 12359
reciever.connect(('localhost',port))

window_size = int(reciever.recv(1024).decode())
time.sleep(1)

while True:
    print("*"*15)
    lst =[]
    i=0
    # Getting From Server
    while i<window_size:
        data = reciever.recv(1024).decode()
        time.sleep(0.5)
        print(f"Recived {data}")
        msg = data.split(":")[0]
        index = data.split(":")[1]
        if msg == VRC(msg[1::]):
            lst.append(f"ACK:{index}")
        else:
            lst.append(f"NACK:{index}")
        i=i+1

    print("\nAll frames Recived\n")

    # Sending to Server
    for msg in lst:
        print(f"Sending {msg}")
        reciever.sendall(msg.encode())
        time.sleep(1)
    print("\nAll acks sent")
    print("*"*15)

