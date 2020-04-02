import requests
def bitbay_orderbook_data():
    response = requests.get("https://bitbay.net/API/Public/BTC/EUR/orderbook.json")
    return response.json()

def cex_ticker_data():
    response = requests.get('https://cex.io/api/ticker/BTC/EUR')
    return response.json()

def blockchain_ticker_data():
    response = requests.get("https://blockchain.info/ticker")
    return response.json()

bitbay_orderbook = bitbay_orderbook_data()
oferty_sprzedarzy = bitbay_orderbook['bids']  
oferty_kupna = bitbay_orderbook['asks']

print('Lista pierwszych 15 ofert: \n Kupna:')
for i in oferty_kupna[:15]:
    print(i)

print('sprzedaży:')
for i in oferty_sprzedarzy[:15]:
    print(i)

print("."*50)

cex_ticker = cex_ticker_data()
cex_sprzedarz = cex_ticker['bid']
cex_kupno = cex_ticker['ask']

blockchain_ticker = blockchain_ticker_data()
blockchain_kupno = blockchain_ticker['EUR']['buy']
blockhain_spedarz = blockchain_ticker['EUR']['sell']

print("Porównywarka")
if cex_kupno < blockchain_kupno:
    print('Bardziej opłaca sie kupić bitcoiny na Euro w bitbay',cex_kupno)
else:
    print('Bardziej opłaca się kupić bitcoiny na Euro w blockchain',blockchain_kupno)

if cex_sprzedarz > blockhain_spedarz :
    print('Drozej sprzedaż bitcoiny na EUR w bitbay',cex_sprzedarz)
else:
    print('Drozej sperzedaz bitcoiny na EUR w blockchain',blockhain_spedarz)

