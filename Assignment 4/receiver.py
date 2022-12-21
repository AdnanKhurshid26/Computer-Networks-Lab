from helper import *
import socket
import json

sock = socket.socket()
sock.bind(('127.0.0.12', 8080))
sock.connect(('127.0.0.4', 8080))

# receiving the number of stations from the sender
n = int(sock.recv(1024).decode())

N = getNextPowerof2(n)

walshtable = None

if (N == 1):
    walshtable = [[1]]
else:
    walshtable = [[0 for i in range(N)] for j in range(N)]
    buildWalshTable(walshtable, N, 0, N - 1, 0, N - 1, False)

print("\nWalsh Table Generated")

for i in walshtable:
    print(i)

print("\n")

data = sock.recv(4096)
data = json.loads(data.decode())


decoded = []

# initilaizing the list of messages with n empty strings
for i in range(n):
    decoded.append("")

for i in range(len(data)):
    for j in range(n):
        sum = 0
        for k in range(N):
            sum += data[i][k]*walshtable[j][k]
        x = sum//N

        if x == 1:
            decoded[j] += "1"
        elif x == -1:
            decoded[j] += "0"
        else:
            # if we get 0 then it means the station is silent
            pass


for i in range(n):
    print(f"Station {i+1}:-  {BinaryToStr(decoded[i])}")
