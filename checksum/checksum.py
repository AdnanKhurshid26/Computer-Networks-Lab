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


def buildFrames(input:str, frameSize):
    output = []
    for i in range(0, len(input), frameSize):
        output.append(input[i:i+frameSize])
    return output

def addBinaryString(a:str, b:str):
    maxlen = max(len(a), len(b))
    
    a = a.zfill(maxlen)
    b = b.zfill(maxlen)
    
    result = ""
    carry=0;
    
    for i in range(maxlen-1,-1,-1):
        r = carry
        r += 1 if a[i] == "1" else 0
        r += 1 if b[i] == "1" else 0
        
        result = ("1" if r % 2 == 1 else "0") + result
        carry = 0 if r < 2 else 1
    
    if carry!=0:
        result = addBinaryString(result,'1')
    return result.zfill(maxlen)

def csencode(input):
    frames = buildFrames(input, 8)
    result = frames[0]
    for i in range(1, len(frames)):
        result = addBinaryString(str(result), str(frames[i]))
    
    result = complement(result)
    return input + result

def csdecode(input):
    frames = buildFrames(input, 8)
    result = frames[0]
    for i in range(1, len(frames)):
        result = addBinaryString(str(result), str(frames[i]))
    
    output = "" 
    for i in range(len(frames)-1):
        output += frames[i]
    if result == "11111111":
        return output,False
    else:
        return output,True
    
def complement(binary):
    return ''.join('0' if x == '1' else '1' for x in binary)