import socket
import sys
import pickle
from getpass import getpass
from time import sleep


CWD = './ClientFolder/'


def sendfile(fname, client_socket):
    file = open(CWD+fname, "rb")
    # l = file.read(1024)
    print("Uploading file...")
    d = file.read(1024)
    while d:
        client_socket.send(d)
        d = file.read(1024)
    file.close()
    sleep(1)
    client_socket.send("EOF".encode())
    sleep(1)
    print("File uploaded successfully")


def recvfile(fname, client_socket):
    file = open(CWD+fname, "wb")
    print("Downloading file...")
    while True:
        data = client_socket.recv(1024)
        if data == b"EOF" : 
            file.close()
            break
        else: file.write(data)
    print("File downloaded successfully")


def main():
    if len(sys.argv) == 3:
        hostname = sys.argv[1]
        port = int(sys.argv[2])
    else:
        print("Server IP and PORT NO. required as arguments")
        sys.exit(2)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.5', 5000))
    s.connect((hostname, port))

    username = input("username: ")
    passwd = getpass()

    s.sendall(pickle.dumps([username, passwd]))

    isAuth = s.recv(1024).decode()

    if isAuth == "SUCCESS":
        print("Authenticataion successful")
    else:
        print("Authentication failed")
        s.close()
        return
    print("Type 'help' for list of commands, Type 'exit' to exit")
    while True:
        print("ftp> ", end="")
        cmd = input()
        if cmd == 'exit':
            s.close()
            return
        elif cmd == 'help':
            print("ls - list files in current directory")
            print("pwd - print current directory")
            print("cd - change directory")
            print("get - download file from server")
            print("put - upload file to server")
            print("mget - download multiple files from server")
            print("mput - upload multiple files to server")
            print("del - delete file from server")
            print("exit - exit the program")
            continue
        elif cmd.startswith('ls'):
            cmd = cmd.split(" ")
            cmd[0] = "dir"
            cmd = " ".join(cmd)
            s.sendall(cmd.encode())
            sleep(0.1)
            response = s.recv(1024).decode()
            print(response)
        elif cmd == 'pwd':
            cmd = 'cd'
            s.sendall(cmd.encode())
            sleep(0.1)
            response = s.recv(1024).decode()
            print(response)
        elif cmd.startswith('cd'):
            s.sendall(cmd.encode())
            sleep(0.1)
            response = s.recv(1024).decode()
            print(response)
        elif cmd.startswith('get'):
            s.sendall(cmd.encode())
            fname = cmd.split(" ")[1]
            sleep(0.1)
            recvfile(fname, s)
        elif cmd.startswith('put'):
            fname = cmd.split(" ")[1]
            s.sendall(cmd.encode())
            sendfile(fname, s)
        elif cmd.startswith('mget'):
            fnames = cmd.split(" ")[1:]
            s.sendall(cmd.encode())
            for fname in fnames:
                recvfile(fname, s)
            print("Files downloaded successfully")
        elif cmd.startswith('mput'):
            fnames = cmd.split(" ")[1:]
            s.sendall(cmd.encode())
            for fname in fnames:
                sendfile(fname, s)
            print("Files uplaoded successfully")
        elif cmd.startswith('del'):
            s.sendall(cmd.encode())
            sleep(0.1)
            response = s.recv(1024).decode()
            print(response)
        else :
            print("Invalid command")
            continue


if __name__ == '__main__':
    main()
