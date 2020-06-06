with open('decodeOutput.txt', 'r') as file:
    data = file.read().split('\n')

data = data[::-1]

with open('decodeOutput.txt', 'w') as file:
    file.write('\n'.join(data))