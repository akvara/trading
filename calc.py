import operator
import sys

# from datetime import datetime

import csv

NUMBER_OF_COLS = 6
ERRORS = {
    'columns': 'Number of columns must be {}\n(date, ticker, amount, purchase, commission, sale)'.format(NUMBER_OF_COLS)
}


def data_error(line_nr, row, error_key):
    sys.stdout.write("error on line {}: {} \nData was: {}\n\n".format(line_nr, ERRORS[error_key], row))
    sys.exit(-1)


def process_currency(item, delimiter_thous='.', delimiter_dec=','):
    value = item.replace(' €', '').replace(delimiter_thous, '').replace(delimiter_dec, '.')
    if not value:
        value = 0
    return float(value)


def process_name(name):
    starts = name.index('(ISIN')
    ends = name.index(')')
    temp = name[:starts] + name[ends + 1:]
    return temp. \
        replace(',,', '"'). \
        replace('"', ''). \
        replace(',', ''). \
        replace('AB ', ''). \
        replace('AS ', ''). \
        replace('JSC ', ''). \
        replace(' PVA', '')


def print_result(dictionary):
    for (key, value) in dictionary:
        sys.stdout.write("{}\t{}\n".format(int(value), key))


def print_report(by, dictionary, sort_column):
    sys.stdout.write("By {}\n".format(by))
    print_result(sorted(dictionary.items(), key=operator.itemgetter(sort_column)))
    sys.stdout.write("-" * 40 + "\n\n")


def read_data(input_file):
    with open(input_file, 'r') as csv_input:
        reader = csv.reader(csv_input, delimiter=',', quotechar='"')
        line_nr = 0
        profit_aggregator = dict()
        trades_aggregator = dict()
        for row in reader:
            line_nr += 1

            if len(row) != NUMBER_OF_COLS:
                data_error(line_nr, row, 'columns')

            # date = datetime.strptime(row[0], '%Y %M %d')
            ticker = process_name(row[1])
            # amount = row[2]
            purchase = process_currency(row[3])
            commission = process_currency(row[4])
            sale = process_currency(row[5])
            if ticker not in profit_aggregator:
                profit_aggregator[ticker] = 0
                trades_aggregator[ticker] = 0
            profit_aggregator[ticker] += purchase - commission - sale
            trades_aggregator[ticker] += 1

        print_report("ticker name", profit_aggregator, 0)
        print_report("trades", trades_aggregator, 1)
        print_report("profit", profit_aggregator, 1)

        sum = 0
        for key, value in profit_aggregator.items():
            sum += value
        sys.stdout.write("Total result: {}€\n".format(int(sum)))


if __name__ == '__main__':
    if not len(sys.argv) == 2:
        sys.stdout.write("Usage: {} file_name\n".format(sys.argv[0]))
        sys.exit(-1)
    read_data(sys.argv[1])
