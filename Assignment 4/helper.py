def getNextPowerof2(num):
    power = 1
    while power < num:
        power *= 2

    return power

def buildWalshTable(walshTable, length, i1, i2, j1,j2, isComplement):
    if length == 2:
        if not isComplement:
            walshTable[i1][j1] = 1
            walshTable[i1][j2] = 1
            walshTable[i2][j1] = 1
            walshTable[i2][j2] = -1
        else:
            walshTable[i1][j1] = -1
            walshTable[i1][j2] = -1
            walshTable[i2][j1] = -1
            walshTable[i2][j2] = 1

        return
    
    midi = (i1 + i2)//2
    midj = (j1 + j2)//2

    #         |  W_N    W_N  |
    # W_2N =  |              |
    #         |  W_N    W_N' |
    buildWalshTable(walshTable, length/2, i1, midi, j1, midj, isComplement)
    buildWalshTable(walshTable, length/2, i1, midi, midj + 1, j2, isComplement)
    buildWalshTable(walshTable, length/2, midi + 1, i2, j1, midj, isComplement)
    buildWalshTable(walshTable, length/2, midi + 1, i2, midj + 1, j2, not isComplement)
    

def strTobinary(string):
    return ''.join(format(ord(x), '08b') for x in string)

def BinaryToStr(binary):
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))