import socket
import subprocess
import csv
import pickle
from time import sleep

CWD = './ServerFolder/'


def check_output(command):
    data = subprocess.run(command, shell=True, capture_output=True, cwd=CWD)
    if data.returncode == 0:
        return data.stdout.decode('utf-8')
    else:
        return data.stderr.decode('utf-8')


class Server():
    def __init__(self, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = '127.0.0.2'
        self.port = 53
        self.allowed_users = self.load_users()
        self.folder = CWD

    def load_users(self):
        users_file = open("users.txt", "r")
        users = []
        csv_file = csv.DictReader(users_file, delimiter=",")
        for user in csv_file:
            users.append(user)
        print(users)
        return users

    def sendfile(self, fname, client_socket):
        
        file = open(CWD+fname, "rb")
        if file == None:
            client_socket.sendall("FAILURE".encode())
            return
        d = file.read(1024)
        while d:
            client_socket.send(d)
            d = file.read(1024)
        file.close()
        sleep(1)
        client_socket.send("EOF".encode())
        sleep(1)

    def recvfile(self, fname, client_socket):
        file = open(CWD+fname, "wb")
        while True:
            data = client_socket.recv(1024)
            if data == b"EOF" : 
                file.close()
                break
            else: file.write(data)

    def auth_user(self, name=None, password=None):
        if name == None or password == None:
            return False
        for user in self.allowed_users:
            if name == user["name"] and user["passwd"] == password:
                return True
        return False

    def startServer(self):
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)
        print("Server is listening on {}:{}".format(self.ip, self.port))

        client_socket, client_addr = self.server_socket.accept()
        print("Connected with {}:{}".format(client_addr[0], client_addr[1]))

        credentials = client_socket.recv(1024)
        credentials = pickle.loads(credentials)
        username = credentials[0]
        passwd = credentials[1]

        isCorrect = self.auth_user(username, passwd)

        if isCorrect:
            print("User {} is authenticated".format(username))
            client_socket.sendall("SUCCESS".encode())
        else:
            print("User {} is not authenticated".format(username))
            client_socket.sendall("FAILURE".encode())
            client_socket.close()
            return

        while True:
            cmd = client_socket.recv(1024).decode()

            if cmd.startswith("dir"):
                response = check_output(cmd)
                client_socket.sendall(response.encode())
            elif cmd.startswith("cd"):
                global CWD
                if cmd == "cd":
                    response = check_output(cmd)
                    client_socket.sendall(response.encode())
                elif cmd == "cd ..":
                    CWD = CWD[:CWD.rfind("/", 0, len(CWD)-1)+1]
                    client_socket.sendall("SUCCESS".encode())
                else:
                    CWD += cmd.split(" ")[1]
                    CWD += "/"
                    client_socket.sendall("SUCCESS".encode())

            elif cmd.startswith("get"):
                fname = cmd.split(" ")[1]
                self.sendfile(fname, client_socket)
            elif cmd.startswith("put"):
                fname = cmd.split(" ")[1]
                sleep(0.1)
                self.recvfile(fname, client_socket)
            elif cmd.startswith("mget"):
                fnames = cmd.split(" ")[1:]
                for fname in fnames:
                    self.sendfile(fname, client_socket)
                print("Files sent")
            elif cmd.startswith("mput"):
                fnames = cmd.split(" ")[1:]
                for fname in fnames:
                    self.recvfile(fname, client_socket)
            elif cmd.startswith("del"):
                response = check_output(cmd)
                client_socket.sendall(response.encode())


if __name__ == '__main__':
    server = Server(53)
    server.startServer()
