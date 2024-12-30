
from  timeit import default_timer as timer

# mechanizm wstawiania pojedynczego elementu do posortowanej listy
def insert_elem(cabinet, insert_elem):

    check_location = len(cabinet) - 1 # zmienna dla obecnie oglądanego dokumentu, zaczynamy od ostatniego elementu
    global stepcounter
    # wstępnie wstawiany element, jego index ustawiamy na 0 czyli poczatek
    insert_location = 0

    while (check_location >=0): #iterowanie po całej liście
        stepcounter += 1  #krok:przez porównywaniem dokumentów
        #jesli element wstawiany jest wiekszy od sprawdzanego elementu
        if insert_elem > cabinet[check_location]:
            insert_location = check_location + 1 # wkładamy element tuż za obecnie sprawdzana lokalizacja (tutaj ustalamy index)
            check_location = -1
        check_location = check_location -1 # dla while aby iterowało
    
    stepcounter += 1 #krok:wstawiamy element do szafki
    cabinet.insert(insert_location, insert_elem)    # tutaj następuje wkładanie
    return(cabinet)



# funcja sortująca całą listę
def insertion_sort(cabinet):
    #pustą szafke na ulozone dokumenty
    new_cabinet = []

    global stepcounter

    while len(cabinet) >0 :
        stepcounter += 1 #krok:bierzemy element ze starej szafki do wstawienia
        to_insert = cabinet.pop(0) #wybieram i usuwam pierwszy elem. z nieposrotowanej listy
        new_cabinet= insert_elem(new_cabinet, to_insert) # stosuje powyższy mechanizm wstawiania
    return(new_cabinet)


start = timer()
# mam nieposortowana szafkę 
cabinet = [8,4,6,1,2,5,3,7]
stepcounter = 0
sorted_cabinet = insertion_sort(cabinet)
# print(sorted_cabinet)
end = timer()
print(end-start)
print(stepcounter)
