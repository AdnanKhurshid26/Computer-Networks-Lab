
from helper import buildFrames,  divisonCRC
class CRC:
    @staticmethod
    def encode(binaryInputString:str, dataWordFrameSize:int, divisor:str):
        output = ""
        crcSize = len(divisor)-1
        for i in buildFrames(binaryInputString, dataWordFrameSize):
            tmp = i+crcSize*"0" # [max degree of polynomial] times 0
            crc = divisonCRC(tmp, divisor)[:crcSize]
            output += i+crc.zfill(crcSize)
        return output

    @staticmethod
    def decode(binaryInputString:str, dataWordFrameSize:int, divisor:str):
        output = ""
        errorFound = False
        crcSize = len(divisor)-1
        for i in buildFrames(binaryInputString, dataWordFrameSize+crcSize):
            remainder = divisonCRC(i, divisor)
            if remainder == 0 or remainder == '0':
                messageData = i[:-crcSize]
                # print(messageData)
                output += messageData
            else:
                messageData = i[:-crcSize]
                # print(messageData)
                output += messageData
                errorFound = True
        
        return output, errorFound
