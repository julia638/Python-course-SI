import requests
import threading 
import time

def ticker_data_EUR():
    response = requests.get('https://www.bitstamp.net/api/v2/ticker/eurusd/')
    return response.json()
def ticker_data_BTC():
    response = requests.get('https://www.bitstamp.net/api/v2/ticker/btcusd/')
    return response.json()
def ticker_data_BCH():
    response = requests.get('https://www.bitstamp.net/api/v2/ticker/bchusd/')
    return response.json()
def ticker_data_LTC():
    response = requests.get('https://www.bitstamp.net/api/v2/ticker/ltcusd/')
    return response.json()
def ticker_data_XRP():
    response = requests.get('https://www.bitstamp.net/api/v2/ticker/xrpusd/')
    return response.json()

def exchange():
    ticker = ticker_data_EUR()
    sell_EUR = ticker['low']
    buy_EUR = ticker['high']
    ticker = ticker_data_BTC()
    sell_BTC = ticker['low']
    buy_BTC = ticker['high']
    ticker = ticker_data_BCH()
    sell_BCH = ticker['low']
    buy_BCH = ticker['high']
    ticker = ticker_data_LTC()
    sell_LTC = ticker['low']
    buy_LTC = ticker['high']
    ticker = ticker_data_XRP()
    sell_XRP = ticker['low']
    buy_XRP = ticker['high']
    
    data= {'EUR':(float(buy_EUR)-float(sell_EUR))*100/float(sell_EUR),
              'BTC':(float(buy_BTC)-float(sell_BTC))*100/float(sell_BTC),
              'BCH':(float(buy_BCH)-float(sell_BCH))*100/float(sell_BCH),
              'LTC':(float(buy_LTC)-float(sell_LTC))*100/float(sell_LTC),
              'XRP':(float(buy_XRP)-float(sell_XRP))*100/float(sell_XRP)}
    
    table = sorted(data, key=data.get, reverse=True)
    for i in range(5):
        print(table[i],round(data[table[i]],2),"%")


    value=[buy_EUR ,buy_BTC ,buy_BCH ,buy_LTC ,buy_XRP ]
    value2=[sell_EUR ,sell_BTC ,sell_BCH ,sell_LTC ,sell_XRP ]
    return value,value2




def buy_sell_sum(money):   
    data,data2=exchange() 
    data2=sorted(data2, reverse=True)
    for i in range(len(data)):
        if float(money)  > 0:
            if (1/float(data2[i]))*float(money) < float(money) :
                money = float(money)- ((1/float(data2[i]))*float(money))
                print("kupil",float(money) /float(data2[i]))
                print("kasy zostalo",float(money))

            else:
                print("kupil",float(money) /float(data2[i]))
                print("kasy zostalo",float(money))


while True:
    buy_sell_sum(1000)
    time.sleep(300)
    print("Refresh")

