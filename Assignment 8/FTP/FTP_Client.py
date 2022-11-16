import socket
import os
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 4454
ADDR = (IP, PORT)
FORMAT = "utf-8"
HEADERSIZE = 10
N = 0

def receive_message(client_socket):
    try:
        msg_header = client_socket.recv(HEADERSIZE)

        if not len(msg_header):
            return False
        msg_len = int(msg_header.decode(FORMAT).strip())
        data = client_socket.recv(msg_len).decode(FORMAT)
        return data
    except:
        return False

def createFrame(message):
    return  f"{len(message):<{HEADERSIZE}}" + message

def clientStart(client):
    while True:
        choice = input("Enter Choice : ")
        if choice == "exit":
            client.close()
            break
        if choice == "UPLOAD":
            file = input("Enter name of the file : ")
            if not os.path.isfile(file):
                print("Invalid File Name\n")
                continue
            fp = open(file,'r')
            message = fp.read()
            print("UPLOADING FILE ..... ")
            time.sleep(2)
            client.send(createFrame("$"+message).encode(FORMAT))
        else:
            client.send(createFrame("LIST").encode(FORMAT))
            res = receive_message(client)
            if not res:
                client.close()
                break
            print("Files in the Server :- \n" + res + "\n")
            if choice == "DOWNLOAD" : 
                fi = input("Enter File to Download : ")
                print("DOWNLOADING FILE ..... ")
                time.sleep(2)
                client.send(createFrame(fi).encode(FORMAT))
                res = receive_message(client)
                if not res:
                    client.close()
                    break
                if res[0] == "$":
                    print(res)
                else:
                    global N
                    N += 1
                    FILENAME = f"ClientFile{N}.txt"
                    print(f"File Downloaded from Server , Saved as {FILENAME}\n")
                    with open(FILENAME, 'w') as f:
                        f.write(res)

if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    clientStart(client)