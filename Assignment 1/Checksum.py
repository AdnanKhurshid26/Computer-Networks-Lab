
from helper import addBinaryStrUsingOnesComplement, buildFrames, binaryStrComplement


class Checksum:
    @staticmethod
    def encode(binaryInputString:str, dataWordFrameSize:int, noOfOriginalDataFramesPerGroup:int=4):
        output = ""
        frames = buildFrames(binaryInputString, dataWordFrameSize)
        # Check whether we can split in to equal length of frames
        noOfFramesRequiredToBeAdded = noOfOriginalDataFramesPerGroup - len(frames)%noOfOriginalDataFramesPerGroup
        if noOfFramesRequiredToBeAdded > 0 and noOfFramesRequiredToBeAdded != noOfOriginalDataFramesPerGroup:
            for _ in range(noOfFramesRequiredToBeAdded):
                frames.append("0"*dataWordFrameSize)

        # Iterate over the frames to calculate the checksum
        for i in range(0, len(frames), noOfOriginalDataFramesPerGroup):
            tmpFrames = frames[i:i+noOfOriginalDataFramesPerGroup]
            tmp = tmpFrames[0]
            frameString = ""
            for frame in tmpFrames[1:]:
                tmp = addBinaryStrUsingOnesComplement(tmp, frame)
                frameString += frame
            
            # Complement and get checksum
            checksum = binaryStrComplement(tmp)
            output = output + tmpFrames[0] + frameString + checksum
        
        return output

    @staticmethod
    def decode(binaryInputString:str, dataWordFrameSize:int, noOfOriginalDataFramesPerGroup:int=4):
        output = ""
        frames = buildFrames(binaryInputString, dataWordFrameSize)
        errorFound = False

        # Iterate over the frames to calculate the checksum and verify 
        for i in range(0, len(frames), noOfOriginalDataFramesPerGroup+1):
            tmpFrames = frames[i:i+noOfOriginalDataFramesPerGroup+1]
            tmp = tmpFrames[0]
            frameString = ""
            for frame in tmpFrames[1:]:
                tmp = addBinaryStrUsingOnesComplement(tmp, frame)
                frameString += frame
            
            # Complement and get checksum
            checksum = binaryStrComplement(tmp)
            if checksum == "0"*dataWordFrameSize:
                output += (tmpFrames[0] + frameString[:-dataWordFrameSize])
            else:
                output += (tmpFrames[0] + frameString[:-dataWordFrameSize])
                errorFound = True
        
        return output, errorFound