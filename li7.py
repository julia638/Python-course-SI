import requests
import random
from datetime import datetime, timedelta

from matplotlib.pyplot import *

public_url = "https://poloniex.com/public"


class Diff:
    def __init__(self, data):
        self.max = 0
        self.min = max(data) - min(data)

    def set_min(self, diff):
        if self.min > diff:
            self.min = diff

    def set_max(self, diff):
        if self.max < diff:
            self.max = diff


def analyse(data):
    lower_diff = Diff(data)
    upper_diff = Diff(data)

    lower = 0
    for i in range(len(data) - 1):
        new_diff = calculate_diff(data, i)
        current_data = data[i]
        next_data = data[i + 1]

        if current_data > next_data:
            lower += 1
            lower_diff.set_min(new_diff)
            lower_diff.set_max(new_diff)
        else:
            upper_diff.set_min(new_diff)
            upper_diff.set_max(new_diff)

    lower_diff.max += 1
    upper_diff.max += 1

    probability = lower / len(data)
    new_data = [data[-1]]
    for i in range(0, len(data)):
        if random.choices([0, 1], weights=[probability, 1 - probability])[0] == 0:
            new_data.append(new_data[i - 1] - random.uniform(lower_diff.min, lower_diff.max))
        else:
            new_data.append(new_data[i - 1] + random.uniform(upper_diff.min, upper_diff.max))
    return new_data


def calculate_diff(data, index):
    return abs(data[index] - data[index + 1])


def generate(start_date, pair):
    first_x_data = []
    second_x_data = []
    old_data, times = currency_data(start_date, pair)
    for i in range(len(times)):
        first_x_data.append(to_day_of_month(datetime.utcfromtimestamp(times[i])))

    second_x_data.append(first_x_data[-1])
    for i in range(len(first_x_data)):
        second_x_data.append(to_day_of_month(datetime.now() + timedelta(days=i)))

    averages = [0] * (len(old_data) + 1)
    for i in range(100):
        predicted_data = analyse(old_data)
        for j in range(len(predicted_data)):
            averages[j] += predicted_data[j]

    for i in range(len(averages)):
        averages[i] = averages[i] / 100
    plot(first_x_data, old_data, '#CCFFFF', label='Pobrane dane')
    plot(second_x_data, predicted_data, '#CCCC33', label='Dane przewidywane')
    plot(second_x_data, averages, '#FFCCCC', label='Średnie przewidywane')

    show()


def currency_data(starting_date, currency_pair):
    request = {'command': 'returnChartData',
               'currencyPair': currency_pair,
               'start': (datetime.strptime(starting_date,
                                           '%Y-%m-%d').timestamp()),
               'end': (datetime.now().timestamp()),
               'period': 86400
               }
    response = requests.get(public_url, params=request).json()

    data = []
    dates = []
    for i in response:
        data.append(i['volume'])
        dates.append(i['date'])
    return data, dates


def to_day_of_month(data_time):
    return data_time.strftime('%d/%m')


while True:
    print('1) USDT - ETH')
    print('2) USDT - BTC')
    print("3) USDT - TRX")
    print('q) Koniec')
    print()

    option = input('Wybierz opcję:')

    if option != 'q':
        start_date = input("Wpisz date: YYYY-MM-DD \n")
        if datetime.strptime(start_date, '%Y-%m-%d') > datetime.now():
            print('Data nie mozesz być późniejsza niż dzisiejsza\n')
            option = '0'

    try:
        if option == '1':
            generate(start_date, 'USDT_ETH')

        if option == '2':
            generate(start_date, 'USDT_BTC')

        if option == '3':
            generate(start_date, 'USDT_TRX')

    except NameError:
        print('Data startu nie została zdefiniowana')

    if option == 'q':
        exit('Koniec')