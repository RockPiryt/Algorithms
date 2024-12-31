from collections import Counter
from heapq import heappop, heappush
global str

str = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBCCCCCCCCCCDDDDDEEF'

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


class HuffmanNode:
    def __init__(self, freq, data, left, right):
        self.freq = freq
        self.data =  data
        self.left = left
        self.right = right

# ------------------------------------------------------------drugi sposoób na generowanie drzewa

#utworzenie drzewa Huffmana,
def generate_tree(frequency_map):
    #klucze czyli każda litera z tekstu
    keySet = frequency_map.keys()
    piorityQ = []

    #Tworzenie węzłów: Każda litera z mapy częstotliwości jest zamieniana na węzeł drzewa Huffmana z polami:
    # freq, letter, left, right: Na początku None, bo te węzły nie mają jeszcze dzieci.
    for letter in keySet:
        node = HuffmanNode(frequency_map[letter], letter, None, None)
        piorityQ.append(node)
        #sortowanie kolejki względem freqency rosnąco, Kolejka priorytetowa to struktura danych, 
        #w której elementy są uporządkowane na podstawie pewnego kryterium — tutaj rosnąco według częstotliwości (freq)
    piorityQ = sorted(piorityQ, key = lambda x:x.freq)
    print("Początkowa kolejka która użyjemy do zbudowania drzewa Huffmana:")
    print([(node.freq, node.data) for node in piorityQ])
    
    #Po przygotowaniu kolejki algorytm zaczyna budować drzewo Huffmana, łącząc węzły o najmniejszych częstotliwościach.
    #dopóki mamy chociaż 2 elemeny to mergujemy
    while len(piorityQ) > 1:
        first = piorityQ.pop(0)
        second = piorityQ.pop(0)

        #Tworzenie nowego węzła (merge_node):
        # letter: Symbol '-' oznacza, że ten węzeł nie reprezentuje żadnej konkretnej litery — jest to węzeł pośredni.
        merge_node = HuffmanNode(first.freq + second.freq, '-', first, second)
        #Nowo utworzony węzeł jest dodawany z powrotem do kolejki i kolejka jest ponownie sortowana.
        piorityQ.append(merge_node)
        piorityQ = sorted(piorityQ, key = lambda x:x.freq)

        # Debugowanie: pokaż stan kolejki po każdym merge
        print("Stan kolejki po scaleniu:")
        print([(node.freq, node.letter) for node in piorityQ])
    
    #zwracam ostatni element, czyli korzeń
    return piorityQ.pop(0)


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

#-------------------------------------------------------odczytanie pliku i częstotliowości znaków
f = open('example_text.txt', 'rb')
memory = f.read ()
print(f"odczytane z pliku {memory}")
frequency = Counter(memory)
# print(f"Częstoliwość występownaia znaków {frequency}")
formatted_frequency = {chr(k): v for k, v in frequency.items()}
print(f"Częstotliwość występowania znaków z literami:  {formatted_frequency}")
# -------------------------------------------------------drugi sposób na zliczanie bez counter
def encode(str_text):
    frequency_map = {}
    for letter in str_text:
        frequency_map[letter] = 1
    else:
        frequency_map[letter] += 1

    print(f"Częstotliwość występowania znaków z literami: {frequency_map}")


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


_, root = heappop(heap)

createCodes(root, '')
print(codeMap)
print("\n")


tree=createTreeByte(root)
print("Drzewo hufmana zapisane w bytach")
print(tree)