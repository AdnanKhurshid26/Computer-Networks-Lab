import socket

#function to build a DNS server heirarchy from a list of domain records

class DNSServer:
    def __init__(self,recordsfile):
        self.infile = recordsfile
        self.root={}
    
    def insertinMap(self,server,query,ip):
        
        if(len(query.split('.')) == 2):
            server[query.split('.')[-1]] = ip
            return
        temp = query.split('.')[-1]
        query= query.split('.')[:-1]
        query = '.'.join(query)
        
        
        if temp not in server:
            server[temp] = {}
            
        self.insertinMap(server[temp],query,ip)
        
        
    
    def buildmap(self):
        with open(self.infile) as f:
            for record in f:
                domain = record.split(',')[0]
                ip = record.split(',')[1][:-1]
                self.insertinMap(self.root,domain,ip)
    
    def resolveQuery(self,query,server):
        if len(query.split('.')) == 2:
            if query.split('.')[-1] in server:
                print(query.split('.')[-1] + " -> " + server[query.split('.')[-1]])
                return server[query.split('.')[-1]]
            else :
                print("NOT FOUND")
                return "-1"
        temp = query.split('.')[-1]
        if temp in server:
            query = query.split('.')[:-1]
            query = '.'.join(query)
            print(temp + " -> ",end='')
            return self.resolveQuery(query,server[temp])
        else:
            print("NOT FOUND")
            return "-1"
            
        

    def startProcess(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) 
        server.bind(('127.0.0.2', 53))
        
        while True :
            query,_ = server.recvfrom(1024)
            query = query.decode()
            print("\nPath : root -> ",end='')
            result = self.resolveQuery(query,self.root)
            # print(result)
            
            server.sendto(result.encode(),('127.0.0.1',53))

            
    
    def printmap(self):
        print(self.root)
        

if __name__ == "__main__":
    server = DNSServer("records.txt")
    server.buildmap()
    server.printmap()
    server.startProcess()
            
            

        