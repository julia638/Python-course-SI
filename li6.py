import json
import requests

with open('data.json') as file:
    data = json.load(file)


possible_currencies = ['BTC', 'BCH', 'LTC', 'XRP']


def save():
    with open('data.json', 'w') as save_file:
        json.dump(data, save_file)


def add(insert):
    x = insert.split()
    if len(x) != 2:
        print('Niepoprawny format danych')
    else:
        if x[0].upper() in possible_currencies:
            if x[1].isnumeric() and float(x[1]) > 0:
                data[x[0]] = float(x[1])
            else:
                print('Ilość nie jest liczbą lub jest mniejsze od 0. Proszę wpisać jeszcze raz.')
        else:
            print('Zasób [{}] nie istnieje'.format(x[0]))
            print('Możliwe zasoby {}'.format(possible_currencies))


def current_price(currency):
    response_json = requests.get('https://www.bitstamp.net/api/v2/ticker/{}{}'.format(currency.lower(), 'usd')).json()
    return float(response_json['bid'])


def price_24h(currency):
    response_json_24h = requests.get('https://www.bitstamp.net/api/v2/transactions/{}{}/?time=day'.format(currency.lower(), 'usd')).json()
    buys = []
    for buy in response_json_24h:
        if buy['type']== '0':
            buys.append(buy)
    buys.sort(key=by_date)
    return float(buys[0]['price'])


def by_date(current_json):
    return current_json['date']


def currency_calculations():
    for (k, v) in data.items():
        cp = current_price(k)
        now = round(v * cp, 2)
        p= price_24h(k)
        have = round(v*p,2)
        profit = (have/now-1)*100
        print('{:10s} {:7.2} {:10.2f} {:10.2f} {:10.2f}%'.format(k,v, now, have, profit))

def sum():
    suma = 0
    for (k,v)in data.items():
        p= price_24h(k)
        have= round(v*p,2)
        suma = suma + have
    print(suma)
    

while True:
    print()
    print('Witaj w menu')
    print('1) Zaktualizuj zasoby')
    print('2) Pokaz zasoby')
    print('3) Twoj bilans')
    print('4) Całkowita wartości w USD')
    print('q) Koniec')
    print()

    option = input('Wybierz opcję:')

    if option == '1':
        print('Podaj w linii walutę z ilością zasobów np.:')
        print(' BTC 100')
        print('Jeżeli chcesz zakończyć wpisz i zatwierdź q')
        resource = ''
        while resource != 'q':
            resource = input()
            if resource != 'q':
                add(resource)
        save()

    if option == '2':
        print(data)
        print()

    if option == '3':
        print('Wyliczone zyski to:')
        print('{:10s} {:10s} {:7s} {:7s} {:15s}'.format('nazwa','ilosc','tyle bys dostał','tyle dostales', '% zysk/strata'))
        currency_calculations()

    if option == '4':
        print('Tyle wynosi twoja suma') 
        sum()  

    if option == 'q':
        save()
        print('Koniec')
        break
