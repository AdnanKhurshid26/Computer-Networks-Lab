
from helper import CountOnesZeros, buildFrames

class VRC:
    @staticmethod
    def encode(binaryInputString:str, dataWordFrameSize:int):
        #  Even Parity VRC
        output = ""
        for i in buildFrames(binaryInputString, dataWordFrameSize):
            _ , noOfOnes = CountOnesZeros(i)
            output += i + ("1" if noOfOnes % 2 == 1 else "0")
        return output

    @staticmethod
    def decode(binaryInputString:str, dataWordFrameSize):
        frames = buildFrames(binaryInputString, dataWordFrameSize+1)
        errorFound = False
        output = ""
        for i in frames:
            #  Even Parity VRC
            _ , noOfOnes = CountOnesZeros(i)
            if noOfOnes % 2 == 0:
                i = i[:-1]
                output += i
            else:
                output += i
                errorFound = True

        return output, errorFound