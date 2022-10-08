from helper import *
import socket
import json


sock = socket.socket()
sock.bind(('127.0.0.1', 8080))
sock.listen(1)

conn, addr = sock.accept()

n = int(input("Enter the number of stations:  "))

N = getNextPowerof2(n)

conn.send(str(n).encode())

print("Generating walsh table...")

walshtable = None

if (n == 1):
    walshtable = [[1]]
else:
    walshtable = [[0 for i in range(N)] for j in range(N)]
    buildWalshTable(walshtable, N, 0, N - 1, 0, N - 1, False)

print("Walsh Table Generated")

for i in walshtable:
    print(i)

binarystrings = []

for i in range(n):
    data = input(f"\nEnter the data for the Station {i + 1}:-  ")
    binarystrings.append([*strTobinary(data)])

print("\nBinary Words:-  ", binarystrings)


count = 0
datatosend = []
while count < n:
    encoded = []
    for i in range(N):
        encoded.append(0)
    for i in range(len(binarystrings)):
        if (len(binarystrings[i]) > 0):
            for j in range(N):
                x = int(binarystrings[i][0])
                if (x == 1):
                    encoded[j] += walshtable[i][j]
                else:
                    encoded[j] += walshtable[i][j]*(-1)

            binarystrings[i].pop(0)
            if (len(binarystrings[i]) == 0):
                count += 1

    datatosend.append(encoded)

res = json.dumps(datatosend)
conn.send(res.encode())
