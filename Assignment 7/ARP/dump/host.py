import socket
from randmac import RandMac
import sys
import pickle
import threading
import time

class Host:
    def __init__(self,ip):
        self.ip = ip
        self.mac = str(RandMac())
        self.arptable = {}
        self.lock = threading.Lock()
        
        self.sock =socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # Enable broadcasting mode
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #enabling port reuse option
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, 12345))
        # print("Host IP: ",self.ip)
    
    def query(self):
        #create a UDP socket to send broadcast packets
        while True:
            dest_ip = input("Enter destination IP: ")
            #if already in arptable, no need to send query just print the mac
            if dest_ip not in self.arptable:
                self.lock.acquire()
                packet = [self.ip,self.mac,dest_ip]
                self.sock.sendto(pickle.dumps(packet), ('<broadcast>', 12345))
                time.sleep(1)
                dest_mac, addr = self.sock.recvfrom(1024)
                dest_mac = dest_mac.decode()
                self.arptable[dest_ip] = dest_mac
                print("Destination MAC: ",self.arptable[dest_ip])
                self.lock.release()
            else:
                print("Destination MAC: ",self.arptable[dest_ip])
                print("ARP table: ",self.arptable)
            choice = input("Do you want to continue? (y/n): ")
            if choice == 'n':
                break
    
    def response(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            
            data = pickle.loads(data)
            
            sourceip = data[0]
            sourcemac = data[1]
            destip = data[2]
            
            if destip == self.ip:
                packet = [sourceip,sourcemac,self.ip,self.mac]
                self.sock.sendto(pickle.dumps(packet), addr)
                self.arptable[sourceip] = sourcemac
            else:
                print("ARP packet dropped")
    
    def startARP(self):
        t1 = threading.Thread(target=self.query)
        t2 = threading.Thread(target=self.response)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
            
            
            

if __name__ == '__main__':
    ip = sys.argv[1]
    host = Host("127.0.0."+str(ip))
    host.startARP()