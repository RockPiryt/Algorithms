import pickle  # Do serializacji słownika binary_codes
global binary_codes
binary_codes ={}

class HuffmanNode:
    def __init__(self, freq, data, left, right):
        self.freq = freq
        self.data =  data
        self.left = left
        self.right = right

#lista kolejkowa w oparciu o min heap
class PiorityQueue:
    def __init__(self, capacity):
        self.storage = [None] * capacity
        self.capacity = capacity
        self.size = 0

    #--------------------------------------------------------pobieranie indexów rodzica i dzieci
    def getParentIndex(self, index):
        return (index - 1) // 2

    def getLeftChildIndex(self, index):
        return 2 * index + 1

    def getRightChildIndex(self, index):
        return 2 * index + 2
    
    #-------------------------------------------------------sprawdzenie posiadania rodzica/dzieci
    def hasParent(self, index):
        #index rodzica musi być większy lub równy 0 (moze być root)
        return self.getParentIndex(index) >= 0

    def hasLeftChild(self, index):
        #index dziecka musi być mniejszy od aktualnej wielkosci kopca
        return self.getLeftChildIndex(index) < self.size

    def hasRightChild(self, index):
        #index dziecka musi być mniejszy od aktualnej wielkosci kopca
        return self.getRightChildIndex(index) < self.size
    
    #--------------------------------------------------------zwracanie wartości na konkretnym indexie rodzica, left i right
    def parent(self,index):
        #wyciagam z listy storage aktualna wartość na wybranym indexie
        return self.storage[self.getParentIndex(index)]
    
    def leftChild(self,index):
        return self.storage[self.getLeftChildIndex(index)]
    
    def rightChild(self,index):
        return self.storage[self.getRightChildIndex(index)]
    
    # -------------------------------------------------------pomocnicze funkcje
    def swap(self, index1, index2):
        self.storage[index1], self.storage[index2] = self.storage[index2], self.storage[index1]

    def resize(self):
        """Podwaja pojemność kopca."""
        self.capacity *= 2
        self.storage.extend([None] * (self.capacity - len(self.storage))) 

    def printHeap(self):
        print("Kopiec:", [(item[0], item[1].data) for item in self.storage[:self.size]])
    # ------------------------------------------------------iteracyjnie wkładanie do stosu
    def insertHeap(self, element):
        if self.size == self.capacity:
            self.resize()  # Zwiększenie rozmiaru kopca
        self.storage[self.size] = element
        self.size += 1
        self.heapifyUp()
    # -----------------------przywracanie własności kopca min idąc w góre (rodzic ma być mniejszy lub równy dzieciom)
    def heapifyUp(self):
        #index wstawianego ostatnio elementu
        index = self.size-1 
        #jeżeli obecny węzeł ma rodzica i rodzic jest większy od tego noda to zrób swap
        while(self.hasParent(index) and self.parent(index) > self.storage[index]):
            self.swap(self.getParentIndex(index), index)
            #kontynuacja w górę swapowania jeżeli potrzeba
            index=self.getParentIndex(index)
    # ------------------------------------------------------iteracyjnie usuwanie ze stosu
    def removeFromHeap(self):
        if self.size == 0:
            raise Exception("Kopiec pusty")
        # usuwany będzie root zawsze (bo to najmniejszy element w kopcu min)
        removed_element = self.storage[0]
        # ustanowienie nowego root, nowym root staje się ostatni element w kopcu
        self.storage[0] = self.storage[self.size - 1]
        self.size -= 1
        # Przywracam własność kopca w dół
        self.heapifyDown()
        return removed_element

    def heapifyDown(self):
        # zaczynam od root bo z tamtąd był usuwany element
        index = 0
        # muszę sprawdzić które dziecko lewe czy prawe a mniejsza wartość i wtedy zamienić z mniejszym dzieckiem 
        while(self.hasLeftChild(index)):
            #pobieram wartość lewego dziecka - narazie zakładam że lewe jest mniejsze
            smallerChildIndex = self.getLeftChildIndex(index)

            # sprawdzam czy prawe dziecko nie jest mniejsze od lewego
            if (self.hasRightChild(index) and self.rightChild(index) < self.leftChild(index)):
                smallerChildIndex= self.getRightChildIndex(index)
            
            #jeśli root mniejszy od dzieci to ok
            if (self.storage[index] < self.storage[smallerChildIndex]):
                break
            else:
                #jeśli jest rodzic większy od dzieci to zamień miejscami
                self.swap(index,smallerChildIndex)
            # przywracanie własności ma iść do końca jeżeli potrzeba, więc ustawiam smallerChildIndex jako index do kolejnego sprawdzenia
            index = smallerChildIndex


def save_text_to_file(file_name):
    # Pobranie tekstu od użytkownika
    user_input = input("Podaj tekst, który chcesz zapisać do pliku: ")

    # Zapis tekstu do pliku
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(user_input)
        print(f"Tekst został zapisany do pliku: {file_name}")
    except Exception as e:
        print(f"Wystąpił błąd podczas zapisu do pliku: {e}")


#-------------------------------------------------------odczytanie pliku i częstotliowości znaków
def count_letters_in_file(file_path):
    try:
        # Otwieranie pliku i odczyt jego zawartości
        with open(file_path, 'r', encoding='utf-8') as file:
            str_text = file.read()

        # Tworzenie mapy częstotliwości
        frequency_map = {}
        for letter in str_text:
            if letter.isalpha():  # Uwzględniamy tylko litery
                if letter not in frequency_map:
                    frequency_map[letter] = 1
                else:
                    frequency_map[letter] += 1
        return frequency_map

    except FileNotFoundError:
        print(f"Błąd: Plik {file_path} nie został znaleziony.")
        return None
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return None
    
