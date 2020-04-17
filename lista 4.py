import requests
import numpy
def bitbay_ticker_data():
    response = requests.get("https://bitbay.net/API/Public/BTC/USD/ticker.json")
    return response.json()

def cex_ticker_data():
    response = requests.get('https://cex.io/api/ticker/BTC/USD')
    return response.json()

def blockchain_ticker_data():
    response = requests.get("https://blockchain.info/ticker")
    return response.json()

def bitstamp_ticker_data():
    response = requests.get("https://www.bitstamp.net/api/ticker")
    return response.json()

def sprzedarz_kupno_ticker():
    bitbay_ticker = bitbay_ticker_data()
    bitbay_buy=bitbay_ticker['ask']
    bitbay_sell=bitbay_ticker['bid']

    cex_ticker = cex_ticker_data()
    cex_sprzedarz = cex_ticker['bid']
    cex_kupno = cex_ticker['ask']

    blockchain_ticker = blockchain_ticker_data()
    blockchain_kupno = blockchain_ticker['USD']['buy']
    blockhain_sprzedarz = blockchain_ticker['USD']['sell']

    bitstamp_ticker = bitstamp_ticker_data()
    bitstamp_buy=float(bitstamp_ticker['ask'])
    bitstamp_sell=float(bitstamp_ticker['bid'])

    taker = [1.03,1.05,1.024,1.025]
    tablica= [['bitbay',bitbay_sell,bitbay_buy,4],['cex',cex_sprzedarz,cex_kupno,9],['blockchain',blockhain_sprzedarz,blockchain_kupno,14],['bitstamp',bitstamp_sell,bitstamp_buy,19]]
    
    for i in range(len(taker)):
      tablica[i][1] = tablica[i][1]*taker[i]*0.3
      tablica[i][2] = tablica[i][2]*(2-taker[i])*0.3
    print(tablica)
    indexmin=0
    indexmax=0
    max= tablica[0][2]
    max_nazwa_kupno=tablica[0][0]
    for i in range (len(tablica)):
        if tablica[i][2]>= max :
            indexmax=tablica[i][3]
            max = tablica[i][2]
            max_nazwa_kupno =tablica[i][0]

    for i in range(len(tablica)):
        if max_nazwa_kupno!= tablica[i][0]:
            min= tablica[i][1]

    min_nazwa_sprzedarz=tablica[1][0]
    for i in range(len(tablica)):
        if max_nazwa_kupno!= tablica[i][0]:
            if tablica[i][1]<= min :
                indexmin = tablica[i][3]
                min = tablica[i][1]
                min_nazwa_sprzedarz = tablica[i][0]
    
    print(indexmax)
    print(indexmin)
    zysk= 0
    if max>min :
        zysk= max-min
        
        print("sprzedaj 0.3 BTC w", max_nazwa_kupno, "za", max,"kup w ",min_nazwa_sprzedarz,"za",min, "zyskujesz",zysk)
        wallet_file = open('D:\gitreprezetoria\Python-course-SI\wallet.txt','r+')
        wallet = wallet_file.readlines()
        if  float(wallet[indexmax+2])>0.3 and float(wallet[indexmin])>min:
            wallet[1]=str(float(wallet[1]) + zysk )+"\n"
            wallet[indexmax+2]=str(float(wallet[indexmax+2])-0.3)+"\n"
            wallet[indexmax]=str(float(wallet[indexmax])+max)+"\n"
            wallet[indexmin+2]=str(float(wallet[indexmin+2])+0.3)+"\n"
            wallet[indexmin]=str(float(wallet[indexmin])-min)+"\n"
            wallet_file.seek(0)
            wallet_file.writelines(wallet)
        else:
            print("brak srodkow na koncie")
        wallet_file.close()
    else : 
        print( "Nie można dokonać arbitrażu")
        
    
    print(max)
    print(max_nazwa_kupno)
    print(min)
    print(min_nazwa_sprzedarz)
    print(zysk)
   
    
   
sprzedarz_kupno_ticker()

