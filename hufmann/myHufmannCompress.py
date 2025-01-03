import pickle
import os

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


#-------------------------------------------------------odczytanie pliku 
def read_file(file_path):
    try:
        # Otwieranie pliku i odczyt jego zawartości
        with open(file_path, 'r', encoding='utf-8') as file:
            str_text = file.read()
            return str_text

    except FileNotFoundError:
        print(f"Błąd: Plik {file_path} nie został znaleziony.")
        return None
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return None  
    
#------------------------------------------------------zliczenie częstotliwości znaków
def create_frequency_map(str_text):

        # Tworzenie mapy częstotliwości
        frequency_map = {}
        for letter in str_text:
            if letter.isalpha():  # Uwzględniamy tylko litery
                if letter not in frequency_map:
                    frequency_map[letter] = 1
                else:
                    frequency_map[letter] += 1
        return frequency_map
    
#-------------------------------------------Utworzenie drzewa Huffmana
def generate_tree_with_heap(frequency_map):
    # Tworzenie kolejki priorytetowej na podstawie klasy PiorityQueue
    priority_queue = PiorityQueue(len(frequency_map))

    # Tworzenie węzłów i dodawanie ich do kolejki priorytetowej
    for letter, freq in frequency_map.items():
        node = HuffmanNode(freq, letter, None, None)
        priority_queue.insertHeap((freq, node))

    print("Początkowa kolejka piorytetowa, którą użyjemy do zbudowania drzewa Huffmana:")
    priority_queue.printHeap()

    # Po przygotowaniu kolejki algorytm zaczyna budować drzewo Huffmana, łącząc węzły o najmniejszych częstotliwościach
    while priority_queue.size > 1:
        # Usunięcie dwóch najmniejszych elementów
        first = priority_queue.removeFromHeap()[1]  
        second = priority_queue.removeFromHeap()[1]

        # Tworzenie nowego węzła (merge_node)
        merge_node = HuffmanNode(first.freq + second.freq, '-', first, second)

        # Dodanie nowego węzła z powrotem do kolejki
        priority_queue.insertHeap((merge_node.freq, merge_node))

        print("Stan kolejki piorytetowej po scaleniu:")
        priority_queue.printHeap()

    # Zwracam korzeń drzewa Huffmana
    return priority_queue.removeFromHeap()[1]

# Utworzenie kodów binarnych dla każdego znaku
def set_binary_code_iterative(node):
    if node is None:
        return
    
    stack = [(node, '')]  
    
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


# Utworzenie drzewa w wersji bytowej
def createTreeByteIterative(root):
    if root is None:
        return b''

    result = b''
    stack = [(root, False)]  

    while stack:
        node, visited = stack.pop()

        if node.left is None and node.right is None:
            # Węzeł liścia: dodaj '0' i wartość znaku
            result += b'0' + node.data.encode('utf-8')
        else:
            if visited:
                # Węzeł wewnętrzny po odwiedzeniu dzieci: dodaj '1'
                result += b'1'
            else:
                # Węzeł wewnętrzny przed odwiedzeniem dzieci: dodaj ponownie na stos jako odwiedzony
                stack.append((node, True))
                if node.right:
                    stack.append((node.right, False))
                if node.left:
                    stack.append((node.left, False))

    return result

#----------------------------------------------------------Kompresja danych
# Zmiana tekstu na kod zerojedynkowy stosując kody Huffmana
def create_encoded_text(str_text, code_map):
    encodedText = ""

    for character in str_text:
        encodedText += code_map[character]
    return encodedText

#zapis tekstu zerojedynkowego do pliku
def save_encoded_text(encoded_text,  output_file):
    with open(output_file, 'w', encoding='utf-8') as zero_one_text:
        zero_one_text.write(encoded_text)
    
    print(f"Tekst zapisany stosując kody Huffmana  w pliku: {output_file}")

# Dodanie padding do encoded_text (teskt zapisany zerojedynkowo) żeby mógł być podzielny przez 8
def pad_encoded_text(encoded_text):
    #określenie potrzbnego dopełeninia 0 gdy teskt nie jest podzielny przez 8
    extra_padding = 8 - len(encoded_text) % 8
    if extra_padding == 8:
        extra_padding = 0
    # Dodanie informacji o dopełnieniu jako 8-bit string
    padded_info = f"{extra_padding:08b}"
    padded_encoded_text = encoded_text + '0' * extra_padding
    # Połącz informację o paddingu (8 pierwszych znaków) z zakodowanym tekstem
    return padded_info + padded_encoded_text

