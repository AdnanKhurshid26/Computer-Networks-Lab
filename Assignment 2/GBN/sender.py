import socket
import time

sender = socket.socket()
port = 12352
sender.connect(('localhost',port))


def VRC(val):
    odd = 0
    for i in val:
        if(i=='1'):
            odd+=1
        
    return str(odd%2)+val


window_size = int(input("Enter Window Size : "))
lst = []
flag = []
times =[]
cur = 0
prev = cur


# Sending Window size
sender.sendall(f"{window_size}".encode())
time.sleep(1)

# Ading First n frames
while True:
    msg = input('Enter Binary String : ')
    lst.insert(cur%window_size,msg)
    flag.insert(cur%window_size,False)
    times.insert(cur%window_size,0)
    cur=cur+1
    if cur%window_size==prev:
        break


while True:
    print("*"*15)
    # Sending frames
    for i in range(len(lst)):
   
        if lst[i] != "exit":
            msg = f"{VRC(lst[i])}:{i}"
        print(f"Sent {msg}")
        sender.sendall(msg.encode())
        times[i]= time.time()
        time.sleep(1)
    


    print("All message Sent")

    # Checking for sack
    for i in range(len(lst)):
        # i = cur_ind%window_size
        print(f"Waiting for {i}")
        # if flag[i]==False:
        ack = sender.recv(1024).decode()
        time.sleep(0.5)
        index = int(ack.split(":")[1])
        ackval = ack.split(":")[0]
        triptime = time.time()-times[index]
        if triptime < 27:
            if ackval == "NACK":
                print(f"Failed Transmission, sending again ")
            else :
                flag[index] = True
                print(f"Succesful Transmission")
        else:
            print("Timeout Had Expired, Sending Again")
                

    print("All responses received")

    # Adding new item to sliding window
    for i in range(len(lst)):
        # i=cur%window_size
        if flag[i]==True:
            msg = input('Enter Binary String : ')
            lst[i] = msg
            flag[i]=False
        else:
            break

        #     break


sender.close()