import socket
from randmac import RandMac
import sys
import pickle
import threading

QUERY_PORT = 12345
RESPONSE_PORT = 37020


class Host:
    def __init__(self, ip):
        self.ip = ip
        self.mac = str(RandMac())
        self.arptable = {}

        print("IP of this host: ", self.ip)
        print("MAC of this host: ", self.mac)

        self.querysock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # # Enable broadcasting mode
        self.querysock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # enable port reuse option
        self.querysock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.querysock.bind((self.ip, QUERY_PORT))

        # create a UDP socket to receive broadcast packets
        self.responsesock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.responsesock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.responsesock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind to the port
        self.responsesock.bind((self.ip, RESPONSE_PORT))

        # print("Host IP: ",self.ip)

    def query(self):
        # create a UDP socket to send broadcast packets
        while True:
            dest_ip = input("Enter destination IP: ")
            # if already in arptable, no need to send query just print the mac
            if dest_ip not in self.arptable:
                packet = [self.ip, self.mac, dest_ip]
                self.querysock.sendto(pickle.dumps(
                    packet), ('<broadcast>', RESPONSE_PORT))
                # print("Sent ARP query to ",dest_ip)
                # print("Waiting for response...")
                recvd_data, _ = self.querysock.recvfrom(1024)
                recvd_data = pickle.loads(recvd_data)
                dest_mac = recvd_data[3]
                self.arptable[dest_ip] = dest_mac
                print("Destination MAC: ", self.arptable[dest_ip])
            else:
                print("Found in ARP table")
                print("Destination MAC: ", self.arptable[dest_ip])
                print("ARP table: ", self.arptable)
            choice = input("Do you want to continue? (y/n): ")
            if choice == 'n':
                break

    def response(self):
        while True:
            # print("Waiting for ARP query...")
            data, _ = self.responsesock.recvfrom(1024)
            # print("Received ARP query")
            data = pickle.loads(data)

            sourceip = data[0]
            sourcemac = data[1]
            destip = data[2]

            if destip == self.ip:
                packet = [sourceip, sourcemac, self.ip, self.mac]
                self.responsesock.sendto(pickle.dumps(
                    packet), (sourceip, QUERY_PORT))
                self.arptable[sourceip] = sourcemac
            # else:
            #     print("ARP packet dropped")

    def startARP(self):
        t1 = threading.Thread(target=self.query)
        t2 = threading.Thread(target=self.response)
        t1.start()
        t2.start()


if __name__ == '__main__':
    ip = sys.argv[1]
    host = Host("127.0.0."+str(ip))
    host.startARP()
