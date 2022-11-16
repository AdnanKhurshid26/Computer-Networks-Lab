def strTobinary(string):
    return ''.join(format(ord(x), '08b') for x in string)


def BinaryToStr(binary):
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))


def CountOnesZeros(input):
    noOfZeros = 0
    noOfOnes = 0

    for i in input:
        if i == '0':
            noOfZeros += 1
        elif i == '1':
            noOfOnes += 1

    return noOfZeros, noOfOnes


def buildFrames(input, frameSize):
    output = []
    for i in range(0, len(input), frameSize):
        output.append(input[i:i+frameSize])
    return output


def lrcencode(binaryInputString: str, dataWordFrameSize: int):
    output = ""
    frames = buildFrames(binaryInputString, dataWordFrameSize)
    # Check whether we can split in to equal length of frames

    # Iterate over the frames to calculate the parity
    
    tmpFrames = frames
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


def lrcdecode(binaryInputString: str, dataWordFrameSize: int):
    # Split frames from data
    frames = buildFrames(binaryInputString, dataWordFrameSize)
    errorFound = False
    output = ""
    # Iterate over the frames
    
    tmp_frames = frames
    parity_frame = tmp_frames[-1]
    tmp_frames = tmp_frames[:-1]
    frameErrorFound = False
        # Verify parity
    for index in range(dataWordFrameSize):
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
