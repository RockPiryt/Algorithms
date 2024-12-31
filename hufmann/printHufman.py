# Klasa reprezentująca węzeł drzewa Huffmana
class HuffmanNode:
    def __init__(self, freq, letter, left=None, right=None):
        self.freq = freq
        self.letter = letter
        self.left = left
        self.right = right

# Funkcja do drukowania drzewa
def print_tree(node, indent=0):
    if node is None:
        return
    # Dodaj wcięcie dla wizualizacji poziomów
    print("  " * indent + f"({node.letter}, {node.freq})")
    # Rekursywnie drukuj lewe i prawe poddrzewo
    if node.left or node.right:  # Jeśli ma dzieci
        print_tree(node.left, indent + 1)
        print_tree(node.right, indent + 1)

# Przykładowe użycie
frequency_map = {'A': 5, 'B': 9, 'C': 12, 'D': 13, 'E': 16, 'F': 45}
root = generate_tree(frequency_map)  # Funkcja generująca drzewo z kodu

print("Drzewo Huffmana:")
print_tree(root)
