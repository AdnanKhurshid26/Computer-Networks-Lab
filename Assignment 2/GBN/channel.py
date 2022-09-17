import socket
import threading
import random
import time
from sys import exit

server = socket.socket()
port = 12352
server.bind(('localhost',port))
server.listen(5)
connection = True

def inject_error(msg):
    x = random.randint(0,9)
    if(x<=3):
        ch = msg[0:1]
        if ch == '1':
            ch='0'
        else:
            ch='1'
        msg = ch + msg[1::]
    
    return msg


def handle_connection(sender,reciever,width):

    print("*"*15)
    while True:
        lst = []
        # Getting from Sender
        i=0
        while i<width:
            msg = sender.recv(1024).decode()
            time.sleep(0.5)
            if msg == "exit":
                sender.close()
                reciever.close()
                server.close()
                exit()
            print(f"Recieved {msg} from sender")
            lst.append(msg)
            i=i+1
        
        print("\nAll frames recieved\n")

        # Sending all to reciever
        for data in lst:
            msg = data.split(":")[0]
            ind = data.split(":")[1]
            msg = inject_error(msg)
            data = f"{msg}:{ind}"
            reciever.sendall(data.encode())
            time.sleep(1)
            print(f"{data} is sent to reciever")

        print("\nAll frames Sent to receiver\n")

        lst = []
        i=0
        # Getting from Reciever
        while i<width:
            msg = reciever.recv(1024).decode()
            time.sleep(0.5)
            print(f"{msg} recived from receiver")
            lst.append(msg)
            i=i+1

        print("\nAll ack recieved\n")
            
        # Sending acknowledgement to Sender
        for msg in lst:
            print(f"{msg} sent to sender")
            sender.sendall(msg.encode())
            time.sleep(1)

        print("\nAll message recieved")
        print("*"*15)
    



while connection:
    c,caddr = server.accept()
    print ('Sender Connected' )
    r,raddr = server.accept()
    print ('Reciever Connected' )
    width = int(c.recv(1024).decode())
    time.sleep(0.5)
    r.sendall(f"{width}".encode())

    thread = threading.Thread(target=handle_connection,args=(c,r,width))
    thread.start()


server.close()