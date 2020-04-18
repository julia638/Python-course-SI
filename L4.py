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

def exchange():
    bitbay_ticker = bitbay_ticker_data()
    bitbay_buy=bitbay_ticker['ask']
    bitbay_sell=bitbay_ticker['bid']

    cex_ticker = cex_ticker_data()
    cex_sell = cex_ticker['bid']
    cex_buy = cex_ticker['ask']

    blockchain_ticker = blockchain_ticker_data()
    blockchain_buy = blockchain_ticker['USD']['buy']
    blockhain_sell = blockchain_ticker['USD']['sell']

    bitstamp_ticker = bitstamp_ticker_data()
    bitstamp_buy=float(bitstamp_ticker['ask'])
    bitstamp_sell=float(bitstamp_ticker['bid'])

    taker = [1.03,1.05,1.024,1.025]
    data= [['bitbay',bitbay_sell,bitbay_buy,4],
              ['cex',cex_sell,cex_buy,9],
              ['blockchain',blockhain_sell,blockchain_buy,14],
              ['bitstamp',bitstamp_sell,bitstamp_buy,19]]
    
    for i in range(len(taker)):
      data[i][1] = data[i][1]*taker[i]*0.3
      data[i][2] = data[i][2]*(2-taker[i])*0.3
    print(data)
    indexmin=0
    indexmax=0
    max= data[0][2]
    max_name_buy=data[0][0]
    for i in range (len(data)):
        if data[i][2]>= max :
            indexmax=data[i][3]
            max = data[i][2]
            max_name_buy =data[i][0]

    for i in range(len(data)):
        if max_name_buy!= data[i][0]:
            min= data[i][1]

    min_name_sell=data[1][0]
    for i in range(len(data)):
        if max_name_buy!= data[i][0]:
            if data[i][1]<= min :
                indexmin = data[i][3]
                min = data[i][1]
                min_name_sell = data[i][0]
    
    zysk= 0
    if max>min :
        zysk= max-min     
        print("Na giełdzie", max_name_buy, "można sprzedać 0.3 BTC za USD ", max,"a kupić w ",min_name_sell,"za",min, "przy tym zyskujesz",zysk)
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
            print("Nie można dokonać arbitrażu : Brak srodkow na koncie!")
        wallet_file.close()
    else : 
        print( "Nie można dokonać arbitrażu")
   
   
exchange()

