import requests
import random
from datetime import datetime, timedelta

from matplotlib.pyplot import *

public_url = "https://poloniex.com/public"
date_format = '%Y-%m-%d'


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


def generate(start_date, middle_date, end_date, pair):
    first_x_data = []
    second_x_data = []
    old_data, times = currency_data(start_date, middle_date, pair)
    real_data, ignored = currency_data(middle_date, end_date, pair)

    for i in range(len(times)):
        first_x_data.append(to_day_of_month(datetime.utcfromtimestamp(times[i])))

    second_x_data.append(first_x_data[0])
    for i in range(len(first_x_data)):
        second_x_data.append(to_day_of_month(start_date + timedelta(days=i)))

    averages = [0] * (len(old_data) + 1)
    for i in range(100):
        predicted_data = analyse(old_data)
        for j in range(len(predicted_data)):
            averages[j] += predicted_data[j]

    for i in range(len(averages)):
        averages[i] = averages[i] / 100

    average_diff = []
    single_data_diff = []

    for i in range(len(averages)):
        average_diff.append(abs(real_data[i] - averages[i]))
        single_data_diff.append(abs(real_data[i] - predicted_data[i]))

    plot(second_x_data, predicted_data, '#CCCC33', label='Dane przewidywane')
    plot(second_x_data, averages, '#FFCCCC', label='Średnie przewidywane')
    plot(second_x_data, real_data)
    show()

    plot(second_x_data, average_diff, '#CCCC33', label='Średnie')
    plot(second_x_data, single_data_diff, '#FFCCCC', label='Odchylenie')
    plot(second_x_data, real_data)
    show()


def currency_data(starting_date, ending_date, currency_pair):
    request = {'command': 'returnChartData',
               'currencyPair': currency_pair,
               'start': (starting_date.timestamp()),
               'end': (ending_date.timestamp()),
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
        start_date = datetime.strptime(input("Wpisz początkową date: YYYY-MM-DD \n"), date_format)
        if start_date >= datetime.now():
            print('Data początku musi być wcześniejsza niż dzisiejsza\n')
            option = '0'

        end_date = datetime.strptime(input("Wpisz końcową date: YYYY-MM-DD \n"), date_format)
        if end_date > datetime.now():
            print('Data nie może być późniejsza niż dzisiejsza\n')
            option = '0'

        delta = end_date - start_date
        old_start_date = start_date - timedelta(days=delta.days - 1)

    try:
        if option == '1':
            generate(old_start_date, start_date, end_date, 'USDT_ETH')

        if option == '2':
            generate(old_start_date, start_date, end_date, 'USDT_BTC')

        if option == '3':
            generate(old_start_date, start_date, end_date, 'USDT_TRX')

    except NameError:
        print('Daty nie zostały poprawnie zdefiniowane')

    if option == 'q':
        exit('Koniec')