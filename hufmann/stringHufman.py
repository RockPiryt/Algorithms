from collections import Counter
from heapq import heappop, heappush

global my_str
global binary_codes
my_str = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBCCCCCCCCCCDDDDDEEF'
binary_codes ={}

class HuffmanNode:
    def __init__(self, freq, data, left, right):
        self.freq = freq
        self.data =  data
        self.left = left
        self.right = right

# ------------------------------------------------------------ sposoób na generowanie drzewa

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
        print([(node.freq, node.data) for node in piorityQ])
    
    #zwracam ostatni element, czyli korzeń
    return piorityQ.pop(0)

#-------------------------------------funkcja do tworzenia kodów
# def set_binary_code(node, current_code):
#     if not node is None:
#         if node.left is None and node.right is None:
#             binary_codes[node.data] = current_code

#             #left
#             current_code += '0'
#             set_binary_code(node.left, current_code)
#             current_code = current_code[:-1]

#             #right
#             current_code += '1'
#             set_binary_code(node.right, current_code)
#             current_code = current_code[:-1]    

def set_binary_code(node, current_code):
    if node is None:
        return
    # Jeśli węzeł jest liściem, dodaj jego kod
    if node.left is None and node.right is None:
        binary_codes[node.data] = current_code
        return

    # Rekurencyjne wywołanie dla lewego i prawego dziecka
    set_binary_code(node.left, current_code + '0')
    set_binary_code(node.right, current_code + '1')

def set_binary_code_iterative(node):
    if node is None:
        return
    
    stack = [(node, '')]  # Stos zawiera pary (węzeł, kod_binarny)
    
    while stack:
        current, code = stack.pop()
        
        # Jeśli jest liściem, przypisz kod binarny
        if current.left is None and current.right is None:
            binary_codes[current.data] = code
        else:
            # Jeśli nie jest liściem, dodajemy jego dzieci do stosu:
            # Prawe dziecko z kodem code + '1'.
            # Lewe dziecko z kodem code + '0'.
            if current.right:
                stack.append((current.right, code + '1'))
            if current.left:
                stack.append((current.left, code + '0'))



# -------------------------------------------------------drugi sposób na zliczanie bez counter
def encode(str_text):
    # Create a frequency map
    frequency_map = {}
    for letter in str_text:
        if letter not in frequency_map:
            frequency_map[letter] = 1
        else:
            frequency_map[letter] += 1

    print(f"Częstotliwość występowania znaków z literami (funkcja encode): {frequency_map}")

    # Creating a Huffman Tree from a frequency map
    root = generate_tree(frequency_map)

    #  Generating binary codes for each character
    # set_binary_code(root, '')
    set_binary_code_iterative(root)
    print(binary_codes)

    print(' char | huffman code' )

    for letter in frequency_map:
        print('%-4r | %12s ' % (letter, binary_codes[letter]))
        # print( letter, binary_codes[letter])

    s = ''
    for c in str_text:
        s += binary_codes[c]
    return s

print(encode(my_str))
