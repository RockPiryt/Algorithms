#1.mechanizm wstawiania pojedynczego elementu do posortowanej listy

# funcja wstawiająca
def insert_elem(cabinet, insert_elem):

    check_location = len(cabinet) - 1 # zmienna dla obecnie oglądanego dokumentu, zaczynamy od ostatniego elementu

    # wstępnie wstawiany element, jego index ustawiamy na 0 czyli poczatek
    insert_location = 0

    while (check_location >=0): #iterowanie po całej liście
        #jesli element wstawiany jest wiekszy od sprawdzanego elementu
        if insert_elem > cabinet[check_location]:
            insert_location = check_location + 1 # wkładamy element tuż za obecnie sprawdzana lokalizacja (tutaj ustalamy index)
            check_location = -1
        check_location = check_location -1 # dla while aby iterowało

    cabinet.insert(insert_location, insert_elem)    # tutaj następuje wkładanie
    return(cabinet)



# Stoje przed posortowaną szafką i ktoś daje mi dokument 5 do włożenia
#mam rosnąco posrtowana liste (na koncu najwiekszy element) i element do wstawienia
cabinet = [1,2,3,4,6,8,12]
new_cabinet = insert_elem(cabinet, 7)
print(new_cabinet)