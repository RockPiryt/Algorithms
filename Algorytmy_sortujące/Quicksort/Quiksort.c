// Optymistycznie 0(nlogn)
// Pesymistycznie O(n^2)
#include <stdio.h>

void swap (int *x, int *y); 
void quicksort(int array[], int length); // główna funkcja, jako wrapper
void quicksor_recursion(int array[], int low, int high); // do sortowania subarrays
int partition(int array[], int low, int high); // odpowiada za podział na subarrays

int main()
{
    int a[] = {10,11,23,44,8,15,3,9,12,45,56,45,45};
    int length = 13;
    quicksort(a, length); // uruchomienie głownej funkcji sortującej

    //printowanie wyniku
    for (int i=0; i<length; i++)
    {
        printf("%d", a[i]);
        printf("\n");
    }

    return 0;
}

void swap (int *x, int *y)
{
    int temp = *x;
    *x=*y;
    *y=temp;
}

void quicksort(int array[], int length) // jako wrapper dla funkcji quicksor_recursion
{   
    quicksor_recursion(array, 0, length-1); //skąd dokąd chcemy srotować, teraz chcemy sortować cała liste
}

void quicksor_recursion(int array[], int low, int high)
{
    if (low < high)
    {
        int pivot_index = partition(array,low,high);
        quicksor_recursion(array, low, pivot_index-1); // sortowanie subarrays przed pivot
        quicksor_recursion(array, pivot_index+1, high);// sortowanie subarrays za pivot 
    }
}

int partition(int array[], int low, int high)
{
    int  pivot_value = array[high];/// teraz pivot wyznaczam jako ostatni element 
    int i=low;
    for (int j=low; j < high; j++)
    {
        if (array[j]<= pivot_value) // kiedy obecnie porównywany obiekt jest większy lub równy pivot_Value dokonaj swap, i++ oraz j+++
        {
            swap(&array[i],&array[j]);// zamieniam i<->j
            i++;
        }
    }
    swap(&array[i], &array[high]); // zamieniam i <-> pivot w ostatnim ruchu
    return i;
}





