def swap(array, x, y):
    """Zamiana dwóch elementów w tablicy."""
    array[x], array[y] = array[y], array[x]


def quicksort(array):
    """Główna funkcja QuickSort jako wrapper."""
    quicksort_recursion(array, 0, len(array) - 1)


def quicksort_recursion(array, low, high):
    """Rekurencyjna funkcja sortująca."""
    if low < high:
        pivot_index = partition(array, low, high)
        quicksort_recursion(array, low, pivot_index - 1)  # Sortowanie przed pivotem
        quicksort_recursion(array, pivot_index + 1, high)  # Sortowanie za pivotem


def partition(array, low, high):
    """Funkcja dzieląca tablicę na podtablice na podstawie pivotu."""
    pivot_value = array[high]  # Wybieramy ostatni element jako pivot
    i = low
    for j in range(low, high):
        if array[j] <= pivot_value:  # Jeśli bieżący element jest <= pivot
            swap(array, i, j)  # Zamiana elementów
            i += 1
    swap(array, i, high)  # Zamiana pivotu na właściwą pozycję
    return i


if __name__ == "__main__":
    a = [10, 11, 23, 44, 8, 15, 3, 9, 12, 45, 56, 45, 45]
    quicksort(a)  # Uruchomienie funkcji sortującej

    # Wypisanie wyniku
    for elem in a:
        print(elem)
