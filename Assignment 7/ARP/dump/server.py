import socket
import time

query_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
query_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:
    query_sock.sendto(b"hello hello hello how low", ('<broadcast>', 12345))
    time.sleep(2)