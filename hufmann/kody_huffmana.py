
import os
import json
import re


# Piority queue (Min heap)

# iteriation

class MinHeap:
    def __init__(self,capacity):
        self.storage = [0] * capacity #wszystkie jako 0
        self.capacity = capacity #wielkość kopca
        self.size = 0 #początkowa wielkość kopca


    #--------------------------------------------------------pobieranie indexów rodzica i dzieci
    def getParentIndex(self, index):
        return (index-1)//2 
    
    def getLeftChildIndex(self,index):
        return 2 * index + 1
    
    def getRightChildIndex(self,index):
        return 2 * index + 2
    
    #-------------------------------------------------------sprawdzenie posiadania rodzica/dzieci
    def hasParent(self,index):
        #index rodzica musi być większy lub równy 0 (moze być root)
        return self.getParentIndex(index) >= 0
    
    def hasLeftChild(self,index):
        #index dziecka musi być mniejszy od aktualnej wielkosci kopca
        return self.getLeftChildIndex(index) < self.size
    
    def hasRighhtChild(self,index):
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
    def isFull(self):
        return self.size == self.capacity
    
    def swap(self, index1, index2):
        temp = self.storage[index1]
        self.storage[index1] = self.storage[index2]
        self.storage[index2] = temp
    
    
    # ------------------------------------------------------iteracyjnie wkładania do stosu
    # wkładanie do stosu 
    def insertHeap(self,element):
        if (self.isFull()):
            raise("Kopiec pełny")
        #wstawienie elementu na ostatnim miejscu kopca
        self.storage[self.size] = element
        self.size += 1
        # przywrócenie własności kopca min
        self.heapifyUp()

    # przywracanie wlasnoci kopca min idać w góre (rodzic ma być mniejszy lub równy dzieciom)
    def heapifyUp(self):
        #index wstawianego ostatnio elementu
        index = self.size-1 
        #jeżeli obecny węzeł ma rodzica i rodzic jest większy od tego noda to zrób swap
        while(self.hasParent(index) and self.parent(index) > self.storage[index]):
            self.swap(self.getParentIndex(index), index)
            #kontynuacja w górę swapowania jeżeli potrzeba
            index=self.getParentIndex(index)

     # ------------------------------------------------------iteracyjnie usuwanie ze stosu
    # usuwanie ze stosu 
    def removeFromHeap(self):
        # Gdy kopiec pusty
        if(self.size == 0):
            raise("Kopiec pusty")
        
        # Kopiec zawiera elementy
        # usuwany będzie root zawsze (bo to najmniejszy element w kopcu min)
        removedElement = self.storage[0]  
        # ustanowienie nowego root, nowym root staje się ostatni element w kopcu
        self.storage[0] = self.storage[self.size - 1]
        self.size -= 1
        # Przywracam własność kopca w dół
        self.heapifyDown()

        #zwrot co zostało usuniete
        return removedElement
    
    def heapifyDown(self):
        # zaczynam od root bo z tamtąd był usuwany element
        index = 0
        # muszę sprawdzić które dziecko lewe czy prawe a mniejsza wartość i wtedy zamienić z mniejszym dzieckiem 
        # musi mieć dziecko jak ma być przywracana własność (jak ma prawe to ma też lewe (musi byc kompletnym drzewem binarnym), dlatego sprawdzam tylko czy ma lewe)
        while(self.hasLeftChild(index)):
            #pobieram wartość lewego dziecka - narazie zakładam że lewe jest mniejsze
            smallerChildIndex = self.getLeftChildIndex(index)

            # sprawdzam czy prawe dziecko nie jest mniejsze od lewego
            if (self.hasRighhtChild(index) and self.rightChild(index) < self.leftChild(index)):
                smallerChildIndex= self.getRightChildIndex(index)
            
            #jeśli root mniejszy od dzieci to ok
            if (self.storage[index] < self.storage[smallerChildIndex]):
                break
            else:
                #jeśli jest rodzic większy od dzieci to zamień miejscami
                self.swap(index,smallerChildIndex)
            # przywracanie własności ma iść do końca jeżeli potrzeba, więc ustawiam smallerChildIndex jako index do kolejnego sprawdzenia
            index = smallerChildIndex
    

def calculate_frequencies(file_path):
    """Wczytuje plik i zlicza wystąpienia wszystkich znaków w tekście, używając słownika."""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Wyrażenie regularne, które dopasowuje wszystkie znaki
    filtered_text = re.findall(r'.', text)  # Dopasowuje każdy znak

    # Tworzymy pusty słownik do przechowywania wyników
    frequencies = {}

    # Zliczamy wystąpienia każdego znaku
    for char in filtered_text:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1

    return text, frequencies


