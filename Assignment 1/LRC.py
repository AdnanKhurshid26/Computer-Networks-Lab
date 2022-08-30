
from helper import  buildFrames


class LRC:
    @staticmethod
    def encode(binaryInputString:str, dataWordFrameSize:int, noOfOriginalDataFramesPerGroup:int=4):
        output = ""
        frames = buildFrames(binaryInputString, dataWordFrameSize)
        # Check whether we can split in to equal length of frames
        noOfFramesRequiredToBeAdded = noOfOriginalDataFramesPerGroup - len(frames)%noOfOriginalDataFramesPerGroup
        if noOfFramesRequiredToBeAdded > 0 and noOfFramesRequiredToBeAdded != noOfOriginalDataFramesPerGroup:
            for _ in range(noOfFramesRequiredToBeAdded):
                frames.append("0"*dataWordFrameSize)
        
        # Iterate over the frames to calculate the parity
        for i in range(0, len(frames), noOfOriginalDataFramesPerGroup):
            tmpFrames = frames[i:i+noOfOriginalDataFramesPerGroup]
            parity = ""
            for index in range(dataWordFrameSize)[::-1]:
                noOfOnes = 0
                # Count no of ones in frame
                for frame in tmpFrames:
                    if frame[index] == "1":
                        noOfOnes += 1
                # Add parity bit
                parity = ("1" if noOfOnes % 2 != 0 else "0") + parity
                

            # Append to output
            output = output + ''.join(tmpFrames) + parity

        return output
    
    @staticmethod
    def decode(binaryInputString:str, dataWordFrameSize:int, noOfOriginalDataFramesPerGroup:int=4):
        # Split frames from data
        frames = buildFrames(binaryInputString, dataWordFrameSize)
        errorFound = False
        output = ""
        # Iterate over the frames
        for i in range(0, len(frames), noOfOriginalDataFramesPerGroup+1):
            tmp_frames = frames[i:i+noOfOriginalDataFramesPerGroup+1]
            parity_frame = tmp_frames[-1]
            frameErrorFound = False
            # Verify parity
            for index in range(dataWordFrameSize)[::-1]:
                noOfOnes = 0
                for frame in tmp_frames[:-1]:
                    noOfOnes = noOfOnes + (1 if frame[index] == '1' else 0)
                noOfOnes = noOfOnes + (1 if parity_frame[index] == '1' else 0)
                if noOfOnes % 2 != 0:
                    frameErrorFound = True
                    break
            if frameErrorFound:
                output += ''.join(tmp_frames[:-1])
                errorFound = True
            else:
                output += ''.join(tmp_frames[:-1])
        
        return output, errorFound