import os
import argparse

NK = 4
NB = 4
NR = 10

s_box = [
    [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
    [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
    [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
    [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
    [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
    [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
    [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
    [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
    [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
    [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
    [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
    [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
    [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
    [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
    [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
    [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]
]

def rowColumnSwitch(state):
    return [[row[i] for row in state] for i in range(len(state[0]))]

def subBytes(state):
    for i in range(4):
        for j in range(4):
            x = (state[i][j] >> 4) & 0xF
            y = state[i][j] & 0xF

            state[i][j] = s_box[x][y]
    
def shiftRows(state):
    state = rowColumnSwitch(state)
    for i in range(1, 4):  # Skip the first row
        state[i] = state[i][i:] + state[i][:i]
    return rowColumnSwitch(state)



def mixColumns(state):
    state = rowColumnSwitch(state)
    # MixColumn matrix
    mixColumnMatrix = [
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02]
    ]

    # Initialize the result state matrix
    resultState = [[0] * 4 for _ in range(4)]

    for i in range(4):  # Iterate over columns
        for j in range(4):  # Iterate over rows
            resultState[j][i] = (
                multiply(mixColumnMatrix[j][0], state[0][i]) ^
                multiply(mixColumnMatrix[j][1], state[1][i]) ^
                multiply(mixColumnMatrix[j][2], state[2][i]) ^
                multiply(mixColumnMatrix[j][3], state[3][i])
            )
    resultState = rowColumnSwitch(resultState)
    return resultState

def multiply(a, b):
    # Multiplication in Galois Field (GF(2^8))
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11B  # The irreducible polynomial for AES
        b >>= 1
    return result
    
def addRoundKey(state, roundKey):
    for i in range(4):
        for j in range(4):
            state[i][j] ^= roundKey[i][j]

def rotWordInplace(word):
    # Assume 'word' is a 32-bit word represented as a list of 4 bytes
    # Rotate the word to the left by 1 position
    word[:] = word[1:] + [word[0]]

def subWord(word):
    for i in range(4):
        word[i] = s_box[word[i] >> 4][word[i] & 0x0F]

def generate_rcon(round_number):
    rcon = 1
    for i in range(1, round_number + 1):
        rcon = (rcon << 1) ^ (0x11b if (rcon & 0x80) else 0)
    return rcon.to_bytes(4, byteorder='little') # TODO: DEBUG IF LITTLE OR BIG

def xorBinaryList(list1, list2):
    result = []
    for i in range(len(list1)):
        result.append(list1[i] ^ list2[i])
    return result

def keyExpansion(key: bytes):
    # Apraksts 128-bitu gadījumā
    # key būs izmērā 128-biti jeb 32-baiti
    # expandedW būs izmērā 44 * 32-biti(4baiti) = 352baiti
    # SVARĪGI VIENA ITERĀCIJA IR 1Xi vai 4Xi (Simulē word garumu)
    # expandedW = 1 Iterācijai jābūt 32-bitiem (4-baitiem) (4xi)
    # key - 1 Iterācija 8-biti (1-baits) (1xi)
    expandedK = []
    for i in range(NB*(NR+1)*4):
        expandedK.append(0x00)

    i = 0
    while(i<NK):
        # Simulēt word = 4 baitus
        expandedK[4*i] = key[4*i]
        expandedK[4*i+1] = key[4*i+1]
        expandedK[4*i+2] = key[4*i+2]
        expandedK[4*i+3] = key[4*i+3]
        i += 1
    
    i = NK
    temp = [0x00, 0x00, 0x00, 0x00]
    while (i < NB * (NR+1)):
        # Simulēt word = 4 baitus
        temp[0] = expandedK[(i-1)*4]
        temp[1] = expandedK[(i-1)*4+1]
        temp[2] = expandedK[(i-1)*4+2]
        temp[3] = expandedK[(i-1)*4+3]
        if (i % NK == 0):
            # temp = SubWord(RotWord(temp)) xor Rcon[i/Nk]
            rotWordInplace(temp)
            # print(f'Rot {i}: {bytesToHexString(temp)}')
            subWord(temp)
            # print(f'Sub {i}: {bytesToHexString(temp)}')
            rcon = generate_rcon(int(i/NK)-1)
            # print(f'I/NK = {int(i/NK)-1}')
            # print(f'Rcon {i}: {bytesToHexString(rcon)}')
            # print(temp)
            # print(generate_rcon(int(i/NK)))
            temp = xorBinaryList(temp, rcon)
        elif (NK > 6) and (i % NK == 4):
            subWord(temp)
        # Simulēt word = 4 baitus
        expandedK[4*i] = expandedK[(i-NK)*4] ^ temp[0]
        expandedK[4*i+1] = expandedK[(i-NK)*4+1] ^ temp[1]
        expandedK[4*i+2] = expandedK[(i-NK)*4+2] ^ temp[2]
        expandedK[4*i+3] = expandedK[(i-NK)*4+3] ^ temp[3]
        i += 1
    return expandedK

def roundKeyFunc(expandedK, expKIndex):
    roundKey = [
        [expandedK[expKIndex], expandedK[expKIndex+1], expandedK[expKIndex+2], expandedK[expKIndex+3]],
        [expandedK[expKIndex+4], expandedK[expKIndex+5], expandedK[expKIndex+6], expandedK[expKIndex+7]],
        [expandedK[expKIndex+8], expandedK[expKIndex+9], expandedK[expKIndex+10], expandedK[expKIndex+11]],
        [expandedK[expKIndex+12], expandedK[expKIndex+13], expandedK[expKIndex+14], expandedK[expKIndex+15]]
    ]
    return roundKey

def matrix(array):
    returnMatrix = [
        [array[0], array[1], array[2], array[3]],
        [array[4], array[5], array[6], array[7]],
        [array[8], array[9], array[10], array[11]],
        [array[12], array[13], array[14], array[15]]
    ]
    return returnMatrix

def cipherAES(input: bytes, expandedK: bytes):
    output = []
    # TODO: HARDCODED FOR 128-bit mode
    state = matrix(input)
    # TODO: HARDCODED FOR 128-bit mode
    roundKey = matrix(expandedK)
    addRoundKey(state, roundKey)
    for round in range(NR-1):
        # print(f'Start({round+1}): ', bytesToHexString(state[0] + state[1] + state[2] + state[3], mode=1))
        subBytes(state)
        # print(f'Sub_b({round+1}): ', bytesToHexString(state[0] + state[1] + state[2] + state[3], mode=1))
        state = shiftRows(state)
        # print(f'Sft_r({round+1}): ', bytesToHexString(state[0] + state[1] + state[2] + state[3], mode=1))
        state = mixColumns(state)
        # print(f'Mix_c({round+1}): ', bytesToHexString(state[0] + state[1] + state[2] + state[3], mode=1))
        # TODO: HARDCODED FOR 128-bit mode
        expKIndex = (round+1)*NB*4
        roundKey = roundKeyFunc(expandedK, expKIndex)
        # print(f'K-sch({round+1}): ', bytesToHexString(roundKey[0] + roundKey[1] + roundKey[2] + roundKey[3], mode=1))
        addRoundKey(state, roundKey)
        
    subBytes(state)
    # print(f'Sub_b({10}): ', bytesToHexString(state[0] + state[1] + state[2] + state[3], mode=1))
    state = shiftRows(state)
    # print(f'Sft_r({10}): ', bytesToHexString(state[0] + state[1] + state[2] + state[3], mode=1))
    # TODO: HARDCODED FOR 128-bit mode
    expKIndex = NR*NB*4
    roundKey = roundKeyFunc(expandedK, expKIndex)
    # print(f'K-sch({10}): ', bytesToHexString(roundKey[0] + roundKey[1] + roundKey[2] + roundKey[3], mode=1))
    addRoundKey(state, roundKey)
    return state

# Iegūs 128-bitu ieeju AESam
def generateAESInput(nonce, counter):
    # Pabīdīs tā, lai pirmie 4 hex būtu nonce, pārējais counter
    combined_value = (nonce << 112) | counter
    # Convert the combined value to bytes (16 bytes for 128 bits) AIKOMENTĒTAIS
    return combined_value.to_bytes(16, byteorder='big') # TODO: DEBUG IF LITTLE OR BIG

def encryptAESCTR(input_file_name:str, key: str, nonce: str):
    # Pārveido no string uz hex nonce
    nonce_bytes = bytes.fromhex(nonce)
    key_bytes = bytes.fromhex(key)
    # Pārveido hex uz parastu skaitli
    nonce_int = int.from_bytes(nonce_bytes, byteorder='big')
    # Counter sākas ar 0
    counter = 0
    expandedK = keyExpansion(key_bytes)
    file_name = os.path.splitext(os.path.basename(input_file_name))
    file_name = file_name[0] + file_name[1]
    if not os.path.exists('encrypted'):
        os.makedirs('encrypted')
    with open(f'encrypted/encrypted', 'wb') as ciphered_file:
        # Šifrētais fails sāksies ar init vektoru
        init_vector = generateAESInput(nonce_int, counter)
        ciphered_file.write(init_vector)
        with open(input_file_name, 'br') as input_file:
            # file_name = bytes(file_name)
            file_name_bytes = file_name.encode("utf-8")
            # TODO: Check file name length
            # print(file_name_bytes)
            # Nošifrē faila nosaukumu
            for i in range(32):
                counter += 1
                chunk = file_name_bytes[i*16:i*16+16]
                chunk += bytes(16 - len(chunk))
                init_vector = generateAESInput(nonce_int, counter)
                block_res = cipherAES(init_vector, expandedK)
                result = bytes(xorBinaryList(chunk,block_res[0] + block_res[1] + block_res[2] + block_res[3]))
                ciphered_file.write(result)
            while True:
                counter += 1
                input_chunk = input_file.read(16)
                if not input_chunk:
                    break
                init_vector = generateAESInput(nonce_int, counter)
                block_res = cipherAES(init_vector, expandedK)
                # print(input_chunk)
                # print(block_res)
                result = bytes(xorBinaryList(input_chunk,block_res[0] + block_res[1] + block_res[2] + block_res[3]))
                # print(result)
                ciphered_file.write(result)

def decryptAESCTR(file_name: str, key: str):
    # Pārveido no string uz hex nonce
    # nonce_bytes = bytes.fromhex(nonce)
    key_bytes = bytes.fromhex(key)
    # Counter sākas ar 0
    counter = 0
    expandedK = keyExpansion(key_bytes)
    with open(file_name, 'br') as ciphered_file:
        # Šifrētais fails sāksies ar init vektoru
        nonce = ciphered_file.read(16)[:2]
        # print(nonce)
        nonce_int = int.from_bytes(nonce, byteorder='big')
        # file_name_without_extension = os.path.splitext(os.path.basename(file_name))[0]
        if not os.path.exists('decrypted'):
            os.makedirs('decrypted')
        decrypted_name = []
        # Atkodēt oriģinālā faila nosaukumu
        for _ in range(32):
            counter += 1
            chunk = ciphered_file.read(16)
            # chunk += bytes(16 - len(chunk))
            init_vector = generateAESInput(nonce_int, counter)
            block_res = cipherAES(init_vector, expandedK)
            result = bytes(xorBinaryList(chunk,block_res[0] + block_res[1] + block_res[2] + block_res[3]))
            decrypted_name += result
        decrypted_name = [value for value in decrypted_name if value != 0]
        # print(decrypted_name)
        decrypted_name = bytes(decrypted_name).decode("utf-8")
        with open(f'decrypted/{decrypted_name}', 'bw') as output_file:
            while True:
                counter += 1
                init_vector = generateAESInput(nonce_int, counter)
                input_chunk = ciphered_file.read(16)
                if not input_chunk:
                    break
                block_res = cipherAES(init_vector, expandedK)
                # print(input_chunk)
                # print(block_res)
                result = bytes(xorBinaryList(input_chunk,block_res[0] + block_res[1] + block_res[2] + block_res[3]))
                # print(result)
                output_file.write(result)

def bytesToHexString(variable, mode=0):
    # return ''.join(['{:02x}'.format(value) + ('\n' if (i + 1) % 4 == 0 else '') for i, value in enumerate(variable)])
    if mode ==0:
        return ''.join(['{:02x}'.format(value) for value in variable])
    else:
        return ''.join(['{:02x}'.format(value) + (' ' if (i + 1) % 4 == 0 else '') for i, value in enumerate(variable)])

def testAES():
    key_bytes = bytes.fromhex('000102030405060708090a0b0c0d0e0f')
    input_bytes = bytes.fromhex('00112233445566778899aabbccddeeff')
    expandedK = keyExpansion(key_bytes)
    # print('Result: ', bytesToHexString(expandedK))
    # return

    block_res = cipherAES(input_bytes, expandedK)
    block_res = block_res[0] + block_res[1] + block_res[2] + block_res[3]
    block_res = bytes(block_res)
    # input_bytes = hex(input_bytes)
    bytesToHexString(key_bytes)
    print('Plaintext: ',bytesToHexString(input_bytes))
    print('Key: ', bytesToHexString(key_bytes))
    print('Result: ', bytesToHexString(block_res))
# Piemēri:
# encryptAESCTR('MyFyle.docx', '0123456789ABCDEF0123456789ABCDEF', 'ABCD')
# decryptAESCTR('encrypted/MyFile', '0123456789ABCDEF0123456789ABCDEF')

def check_key(key):
    if len(key) != 32 or not all(c in '0123456789abcdefABCDEF' for c in key):
        raise argparse.ArgumentTypeError('Key must be 32 hexadecimal characters long')
    return key


def check_nonce(nonce):
    if len(nonce) != 4 or not all(c in '0123456789abcdefABCDEF' for c in nonce):
        raise argparse.ArgumentTypeError('Nonce must be 4 hexadecimal characters long')
    return nonce


parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, help='File to encrypt/decrypt')
parser.add_argument('-m', '--mode', required=True, type=str, help='Mode to use (encrypt/decrypt)')
parser.add_argument('-k', '--key', required=True, type=check_key, help='Key to use for encryption/decryption (32 hex characters)')
parser.add_argument('-n', '--nonce', required=False, type=check_nonce, help='Nonce to use for encryption/decryption (4 hex characters)')
args = parser.parse_args()

if args.mode == 'encrypt':
    encryptAESCTR(args.file, args.key, args.nonce)
elif args.mode == 'decrypt':
    decryptAESCTR(args.file, args.key)

# testAES()
# def invMixColumns(state):
#     inv_mix_matrix = [
#         [0xE, 0xB, 0xD, 0x9],
#         [0x9, 0xE, 0xB, 0xD],
#         [0xD, 0x9, 0xE, 0xB],
#         [0xB, 0xD, 0x9, 0xE]
#     ]
#
#     def gf_add_mul(a, b):
#         p = 0
#         for i in range(4):
#             p ^= gf_mul(a[i], b[i])
#         return p
#
#     def gf_mul(a, b):
#         p = 0
#         for _ in range(4):
#             if b & 1:
#                 p ^= a
#             hi_bit_set = a & 0x8
#             a <<= 1
#             if hi_bit_set:
#                 a ^= 0x3
#             b >>= 1
#         return p & 0xF
#
#     mixed_state = [[0] * 4 for _ in range(4)]
#     for col in range(4):
#         for row in range(4):
#             mixed_state[row][col] = gf_add_mul(
#                 [state[i][col] for i in range(4)],
#                 [inv_mix_matrix[row][i] for i in range(4)]
#             )
#
#     return mixed_state

    
""" def invShiftRows(state):
    for i, row in enumerate(state):
        state[i] = row[-i:] + row[:-i] """
    
""" def invSubBytes(state):
    for i in range(4):
        for j in range(4):
            x = (state[i][j] >> 4) & 0xF
            y = state[i][j] & 0xF

            state[i][j] = inv_s_box[x][y] """

""" inv_s_box = [
    [0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB],
    [0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB],
    [0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E],
    [0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25],
    [0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92],
    [0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84],
    [0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06],
    [0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B],
    [0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73],
    [0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E],
    [0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B],
    [0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4],
    [0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F],
    [0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF],
    [0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61],
    [0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D]
] """