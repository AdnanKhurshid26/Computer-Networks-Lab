import socket
import random
from LRC import strTobinary, lrcencode, lrcdecode,buildFrames, CountOnesZeros, BinaryToStr

def injectErrorAtIndex(index,encoded):
        encoded = encoded[:index] + ('0' if encoded[index] == '1' else '1') + encoded[index+1:]
        return encoded


sender = socket.socket()
print("Socket successfully created")

sender.bind(('', 12345))

sender.listen(1)

recv, addr = sender.accept()

datatosend = input("Enter the data to be sent: ")

binarydata = strTobinary(datatosend)

encoded = lrcencode(binarydata, 8)

encodedframes = buildFrames(binarydata,8+1)

print("Frames to be sent: ", encodedframes)

iserror = int(input("Enter 1 if you want to introduce error,else 0: "))

if iserror == 1:
    errorpos = (input("Enter the positions of error separated by comm : "))
    errorpos = [int(i.strip()) for i in errorpos.split(",")]
    for i in errorpos:
           encoded = injectErrorAtIndex(i,encoded)
    


recv.send(encoded.encode())

exit = input("Press any key to exit: ")
