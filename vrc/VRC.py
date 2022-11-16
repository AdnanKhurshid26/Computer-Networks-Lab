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


def vrcencode(binaryInputString: str, dataWordFrameSize: int):
    #  Even Parity VRC
    output = ""
    for i in buildFrames(binaryInputString, dataWordFrameSize):
        _, noOfOnes = CountOnesZeros(i)
        output += i + ("1" if noOfOnes % 2 == 1 else "0")
    return output


def vrcdecode(binaryInputString: str, dataWordFrameSize):
    frames = buildFrames(binaryInputString, dataWordFrameSize+1)
    errorFound = False
    output = ""
    for i in frames:
        #  Even Parity VRC
        _, noOfOnes = CountOnesZeros(i)
        i = i[:-1]
        output += i
        if noOfOnes % 2 == 1:
            errorFound = True

    return output, errorFound
