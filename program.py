# TODO: Uztaisīt argument parser (pogas encrypt/derypt)


def subBytes(state): {
    # TODO: Implementēt
    print("Nav implementēts")
}
    
def invSubBytes(state): {
    # TODO: Implementēt
    print("Nav implementēts")
}
    
def shiftRows(state): 
    for i, row in enumerate(state):
            state[i] = row[i:] + row[:i]

    
def invShiftRows(state):
    for i, row in enumerate(state):
        state[i] = row[-i:] + row[:-i]
    
def mixColumns(state): {
    # TODO: Implementēt
    print("Nav implementēts")
}
    
def invMixColumns(state): {
    # TODO: Implementēt
    print("Nav implementēts")
}
    
def addRoundKey(state, roundKey):
    for i in range(4):
        for j in range(4):
            state[i][j] ^= roundKey[i][j]
    

def encryptAESCTR(fileBits, key, initVector, nonce): {
    # TODO: Implementēt AES-CTR šifru
    print("Nav implementēts")
}