# funkcja dzieląca tekst zapisany bitowo na bajty
def create_byte_array(padded_encoded_text):
    #sprawdzenie czy padded encoded text jest podzielny prze 8
    if len(padded_encoded_text) % 8 != 0:
        raise ValueError("Padded encoded text length is not a multiple of 8.")
    #podział bitów na bajty
    byte_array = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i+8]
        byte_array.append(int(byte, 2))
    return bytes(byte_array)

# funkcja kompresująca 
def compress(encoded_text):
    # Dodanie dopelenienia żeby był podzielny przez 8
    padded_encoded_text = pad_encoded_text(encoded_text)
    # Podział bitów na bajty
    return create_byte_array(padded_encoded_text)


# Zapisanie kodów Huffmana i teksty w postaci binarnej do pliku
def save_compressed_data(compressed_file_path, code_map, compressed_data):
    with open(compressed_file_path, 'wb') as output:
        # Serializacja mapy kodów Huffmana
        pickle.dump(code_map, output)
        output.write(compressed_data)


# -------------------------------------------------------------Dekompresja danych
# Usuwanie paddingu
def remove_padding(padded_encoded_text):
    # Pobranie 8 bitów jako informacja o paddingu
    padded_info = padded_encoded_text[:8]
    # Konwersja informacji o paddingu z binarnej na liczbę całkowitą
    extra_padding = int(padded_info, 2)
    # Usuń informację o paddingu i same bity paddingu
    encoded_text = padded_encoded_text[8:-extra_padding] if extra_padding > 0 else padded_encoded_text[8:]
    return encoded_text

#Dekompresja na podstawie kodów hHuffmana zapisanych w pliku
def decompress(compressed_data, reverse_code_map):
    # Konwersja bajtów na ciąg bitów
    bit_string = ''.join(f"{byte:08b}" for byte in compressed_data)
    
    # Usunięcie paddingu w celu uzyskania oryginalnego zakodowanego tekstu
    encoded_text = remove_padding(bit_string)
    
    # Dekodowanie zakodowanego tekstu przy użyciu odwróconej mapy kodów
    current_code = ''
    decoded_text = []
    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_code_map:
            character = reverse_code_map[current_code]
            decoded_text.append(character)
            current_code = ''
    
    return ''.join(decoded_text)



# TODO
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

# TODO
def compare_files(original_file_path, compressed_file_path):
    try:
        # Odczyt oryginalnego pliku tekstowego
        with open(original_file_path, 'r', encoding='utf-8') as original_file:
            original_content = original_file.read()

        # Podwojenie zawartości oryginalnego pliku
        doubled_content = original_content * 2

        # Zapis podwojonej zawartości do tymczasowego pliku
        temp_file_path = 'temp_doubled_file.txt'
        with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
            temp_file.write(doubled_content)

        # Pobranie rozmiarów plików
        original_size = os.path.getsize(temp_file_path)
        compressed_size = os.path.getsize(compressed_file_path)

        # Porównanie rozmiarów plików
        print(f"Rozmiar podwojonego pliku oryginalnego: {original_size} bajtów")
        print(f"Rozmiar skompresowanego pliku binarnego: {compressed_size} bajtów")

        if original_size > compressed_size:
            print("Podwojony plik oryginalny jest większy niż skompresowany plik binarny.")
        elif original_size < compressed_size:
            print("Skompresowany plik binarny jest większy niż podwojony plik oryginalny.")
        else:
            print("Oba pliki mają ten sam rozmiar.")

        # Usunięcie tymczasowego pliku
        os.remove(temp_file_path)

    except FileNotFoundError as e:
        print(f"Błąd: {e}")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")


    
