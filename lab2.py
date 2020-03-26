import datetime

def bobelkowe(Tablica,Tablica_ind):
    for j in range(len(Tablica)-1):
        for i in range(len(Tablica)-1):
           
            if Tablica[i] < Tablica[i+1]:
                tmp=Tablica[i]
                Tablica[i]=Tablica[i+1]
                Tablica[i+1]=tmp
                tmp_ind=Tablica_ind[i]
                Tablica_ind[i]=Tablica_ind[i+1]
                Tablica_ind[i+1]=tmp_ind

                

def szybkie(lewy,prawy,Tablica,Tablica_ind):
    i=int((lewy+prawy)/2)
    piwot=Tablica[i]
    Tablica[i]=Tablica[prawy]
    piwot_ind=Tablica_ind[i]
    Tablica_ind[i]=Tablica_ind[prawy]
    j=lewy
    i=lewy
    while i<prawy:
        if Tablica[i]>piwot:
                tmp=Tablica[i]
                Tablica[i]=Tablica[j]
                Tablica[j]=tmp
                tmp=Tablica_ind[i]
                Tablica_ind[i]=Tablica_ind[j]
                Tablica_ind[j]=tmp
                j=j+1
        i=i+1
    Tablica[prawy]=Tablica[j]
    Tablica[j]=piwot
    Tablica_ind[prawy]=Tablica_ind[j]
    Tablica_ind[j]=piwot_ind
    if lewy<j-1:
        szybkie(lewy,j-1,Tablica,Tablica_ind)
    if j+1<prawy:
        szybkie(j+1,prawy,Tablica,Tablica_ind)
    


def szukaj_szyb(Tablica,wartosc):
    Tablica_wynik=[]
    Tablica_wart=[]
    ind=0
    for i in range(len(Tablica)):
        if Tablica[i]>wartosc:
            ind=ind+1
            Tablica_wynik.append(i)
            Tablica_wart.append(Tablica[i])
        if ind == 3:
            szybkie(0,2,Tablica_wart,Tablica_wynik)
            return Tablica_wynik
    return Tablica_wynik


def szukaj_bomb(Tablica,wartosc):
    Tablica_wynik=[]
    Tablica_wart=[]
    ind=0
    for i in range(len(Tablica)):
        if Tablica[i]>wartosc:
            ind=ind+1
            Tablica_wynik.append(i)
            Tablica_wart.append(Tablica[i])
        if ind == 3:
            bobelkowe(Tablica_wart,Tablica_wynik)

            return Tablica_wynik
    return Tablica_wynik



def main():
    print("liczby przed sortowaniem")
    Tablica = [9,1,1,1,0,0,0,8,10,11,14,2132323,24234524]
    print(Tablica)
    print("indeksy boblekowe")
    start =  datetime.datetime.now()
    print(szukaj_bomb(Tablica,2))
    end = datetime.datetime.now()
    total = end - start
    print(total.microseconds,"ms")
    print("indeksy szybkie")
    start =  datetime.datetime.now()
    print(szukaj_szyb(Tablica,2))
    end = datetime.datetime.now()
    total = end - start
    print(total.microseconds,"ms")
 



main()
