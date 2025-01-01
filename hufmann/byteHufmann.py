from collections import Counter
from heapq import heappop, heappush

#-------------------------------------------------------odczytanie pliku i częstotliowości znaków
f = open('example_text.txt', 'rb')
memory = f.read ()
print(f"odczytane z pliku {memory}")
frequency = Counter(memory)
# print(f"Częstoliwość występownaia znaków {frequency}")
formatted_frequency = {chr(k): v for k, v in frequency.items()}
print(f"Częstotliwość występowania znaków z literami:  {formatted_frequency}")


class Node:
    def __init__(self, freq, value, code='', left=None, right=None):
        self.left = left
        self.right = right
        self.freq = freq
        self.value = value
        self.isLeaf = False
        self.code = code

    def __lt__(self, other):
        return self.freq < other.freq
    
    def __str__(self):
        return f"Node(freq={self.freq}, value={self.value})"


def createTreeByte(root):
    if root.isLeaf:
        return b'0' + root.value.to_bytes(1, 'little')
    return createTreeByte(root.left) + createTreeByte(root.right) +b'1'

#---------------------------------------------------------------------Funkcja do tworzenia kodów
codeMap = {}     
def createCodes(root,code):
    # jeśli brak liści 
    # if not root.left and not root.right:
    if root.isLeaf:
        root.code=code
        codeMap[root.value] = code
        return
    # jeśli jest lewa i prawa gałąź 
    createCodes(root.left, code + '0')
    createCodes(root.right, code + '1')



#--------------------------------------------Tworze kopiec znaków wraz z ich częstotliwością
heap=[]

# #Sprawdzenie wypychania 1 znaku na górę kopca
# for letter in frequency:
#     heappush(heap, (frequency[letter], letter )) tutaj wypychałam tuple, wiec jeden obiekt z 2 wartosciami
# print(heap[1])

# ------------------------------------------Tutaj stowrzyłam kopiec liter z labelami frequency
#Sprawdzenie wypychania 1 znaku klasy node na górę kopca
for letter in frequency:
    # heappush(heap, (frequency[letter], Node(frequency[letter], letter )))
    leaf = Node(frequency[letter], letter)
    leaf.isLeaf = True
    heappush(heap, (frequency[letter], leaf))

# print("Print heapa jako obiektu\n")
# print(heap)
print("Print noda jako obiektu") 
print(heap[0][1])#Node(freq=1, value=70)
# print("frequency dla 0 obiektu, 1 oznacza Node(frequency[letter], letter ) bo tupla")  
# print(heap[0][1].freq)

# left=letter1
# right=letter2
while len(heap) >=2:
    frequency1, left = heappop(heap)
    frequency2, rigth = heappop(heap)

    frequency_sum = frequency1 +  frequency2
    node = Node(frequency_sum, -1, '',  left, rigth)
    heappush(heap, (node.freq, node))

print("Nowy kopiec po while")
print(heap[0][1])
print(f"długość kopca {len(heap)}")

#-------------------------------------------------------------------------------
# _, root = heappop(heap)

# createCodes(root, '')
# print(codeMap)
# print("\n")


# tree=createTreeByte(root)
# print("Drzewo hufmana zapisane w bytach")
# print(tree)

# out = open('output.pk', 'wb')
# #Najpierw zapisujemy długość drzewa (w bajtach) jako liczbę 4-bajtową
# out.write(len(tree).to_bytes(4, 'little'))
# out.write(tree)


# byte = 0
# packed = 0

# for b in memory: 
#     code = codeMap[b]
#     for bit in code:
#         if packed == 0:
#             out.write(byte)
#             byte = 0
#             packed = 0
#         if bit == '1':
#             byte |= 1
#         byte <<=1
#         packed <<=1

# if packed < 8:
#     out.write(byte)

#---------------------------------------------------------------------------------------------------------
_, root = heappop(heap)  # Pobierz korzeń drzewa Huffmana z kopca

createCodes(root, '')  # Utwórz mapę kodów Huffmana
print("Mapa kodów Huffmana:", codeMap)
print("\n")

# Utworzenie drzewa w formacie bajtowym
tree = createTreeByte(root)
print("Drzewo Huffmana zapisane w bajtach")
print(tree)

# Otwórz plik do zapisu
with open('output.bin', 'wb') as out:
    # Zapisz długość drzewa (4 bajty, little-endian)
    out.write(len(tree).to_bytes(4, 'little'))
    # Zapisz samo drzewo w bajtach
    out.write(tree)

    # ---------------------Kodowanie danych na podstawie mapy kodów Huffmana
    byte = 0      # Aktualny bajt w trakcie budowy
    packed = 0    # Liczba bitów w bieżącym bajcie

    for b in memory:  # Iteracja po danych wejściowych
        code = codeMap[b]  # Pobierz kod binarny dla bajtu
        for bit in code:  # Przejdź przez każdy bit kodu
            byte = (byte << 1) | int(bit)  # Przesuń bajt w lewo i dodaj bit
            packed += 1  # Zwiększ licznik zapisanych bitów

            # Jeśli bajt jest pełny, zapisz go do pliku
            if packed == 8:
                out.write(byte.to_bytes(1, 'big'))
                byte = 0
                packed = 0

    # Zapisz ostatni niepełny bajt (jeśli istnieje)
    if packed > 0:
        byte = byte << (8 - packed)  # Uzupełnij pozostałe bity zerami
        out.write(byte.to_bytes(1, 'big'))