#-------------------------------------------Utworzenie drzewa Huffmana
def generate_tree(frequency_map):
    keySet = frequency_map.keys()
    piorityQ = []

    #Tworzenie węzłów: Każda litera z mapy częstotliwości jest zamieniana na węzeł drzewa Huffmana
    for letter in keySet:
        node = HuffmanNode(frequency_map[letter], letter, None, None)
        piorityQ.append(node)
        #sortowanie kolejki względem freqency rosnąco
    piorityQ = sorted(piorityQ, key = lambda x:x.freq)
    print("Początkowa kolejka która użyjemy do zbudowania drzewa Huffmana:")
    print([(node.freq, node.data) for node in piorityQ])
    
    # Po przygotowaniu kolejki algorytm zaczyna budować drzewo Huffmana, łącząc węzły o najmniejszych częstotliwościach.
    while len(piorityQ) > 1:
        first = piorityQ.pop(0)
        second = piorityQ.pop(0)
        merge_node = HuffmanNode(first.freq + second.freq, '-', first, second)

        #Nowo utworzony węzeł jest dodawany z powrotem do kolejki i kolejka jest ponownie sortowana.
        piorityQ.append(merge_node)
        piorityQ = sorted(piorityQ, key = lambda x:x.freq)

        # Debugowanie: pokaż stan kolejki po każdym merge
        print("Stan kolejki po scaleniu:")
        print([(node.freq, node.data) for node in piorityQ])
    
    #zwracam ostatni element, czyli korzeń
    return piorityQ.pop(0)

def generate_tree_with_heap(frequency_map):
    # Tworzenie kolejki priorytetowej na podstawie klasy PiorityQueue
    priority_queue = PiorityQueue(len(frequency_map))

    # Tworzenie węzłów i dodawanie ich do kolejki priorytetowej
    for letter, freq in frequency_map.items():
        node = HuffmanNode(freq, letter, None, None)
        priority_queue.insertHeap((freq, node))

    print("Początkowa kolejka, którą użyjemy do zbudowania drzewa Huffmana:")
    priority_queue.printHeap()

    # Po przygotowaniu kolejki algorytm zaczyna budować drzewo Huffmana, łącząc węzły o najmniejszych częstotliwościach
    while priority_queue.size > 1:
        # Usunięcie dwóch najmniejszych elementów
        first = priority_queue.removeFromHeap()[1]  # Pobierz węzeł
        second = priority_queue.removeFromHeap()[1]

        # Tworzenie nowego węzła (merge_node)
        merge_node = HuffmanNode(first.freq + second.freq, '-', first, second)

        # Dodanie nowego węzła z powrotem do kolejki
        priority_queue.insertHeap((merge_node.freq, merge_node))

        # Debugowanie: pokaż stan kolejki po każdym scaleniu
        print("Stan kolejki po scaleniu:")
        priority_queue.printHeap()

    # Zwracam korzeń drzewa Huffmana
    return priority_queue.removeFromHeap()[1]


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
            # Jeśli nie jest liściem, dodajemy jego dzieci do stosu z odpowiednimi kodami
            if current.right:
                stack.append((current.right, code + '1'))
            if current.left:
                stack.append((current.left, code + '0'))

def create_compressed_file(original_file_path , compressed_file_path):
    frequency_map = count_letters_in_file(original_file_path)
    print(f"Częstotliwość występowania znaków z literami: {frequency_map}")

    # Utworzenie drzewa Huffmana na podstawie frequency_map
    root = generate_tree_with_heap(frequency_map)

    #  Utworzenie słownika kodów binarnych dla każdego znaku z tekstu
    set_binary_code_iterative(root)
    sorted_binary_codes = dict(sorted(binary_codes.items(), key=lambda x: ord(x[0])))
    print(f"Słownik kodów binarnych: {sorted_binary_codes}")


def decompress_file(compressed_file_path, decompressed_file_path):
    with open(compressed_file_path, 'rb') as compressed_file:
        # Odczytanie nagłówka (słownika binary_codes)
        binary_codes = pickle.load(compressed_file)
        # Odczytanie danych skompresowanych
        compressed_data = compressed_file.read()
    
    # Odwrócenie słownika (wartości na klucze)
    reverse_codes = {v: k for k, v in binary_codes.items()}
    
    # Konwersja bajtów na ciąg binarny
    binary_string = ''.join(f'{byte:08b}' for byte in compressed_data)
    
    # Odtworzenie oryginalnego tekstu
    decoded_text = ''
    current_code = ''
    for bit in binary_string:
        current_code += bit
        if current_code in reverse_codes:
            decoded_text += reverse_codes[current_code]
            current_code = ''
    
    # Zapisanie tekstu do pliku dekompresji
    with open(decompressed_file_path, 'w', encoding='utf-8') as decompressed_file:
        decompressed_file.write(decoded_text)
    
    print(f"Dekompresowany plik zapisano jako: {decompressed_file_path}")

   
    
if __name__ == "__main__":   
    original_file_path = '1original_text.txt'
    compressed_file_path = '2compressed_text.txt'
    decompressed_file_path = '3decompressed_text.txt'

    #zapisanie tekstu do pliku txt
    # save_text_to_file(original_file_path)

    # Tworzenie skompresowanego pliku
    create_compressed_file(original_file_path , compressed_file_path)

    # Dekompresja pliku
    # decompress_file(compressed_file_path, decompressed_file_path)

    
