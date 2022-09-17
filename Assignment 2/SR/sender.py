import socket
import time

client = socket.socket()
port = 12359
client.connect(('localhost',port))


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
client.sendall(f"{window_size}".encode())
time.sleep(1)

# Ading First frames to it
while True:
    msg = input('Enter Binary String : ')
    lst.insert(cur%window_size,msg)
    flag.insert(cur%window_size,False)
    times.insert(cur%window_size,0)
    cur=cur+1
    if cur%window_size==prev:
        break


# Startiung loop
while True:
    print("**"*15)
    # Send all Binary Strings
    cur_ind = cur
    while True:
        i = cur_ind%window_size
        if flag[i]==False:
            if lst[i] != "exit":
                msg = f"{VRC(lst[i])}:{i}"
            print(f"Sent frame : {msg}")
            client.sendall(msg.encode())
            times[i]= time.time()
            time.sleep(1)
        cur_ind=cur_ind+1
        if cur_ind%window_size == cur%window_size:
            break;

    print("All message Sent")

    # Checking For Acknowledement
    cur_ind = cur
    while True:
        i = cur_ind%window_size

        if flag[i]==False:
            ack = client.recv(1024).decode()
            time.sleep(0.5)
            index = int(ack.split(":")[1])
            ackval = ack.split(":")[0]
            triptime = time.time()-times[index]
            if triptime < 27:
                if ackval == "NACK":
                    print(f"Unsuccesful transmission, sending again")
                else :
                    flag[index] = True
                    print(f"Succesfully transmitted")
            else:
                print("Timeout Had Expired, Sending Again")
                
        cur_ind=cur_ind+1
        if cur_ind%window_size == cur%window_size:
            break;

    print("All Ack Recived")

    # Adding new item to sliding window
    cur_ind = cur
    while True:
        i=cur%window_size
        if flag[i]==True:
            msg = input('Enter Binary String : ')
            lst[i] = msg
            flag[i]=False

        cur = cur +1
        if cur%window_size == cur_ind%window_size  :
            break


client.close()