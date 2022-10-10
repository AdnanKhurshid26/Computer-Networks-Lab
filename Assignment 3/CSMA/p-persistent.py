import threading
import time
import random

transmissionTime = 2
backoffTime = None
lock = threading.Lock()

class p_Persistent(threading.Thread):
    def __init__(self,frames,index,prob):
        super().__init__()
        self.frames = frames
        self.ind = index
        self.prob = prob
    
    def run(self):
        count = 1
        while count<=self.frames:
            while lock.locked():
                print(f"CHANNEL BUSY. SENDER {self.ind} WAITING\n")
                time.sleep(0.3)
            
            lock.acquire()
            print(f"CHANNEL IDLE. SENDER {self.ind} GETTING PROBABILTY...\n")
            #calculating probability
            p = random.random()
            if(p>=self.prob):
                print(f"PROBABILITY GREATER THAN {self.prob} , SENDING FRAME {count} NOW...\n")
                #transmission time
                time.sleep(transmissionTime)
                count += 1
                lock.release()
            else:
                print(f"PROBABILITY GREATER THAN {self.prob} , WAITING ONE SLOT\n")
                lock.release()
                time.sleep(backoffTime)
        return

if __name__=='__main__':
    sender_count = int(input("Enter number of senders: "))
    frames= int(input("Enter number of frames to be sent: "))
    backoffTime = int(input("Enter backoff time: "))
    start = time.time()
    senders = [p_Persistent(frames,i+1,1/sender_count) for i in range(0,sender_count)]
    for node in senders:
        node.start()
    
    for node in senders:
        node.join()
    
    end = time.time()
    
    utilization = round(100*(frames*transmissionTime*sender_count)/(end-start),2)
    
    print(f"Channel utilization: {utilization}%")

    
    

        
        
