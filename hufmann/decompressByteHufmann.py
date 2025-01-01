encoded = open('output.pk', 'rb')
data = encoded.read()

print(data)

treeSize = int.from_bytes(data[0:4], 'little')
print(treeSize)