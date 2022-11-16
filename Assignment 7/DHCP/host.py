import socket
import time
import pickle

#udp socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

#enabling broadcasting mode
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

client.sendto(b"DHCPREQ", ('<broadcast>', 37020))
print("DHCPREQ broadcasted")

time.sleep(1)

data, addr = client.recvfrom(1024)
ip, gateway, subnetmask = pickle.loads(data)

print("IP: " + ip)
print("Gateway: " + gateway)
print ("Subnet Mask: " + subnetmask)

print("STATUS: Online [ IP:", ip, "]")

flag = input("Enter q to terminate: ")

client.sendto(ip.encode(), ('<broadcast>', 37020))





