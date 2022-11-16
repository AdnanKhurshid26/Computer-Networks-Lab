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
        self.event = threading.Event()
        self.event.set()
        
    def request(self):
            query_sock =socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            # Enable broadcasting mode
            query_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            query_sock.bind(("", 37020))
            dest_ip = input("Enter destination IP: ")
            if dest_ip not in self.arptable:
                query_sock.sendto(dest_ip.encode(), ('<broadcast>', 12345))
                time.sleep(1)
            
                dest_mac, addr = self.sock.recvfrom(1024)
                dest_mac = dest_mac.decode()
                self.arptable[dest_ip] = dest_mac

            print("Destination MAC: ",self.arptable[dest_ip])
            print("ARP table: ",self.arptable)
            
    def response(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            dest_ip = data.decode()
            
            if dest_ip == self.ip:
                print("Received ARP request from :",addr[0])
                print("Sending ARP response to :",addr[0])
                self.sock.sendto(self.mac.encode(), addr)
            else:
                print("ARP packet dropped")
    def startARP(self):
        t1 = threading.Thread(target=self.request)
        t2 = threading.Thread(target=self.response)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    
if __name__ == '__main__':
    ip = sys.argv[1]
    host = Host("127.0.0."+str(ip))
    host.startARP()
    