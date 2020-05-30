import requests
import random
from datetime import datetime, timedelta
from matplotlib.pyplot import *


def get_data(starting_date, currency_pair):
    request = {'command': 'returnChartData',
               'currencyPair': currency_pair,
               'start': (datetime.strptime(starting_date,
                                           '%Y-%m-%d').timestamp()),
               'end': (datetime.now().timestamp()),
               'period': 86400
               }
    response = requests.get("https://poloniex.com/public", params=request).json()

    data = []
    dates = []
    for i in response:
        data.append(i['volume'])
        dates.append(i['date'])
    return data, dates


def analyse(data):
    lower = 0
    max_lower_diff = 0
    max_upper_diff = 0
    min_lower_diff = max(data) - min(data)
    min_upper_diff = max(data) - min(data)

    for i in range(len(data) - 1):
        if data[i] > data[i + 1]:
            lower += 1
            if min_lower_diff > abs(data[i] - data[i + 1]):
                min_lower_diff = abs(data[i] - data[i + 1])
            if max_lower_diff  < abs(data[i] - data[i + 1]):
                max_lower_diff  = abs(data[i] - data[i + 1])
        else:
            if min_upper_diff > abs(data[i] - data[i + 1]):
               min_upper_diff = abs(data[i] - data[i + 1])
            if max_upper_diff < abs(data[i] - data[i + 1]):
                max_upper_diff = abs(data[i] - data[i + 1])

    max_lower_diff += 1
    max_upper_diff += 1
    probability = lower / len(data)
    new_data = [data[-1]]
    for i in range(0, len(data)):
        if random.choices([0, 1], weights=[probability, 1 - probability])[0] == 0:
            new_data.append(new_data[i - 1] - random.uniform(min_lower_diff, max_lower_diff))
        else:
            new_data.append(new_data[i - 1] + random.uniform(min_upper_diff, max_upper_diff))
    return new_data


def generate(start_date, pair):
    data_set_1 = []
    data_set_2 = []
    old_data, times = get_data(start_date, pair)
    for i in range(len(times)):
        data_set_1.append(to_month_day(datetime.utcfromtimestamp(times[i])))

    data_set_2.append(data_set_1[-1])
    for i in range(len(data_set_1)):
        data_set_2.append(to_month_day(datetime.now() + timedelta(days=i)))

    averages = [0] * (len(old_data) + 1)
    for i in range(100):
        predicted_data = analyse(old_data)
        for j in range(len(predicted_data)):
            averages[j] += predicted_data[j]

    for i in range(len(averages)):
        averages[i] = averages[i] / 100
    plot(data_set_1, old_data, 'c')
    plot(data_set_2, averages, 'r')
    plot(data_set_2, predicted_data, 'y')
    
    show()


def to_month_day(data_time):
    return data_time.strftime('%m-%d')


while True:
    print('1) USDT - ETH')
    print('2) USDT - BTC')
    print("3) USDT - TRX")
    print('q) Koniec')
    print()

    option = input('Wybierz opcję:')

    start_date = input("Wpisz date: YYYY-MM-DD \n")

    if option == '1':
        generate(start_date, 'USDT_ETH')

    if option == '2':
        generate(start_date, 'USDT_BTC')

    if option == '3':
        generate(start_date, 'USDT_TRX')

    if option == 'q':
        exit('Koniec')