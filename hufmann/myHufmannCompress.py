# import pickle  # Do serializacji słownika binary_codes
global binary_codes
binary_codes ={}

class HuffmanNode:
    def __init__(self, freq, data, left, right):
        self.freq = freq
        self.data =  data
        self.left = left
        self.right = right


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
    root = generate_tree(frequency_map)

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

    # Tworzenie skompresowanego pliku
    create_compressed_file(original_file_path , compressed_file_path)

    # Dekompresja pliku
    # decompress_file(compressed_file_path, decompressed_file_path)
