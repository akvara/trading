import operator
import sys
from datetime import datetime

import csv

NUMBER_OF_COLS = 6
ERRORS = {
    'columns': 'Number of columns must be {}\n(date, ticker, amount, purchase, commission, sale)'.format(NUMBER_OF_COLS)
}
OPERATION_TYPES = [
    # {
    #     'text': 'UAB NEO FINANCE',
    #     'key': 'UAB NEO FINANCE',
    #     'description': 'UAB NEO FINANCE'
    # },
    {
        'text': 'Lėšų nurašymas: Sąskaitos LT317044064000061387 tvarkymo mokestis už ',
        'key': 'tvarkymo',
        'description': 'Sąskaitos LT317044064000061387 tvarkymo mokestis'
    },
    {
        'text': 'mokėtojas ANDRIUS KVARACIEJUS',
        'key': 'savo',
        'description': 'Į savo sąskaitą'
    },
    {
        'text': 'mokėtojas Andrius Kvaraciejus',
        'key': 'savo',
        'description': 'Į savo sąskaitą'
    },
    {
        'text': 'gavėjas Andrius Kvaraciejus',
        'key': 'savo',
        'description': 'Į savo sąskaitą'
    },
    {
        'text': 'Komisinis mokestis už lėšų įskaitymą',
        'key': 'banko',
        'description': 'Banko komisiniai'
    },
    {
        'text': 'Komisinis mokestis už pervedimą banko viduje',
        'key': 'banko',
        'description': 'Banko komisiniai'
    },
    {
        'text': 'Lėšų įskaitymas: Pardavimas ',
        'key': 'pardavimas',
        'description': 'VP pardavimas'
    },
    {
        'text': 'Lėšų nurašymas: Pirkimas ',
        'key': 'pirkimas',
        'description': 'VP pirkimas'
    },
    {
        'text': 'Lėšų įskaitymas: Dividendai už ',
        'key': 'dividendai',
        'description': 'Dividendai'
    },
    {
        'text': 'Lėšų pervedimas banko viduje: Alimentai už Tomą, ',
        'key': 'Tomui',
        'description': 'Alimentai už Tomą'
    },
    {
        'text': 'gavėjas Kristina Kvaraciejūtė, asm. kod.: 49706180559,',
        'key': 'Kristinai',
        'description': 'Alimentai Kristinai'
    },
    {
        'text': 'Lėšų įskaitymas: Dividendai ',
        'key': 'dividendai',
        'description': 'Dividendai'
    },
    {
        'text': 'Lėšų nurašymas: Paslaugų plano ',
        'key': 'plano',
        'description': 'Paslaugų plano mokestis'
    },
    {
        'text': ' gavėjas UAB "Viena sąskaita"',
        'key': 'Viena sąskaita',
        'description': 'Viena sąskaita'
    },
    {
        'text': 'VP saugojimo ir pervedimo mokesčiai',
        'key': 'saugojimo',
        'description': 'VP saugojimo ir pervedimo mokesčiai'
    },
    {
        'text': 'SEB gyvybės draudimas',
        'key': 'gyvybės_draudimas',
        'description': 'SEB gyvybės draudimas'
    },
    {
        'text': 'Bitė Lietuva',
        'key': 'Bitė',
        'description': 'Bitė Lietuva'
    },
    {
        'text': 'Indrės Aleksiejūnienės įmonė',
        'key': 'implantavimas',
        'description': 'Implantavimas'
    },
]
LINE_LENGTH = 140


def data_error(line_nr, row, error_key):
    sys.stdout.write("error on line {}: {} \nData was: {}\n\n".format(line_nr, ERRORS[error_key], row))
    sys.exit(-1)


def process_description(text):
    for operation_type in OPERATION_TYPES:
        try:
            text.index(operation_type['text'])
            return operation_type['key']
        except ValueError:
            pass
    return text[:LINE_LENGTH]


def process_currency(item, delimiter_thous='.', delimiter_dec=','):
    value = item.replace(' €', '').replace(delimiter_thous, '').replace(delimiter_dec, '.')
    if not value:
        value = 0
    return float(value)


def print_result(array):
    for (key, value) in array:
        descr = [item['description'] for item in OPERATION_TYPES if item['key'] == key]
        description = descr[0] if len(descr) > 0 else key
        sys.stdout.write("{}\t\t{}\n".format(int(value), description))


def print_report(dictionary, sort_column):
    sys.stdout.write("-" * 40 + "\n")
    print_result(sorted(dictionary.items(), key=operator.itemgetter(sort_column)))
    # print_result(sorted(dictionary.items(), key=operator.itemgetter(sort_column)))
    sys.stdout.write("-" * 40 + "\n\n")


def read_data(input_file):
    with open(input_file, 'r') as csv_input:
        reader = csv.reader(csv_input, delimiter=',', quotechar='"')
        line_nr = 0
        aggregator = dict()
        for row in reader:
            line_nr += 1
            if len(row) != NUMBER_OF_COLS:
                data_error(line_nr, row, 'columns')

            # date = datetime.strptime(row[0], '%Y-%M-%d')
            description = process_description(row[1])
            money_out = process_currency(row[2])
            money_in = process_currency(row[3])
            if description not in aggregator:
                aggregator[description] = 0
            aggregator[description] += money_in - money_out

        print_report(aggregator, 1)

        total_balance = 0
        without_trading = 0
        for item in aggregator.items():
            total_balance += item[1]
            if not (item[0] in ['pirkimas' , 'pardavimas']):
                without_trading += item[1]
        sys.stdout.write("Total balance: {}€\n".format(int(total_balance)))
        sys.stdout.write("Without trading: {}€\n\n".format(int(without_trading)))


if __name__ == '__main__':
    if not len(sys.argv) == 2:
        sys.stdout.write("Usage: {} file_name\n".format(sys.argv[0]))
        sys.exit(-1)
    read_data(sys.argv[1])
