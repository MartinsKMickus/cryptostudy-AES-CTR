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

# Iegūs 128-bitu ieeju AESam
def generateAESInput(nonce, counter):
    # Pabīdīs tā, lai pirmie 4 hex būtu nonce, pārējais counter
    combined_value = (nonce << 112) | counter
    # Convert the combined value to bytes (16 bytes for 128 bits) AIKOMENTĒTAIS
    return combined_value #.to_bytes(16, byteorder='big')

def encryptAESCTR(fileBits, key, nonce: str):
    # Pārveido no string uz hex nonce
    nonce_bytes = bytes.fromhex(nonce)
    # Pārveido hex uz parastu skaitli
    nonce_int = int.from_bytes(nonce_bytes, byteorder='big')
    # Counter sākas ar 0
    counter = 0
    generateAESInput(nonce_int, counter)

    # TODO: Iterēt caur faila bitiem
    # TODO: Beigās XORot datus ar iegūto
    print("Nav implementēts")
