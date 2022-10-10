import threading
import time

lock = threading.Lock()
transmissionTime = 2
#thread class for each station
class OnePersistent(threading.Thread):
    def __init__(self,frames, index):
        super().__init__()
        self.ind = index
        self.frames = frames

    def run(self):
        
        for i in range(self.frames):
            if lock.locked():
                # print(f"CHANNEL BUSY. SENDER {self.ind} WAITING\n")
                while lock.locked():
                    print(f"CHANNEL BUSY. SENDER {self.ind} LISTENING AGAIN\n")
                    time.sleep(0.1)
                    pass
                
            lock.acquire()
            print(f"CHANNEL IDLE. SENDER {self.ind} SENDING FRAME {i+1} NOW...\n")
            time.sleep(transmissionTime)
            lock.release()
            time.sleep(0.4)

        return


if __name__ == '__main__':
    sender_count = int(input("Enter number of senders: "))
    frames= int(input("Enter number of frames to be sent: "))
    start = time.time()
    senders = [OnePersistent(frames,i+1) for i in range(0, sender_count)]
    
    for node in senders:
        node.start()
    for node in senders:
        node.join()
        
    end = time.time()
    
    utilization = round(100*(frames*transmissionTime*sender_count)/(end-start),2)
    
    print(f"Channel utilization: {utilization}%")