# Konwertuje zakodowany tekst na dane bajtowe na podstawie mapy kodów Huffmana.
def bits_to_byte2(code_map, encoded_text):

    byte_array = bytearray()
    current_byte = 0
    packed = 0

    # Iteracja po danych wejściowych
    for char in encoded_text:
        code = code_map[char]  # Pobranie kodu binarnego dla znaku
        for bit in code:  # Przejście przez każdy bit kodu
            # Przesunięcie bieżącego bajtu w lewo i dodanie nowego bitu
            current_byte = (current_byte << 1) | int(bit)
            packed += 1

            # Jeśli bajt jest pełny (8 bitów), dodaj go do byte_array
            if packed == 8:
                byte_array.append(current_byte)
                # Zeruję liczniki
                current_byte = 0
                packed = 0

    # Dodanie ostatniego niepełnego bajtu (jeśli istnieje)
    if packed > 0:
        current_byte <<= (8 - packed)  # Uzupełnij pozostałe bity zerami
        byte_array.append(current_byte)

    # Zwraca obiekt bytes reprezentujący skompresowane dane
    return bytes(byte_array)


def bits_to_byte(encoded_text):
    byte_array = bytearray()
    current_byte = 0
    packed = 0

    # Iterate over each bit in the encoded text
    for bit in encoded_text:
        # Shift the current byte left and add the new bit
        current_byte = (current_byte << 1) | int(bit)
        packed += 1

        # If we've packed 8 bits, append the byte to the array
        if packed == 8:
            byte_array.append(current_byte)
            current_byte = 0
            packed = 0

    # If there are remaining bits, pad with zeros and append
    if packed > 0:
        current_byte <<= (8 - packed)  # Pad the remaining bits with zeros
        byte_array.append(current_byte)

    return bytes(byte_array)

if __name__ == "__main__":   
    original_file_path = '1original_text.txt'
    string_codes_file_path = '2string_codes_text.txt'
    compressed_file_path = '3compressed_text.bin'
    decompressed_file_path = '4decompressed_text.txt'

    #zapisanie pobranego tekstu do pliku txt
    # save_text_to_file(original_file_path)

    str_text= read_file(original_file_path)
    print(f"Odczytany tekst: {str_text}")
    freq_map=create_frequency_map(str_text)
    print(f"Częstotliwość występowania znaków z literami: {freq_map}")

    # Utworzenie drzewa Huffmana na podstawie frequency_map
    root = generate_tree_with_heap(freq_map)

    # --------------------------------------------Tworzenie słownika kodów Huffmana
    set_binary_code_iterative(root)
    code_map = dict(sorted(binary_codes.items(), key=lambda x: ord(x[0])))
    print(f"Słownik kodów binarnych: {code_map}")

    # -----------------------------------------------------Kompresja danych
    # Oryginalny tekst przekształcony na zerojedynkowy stosując kody Huffmana  
    encoded_text = create_encoded_text(str_text, code_map)
    print(f"Oryginalny tekst przekształcony na zerojedynkowy stosując kody Huffmana: {encoded_text}")

    # Dodanie padding do tekstu oraz podzial bitów na bajty
    compressed_data = compress(encoded_text)

    # Zapis wybranych danych do pliku binarnego
    save_compressed_data(compressed_file_path, code_map, compressed_data)

    # ----------------------------------------------------------------Dekompresja
    reverse_code_map = {v: k for k, v in code_map.items()}
    print(f"Słownik kodów binarnych służący do dekompresji: {code_map}")

    decompressed_text = decompress(compressed_data, reverse_code_map)

    print(f"Original Text: {str_text}")
    print(f"Decompressed Text: {decompressed_text}")

    # -----------------------------------------------------------Porównanie wielkości plików
    # compare_files(original_file_path, compressed_file_path)






















    # # Konwertuje zakodowany tekst (zerojedynkowy) na dane bajtowe na podstawie mapy kodów Huffmana.
    # text_bytes = bits_to_byte(code_map, encoded_text)
    #-----------------------------------------------------------
    # tree_bytes = createTreeByteIterative(root)
    # print(f"Drzewo Huffmana zapisane w bajtach {tree_bytes}")
    # tree_length = len(tree_bytes)
    
    #zeroOne = saveTextZeroOne(original_file_path, string_codes_file_path, code_map)
    #print(f"Oryginalny tekst przekształcony na zerojedynkowy stosując kody Huffmana - wersja ZeroOne: {zeroOne}")


    # compress_and_write(compressed_file_path, tree_length, tree_bytes, code_map, str_text)

    # Dekompresja pliku
    # decompress_file(compressed_file_path, decompressed_file_path)


