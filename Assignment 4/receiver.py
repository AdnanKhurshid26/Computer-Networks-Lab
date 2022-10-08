from helper import *
import socket
import json

sock = socket.socket()
sock.connect(('127.0.0.1',8080))

n = int(sock.recv(1024).decode())

N = getNextPowerof2(n)

print("Generating walsh table...")

walshtable = None

if(N==1):
    walshtable = [[1]]
else:
    walshtable = [[0 for i in range(N)] for j in range(N)]
    buildWalshTable(walshtable, N, 0, N - 1, 0, N - 1, False)

print("Walsh Table Generated")

for i in walshtable:
    print(i)

print("\n")

data = sock.recv(4096)
res = json.loads(data.decode())


decoded_words = []

for i in range(n):
    decoded_words.append("")
    
for i in range(len(res)):
    for j in range(n):
        sum =0
        for k in range(N):
           sum += res[i][k]*walshtable[j][k]
        x = sum//N
        
        if x == 1:
            decoded_words[j] += "1"
        elif x == -1:
            decoded_words[j] += "0"
        else:
            pass
        

for i in range(n):
    print(f"Station {i+1}:-  {BinaryToStr(decoded_words[i])}")
    

    
