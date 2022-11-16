import socket
import pickle


class DHCPServer:
    startingIP = ""
    lastAssignedIP = ""
    defaultGateway = ""
    subnetMask = ""
    IPpool = {}
    
    def __init__(self, startingIP, defaultGateway, subnetMask):
        self.startingIP = startingIP
        self.lastAssignedIP = startingIP
        self.defaultGateway = defaultGateway
        self.subnetMask = subnetMask
        self.IPpool[startingIP] = False
    
    def getFreeIP(self):
        for ip in self.IPpool:
            if not self.IPpool[ip]:
                self.IPpool[ip] = True
                return str(ip)
        hostnum = int(self.lastAssignedIP.split(".")[3])
        newip =  self.lastAssignedIP.split(".")[0] + "." + self.lastAssignedIP.split(".")[1] + "." + self.lastAssignedIP.split(".")[2] + "." + str(hostnum + 1)
        self.IPpool[newip] = True
        self.lastAssignedIP = newip
        return newip

    def releaseIP(self, ip):
        if ip in self.IPpool:
            self.IPpool[ip] = False
            return True
        else:
            return False
    
    def startServer(self):
        #udp socket
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) 

        # Enable broadcasting mode
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        server.bind(("", 37020))
        while True:
            data, addr = server.recvfrom(1024)
            clientip, clientport = addr
            
            if data.decode() == "DHCPREQ":
                print("DHCPREQ received from " + clientip)
                newip = self.getFreeIP()
                print("New IP assigned to " + clientip + ": " + newip)
                server.sendto(pickle.dumps([newip, self.defaultGateway, self.subnetMask]), addr)
            else :
                print("DHCPREL received from " + data.decode())
                self.releaseIP(data.decode())
                print("IP released")
        

if __name__ == "__main__":
    server = DHCPServer("192.168.1.2", "192.168.1.1", "255.255.255.0")
    server.startServer()
    


