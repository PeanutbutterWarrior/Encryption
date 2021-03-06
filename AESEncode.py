# AES 256
import random


def keyExpansion(key):
    def rotWord(word):
        return word[1:] + [word[0]]

    def subWord(word):
        outWord = []
        for byte in word:
            hexByte = hex(byte)[2:]
            if len(hexByte) == 1:
                hexByte = '0' + hexByte
            outWord.append(sBoxLookup[int(hexByte[0], 16)][int(hexByte[1], 16)])
        return outWord

    def xorWord(a, b):
        out = []
        for i, j in zip(a, b):
            out.append(i ^ j)
        return out

    key = [int(hex(key)[i:i+2], 16) for i in range(2, len(hex(key)), 2)]
    roundConstants = [None, [0x01, 0, 0, 0], [0x02, 0, 0, 0], [0x04, 0, 0, 0], [0x08, 0, 0, 0],
                      [0x10, 0, 0, 0], [0x20, 0, 0, 0], [0x40, 0, 0, 0], [0x80, 0, 0, 0]]
    N = 8
    keyWords = [[key[i], key[i+1], key[i+2], key[i+3]] for i in range(0, len(key), 4)]
    R = 15
    expandedKey = []
    for i in range(4*R):
        if i < N:
            expandedKey.append(keyWords[i])
        elif i % N == 0:
            oldKey = expandedKey[i-N]
            subbedKey = subWord(rotWord(expandedKey[i-1]))
            const = roundConstants[i//N]
            expandedKey.append(xorWord(xorWord(oldKey, subbedKey), const))
        elif i % N == 4:
            oldKey = expandedKey[i - N]
            subbedKey = subWord(expandedKey[i - 1])
            expandedKey.append(xorWord(oldKey, subbedKey))
        else:
            expandedKey.append(xorWord(expandedKey[i-N], expandedKey[i-1]))
    roundKeys = []
    for i in range(0, 60, 4):
        roundKeys.append([expandedKey[i], expandedKey[i+1], expandedKey[i+2], expandedKey[i+3]])
    return roundKeys


def messageToState(mes):
    out = []
    for i in range(0, 16, 4):
        out.append([])
        for j in range(4):
            out[-1].append(ord(mes[i + j]))
    return out


# WARNING: Acts in place
def addRoundKey(state, key):
    for i, column in enumerate(key):
        for j, byte in enumerate(column):
            state[i][j] ^= byte
    return state


# WARNING: Acts in place
def subBytes(state):
    for i, column in enumerate(state):
        for j, byte in enumerate(column):
            hexByte = hex(byte)[2:]
            if len(hexByte) == 1:
                hexByte = '0' + hexByte
            state[i][j] = sBoxLookup[int(hexByte[0], 16)][int(hexByte[1], 16)]
    return state


def shiftRows(state):
    out = [[], [], [], []]
    for row in range(4):
        for column in range(4):
            out[column].append(state[(column + row) % 4][row])
    return out


def multiply(a, b):
    p = 0
    for i in range(8):
        if b | 0b11111110 == 0xff:
            p ^= a
        aHighSet = a | 0b01111111 == 255
        a <<= 1
        a &= 0xff
        if aHighSet:
            a ^= 0x1b
        b >>= 1
    return p % 256


def mixColumns(state):
    out = []
    const = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
    for column in state:
        newColumn = []
        for a, b, c, d in const:
            newColumn.append(multiply(a, column[0]) ^ multiply(b, column[1]) ^ multiply(c, column[2]) ^ multiply(d, column[3]))
        out.append(newColumn)
    return out


def AESEncode(keys, snippet):
    state = messageToState(snippet)
    keyIndex = 0
    state = addRoundKey(state, keys[keyIndex])
    keyIndex += 1

    for i in range(13):
        state = subBytes(state)
        state = shiftRows(state)
        state = mixColumns(state)
        state = addRoundKey(state, keys[keyIndex])
        keyIndex += 1
    state = subBytes(state)
    state = shiftRows(state)
    state = addRoundKey(state, keys[keyIndex])
    output = []
    for i in state:
        for j in i:
            out = hex(j)[2:]
            if len(out) == 1:
                out = '0' + out
            output.append(out)
    return ' '.join(output)


sBoxLookup = [[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x1, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
              [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
              [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
              [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x5, 0x9a, 0x7, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
              [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
              [0x53, 0xd1, 0x0, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
              [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x2, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
              [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
              [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
              [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
              [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x6, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
              [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x8],
              [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
              [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x3, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
              [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
              [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]]

message = input('Message: ')
# Buffer message with null characters
message += chr(0) * (16 - len(message)%16)

key = random.randint(0x1000000000000000000000000000000000000000000000000000000000000000,
                     0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)
print(f'Key: {hex(key)}')
expandedKeys = keyExpansion(key)

snippets = [message[i:i+16] for i in range(0, len(message), 16)]

outputs = []
for snippet in snippets:
    outputs.append(AESEncode(expandedKeys, snippet))

out = ''
for i in outputs:
    out += i
    out += ' '
print(f'Ciphertext: {out}')