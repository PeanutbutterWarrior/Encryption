# AES 256
def keyExpansion(key):
    def rotWord(word):
        word = hex(word)[2:]
        return int(word[2:] + word[:2], 16)

    def subWord(word):
        outWord = []
        sBoxLookup = [['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '1', '67', '2b', 'fe', 'd7', 'ab', '76'],
                      ['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'],
                      ['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'],
                      ['4', 'c7', '23', 'c3', '18', '96', '5', '9a', '7', '12', '80', 'e2', 'eb', '27', 'b2', '75'],
                      ['9', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'],
                      ['53', 'd1', '0', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'],
                      ['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '2', '7f', '50', '3c', '9f', 'a8'],
                      ['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'],
                      ['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'],
                      ['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'],
                      ['e0', '32', '3a', '0a', '49', '6', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'],
                      ['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '8'],
                      ['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'],
                      ['70', '3e', 'b5', '66', '48', '3', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'],
                      ['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'],
                      ['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']]
        hexWord = hex(word)
        for i in range(2, 10, 2):
            outWord.append(sBoxLookup[int(hexWord[i], 16)][int(hexWord[i+1], 16)])
        return int(''.join(outWord), 16)

    key = [hex(key)[i:i+2] for i in range(2, len(hex(key)), 2)]
    roundConstants = [0x01000000, 0x02000000, 0x04000000, 0x08000000,
                      0x10000000, 0x20000000, 0x40000000, 0x80000000]
    N = 8
    keyWords = [int(key[i]+key[i+1]+key[i+2]+key[i+3], 16) for i in range(0, len(key), 4)]
    R = 15
    expandedKey = []
    for i in range(4*R):
        if i < N:
            expandedKey.append(keyWords[i])
        elif i % N == 0:
            oldKey = expandedKey[i-N]
            subbedKey = subWord(rotWord(expandedKey[i-1]))
            const = roundConstants[i//N]
            expandedKey.append(oldKey ^ subbedKey ^ const)
        elif i % N == 4:
            oldKey = expandedKey[i - N]
            subbedKey = subWord(expandedKey[i - 1])
            expandedKey.append(oldKey ^ subbedKey)
        else:
            expandedKey.append(expandedKey[i-N] ^ expandedKey[i-1])
    return expandedKey


key = 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
print(len(keyExpansion(key)))