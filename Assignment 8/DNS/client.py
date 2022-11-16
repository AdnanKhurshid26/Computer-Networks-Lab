import socket

class Client:
    def __init__(self):
        pass
    
    def startProcess(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        client.bind(('127.0.0.1', 53))
        
        while True:
            query = input("Enter a domain name: ")
        
            client.sendto(query.encode(),('127.0.0.2',53))
        
            result,_ = client.recvfrom(1024)
            result = result.decode()
        
            if(result == "-1"):
                print("Domain not found")
                break
            
            print("IP address: " + result)

if __name__ == "__main__":
    client = Client()
    client.startProcess()
        