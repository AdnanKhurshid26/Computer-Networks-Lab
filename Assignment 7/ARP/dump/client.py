import socket
import time

#creat udp socket

clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

clientsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
# clientsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
clientsock.bind(('', 12345))

while True:
    data, addr = clientsock.recvfrom(1024)

    print(data.decode())
    time.sleep(1)