import threading
import time
import random

transmissionTime = 2
lock = threading.Lock()

class nonPersistent(threading.Thread):
    def __init__(self,frames,index):
        super().__init__()
        self.ind = index
        self.frames = frames
    
    def run(self):
        for i in range(self.frames):
            while lock.locked():
                x = random.randint(1, 7)
                print(f"CHANNEL BUSY. SENDER {self.ind} WAITING for {x} SECONDS\n")
                time.sleep(x)
            lock.acquire()
            print(f"CHANNEL IDLE. SENDER {self.ind} SENDING FRAME {i+1} NOW...\n")
            #transmission time
            time.sleep(transmissionTime)
            lock.release()
        return

if __name__=='__main__':
    sender_count = int(input("Enter number of senders: "))
    frames= int(input("Enter number of frames to be sent: "))
    start = time.time()
    senders = [nonPersistent(frames,i+1) for i in range(0,sender_count)]
    for node in senders:
        node.start()
    
    for node in senders:
        node.join()
    
    end = time.time()
    
    utilization = round(100*(frames*transmissionTime*sender_count)/(end-start),2)
    
    print(f"Channel utilization: {utilization}%")
    
    # metric = 100*totalsent/(4*sender_count)
    # print(f"Total number of packets successfully sent: {totalsent}")
    
    

        
        