def build_huffman_tree(frequencies):
    """Tworzy drzewo Huffmana na podstawie częstotliwości znaków przy użyciu MinHeap."""
    # Tworzymy kopiec o rozmiarze odpowiadającym liczbie znaków
    min_heap = MinHeap(len(frequencies))

    # Wstawiamy do kopca krawędzie (elementy) zawierające znak i jego częstotliwość
    for char, weight in frequencies.items():
        min_heap.insertHeap([weight, [char, ""]])

    while min_heap.size > 1:
        # Pobieramy dwa najmniejsze elementy
        lo = min_heap.removeFromHeap()
        hi = min_heap.removeFromHeap()

        # Dodajemy '0' i '1' do kodów odpowiednio dla pierwszego i drugiego elementu
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]

        # Łączymy je w jeden węzeł i wkładamy z powrotem do kopca
        min_heap.insertHeap([lo[0] + hi[0]] + lo[1:] + hi[1:])

    # Pobieramy drzewo Huffmana z kopca i sortujemy po długości kodu
    huffman_tree = sorted(min_heap.removeFromHeap()[1:], key=lambda p: (len(p[-1]), p))
    return huffman_tree


def create_huffman_codes(huffman_tree):
    """Tworzy słownik kodów Huffmana."""
    return {char: code for char, code in huffman_tree}

def compress_file(input_path, output_path):
    """Szyfruje plik za pomocą kodów Huffmana."""
    # Wczytanie pliku i zliczenie znaków
    text, frequencies = calculate_frequencies(input_path)

    # Tworzenie drzewa Huffmana
    huffman_tree = build_huffman_tree(frequencies)
    huffman_codes = create_huffman_codes(huffman_tree)

    # Kodowanie tekstu
    encoded_text = ''.join(huffman_codes[char] for char in text)

    # Tworzenie nagłówka
    header = json.dumps(huffman_codes)

    # Zapisywanie skompresowanego pliku
    with open(output_path, "wb") as f:
        header_bytes = header.encode('utf-8')
        header_length = len(header_bytes)

        # Zapis nagłówka
        f.write(header_length.to_bytes(4, 'big'))
        f.write(header_bytes)

        # Zapis zakodowanego tekstu
        byte_array = bytearray()
        for i in range(0, len(encoded_text), 8):
            byte = encoded_text[i:i+8]
            byte_array.append(int(byte, 2))
        f.write(byte_array)

def decompress_file(input_path, output_path):
    """Deszyfruje plik skompresowany kodami Huffmana."""
    with open(input_path, "rb") as f:
        # Odczyt nagłówka
        header_length = int.from_bytes(f.read(4), 'big')
        header = json.loads(f.read(header_length).decode('utf-8'))

        # Odczyt zakodowanego tekstu
        encoded_text = ''
        byte = f.read(1)
        while byte:
            encoded_text += f"{bin(ord(byte))[2:]:0>8}"
            byte = f.read(1)

    # Odwrócenie słownika Huffmana
    reverse_huffman_codes = {code: char for char, code in header.items()}

    # Dekodowanie tekstu
    decoded_text = ''
    buffer = ''
    for bit in encoded_text:
        buffer += bit
        if buffer in reverse_huffman_codes:
            decoded_text += reverse_huffman_codes[buffer]
            buffer = ''

    # Zapisanie odszyfrowanego pliku
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(decoded_text)

# Przykład użycia
if __name__ == "__main__":
    input_file = "plik.txt"
    compressed_file = "zaszyfrowany_plik.txt"
    decompressed_file = "deszyfrowany_plik.txt"

    compress_file(input_file, compressed_file)
    decompress_file(compressed_file, decompressed_file)

    # Sprawdzenie rozmiarów plików
    original_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(compressed_file)
    decompressed_size = os.path.getsize(decompressed_file)

    print(f"Rozmiar oryginalnego pliku: {original_size} bajtów")
    print(f"Rozmiar skompresowanego pliku: {compressed_size} bajtów")
    print(f"Rozmiar odszyfrowanego pliku: {decompressed_size} bajtów")

    # Sprawdzenie zgodności plików
    with open(input_file, "r", encoding="utf-8") as f:
        original_text = f.read()

    with open(decompressed_file, "r", encoding="utf-8") as f:
        decompressed_text = f.read()

    assert original_text == decompressed_text, "Odszyfrowany tekst nie jest zgodny z oryginalnym!"
    print("Sukces! Plik został poprawnie zaszyfrowany i odszyfrowany.")

