

def bobelkowe(Tablica):
    for j in range(len(Tablica)-1):
        for i in range(len(Tablica)-1):
            k=i+1
            if Tablica[i] > Tablica[i+1]:
                tmp=Tablica[i]
                Tablica[i]=Tablica[i+1]
                Tablica[i+1]=tmp





def szybkie(lewy,prawy,Tablica):
    i=int((lewy+prawy)/2)
    piwot=Tablica[i]
    Tablica[i]=Tablica[prawy]
    j=lewy
    i=lewy
    while i<prawy:
        if Tablica[i]<piwot:
                tmp=Tablica[i]
                Tablica[i]=Tablica[j]
                Tablica[j]=tmp
                j=j+1
        i=i+1
    Tablica[prawy]=Tablica[j]
    Tablica[j]=piwot
    if lewy<j-1:
        szybkie(lewy,j-1,Tablica)
    if j+1<prawy:
        szybkie(j+1,prawy,Tablica)
    


def main():
    print("liczby przed sortowaniem")
    Tablica = [3,4,51,6,1,12,6,56,32,1,7,34]
    print(Tablica)
    szybkie(0,len(Tablica)-1,Tablica)
    print("posortowaniu (sortowanie szybkie)")
    print(Tablica)
    print("liczby przed posortowaniem")
    Tablica = [4,5,7,23,1,6,13,1,3,672,1,42,4]
    print(Tablica)
    print("posortowaniu (sortowanie bąbelkowe)")
    bobelkowe(Tablica)
    print(Tablica)


main()
