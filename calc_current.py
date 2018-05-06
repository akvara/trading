import sys
from datetime import datetime

import csv
from utils import process_currency

NUMBER_OF_COLS = 13
ERRORS = {
    'columns': 'Number of columns must be {}\n(date, op_type, ticker, quantity, price, commission, op_sum, ...)'.format(
        NUMBER_OF_COLS)
}
OPERATION_TYPES = {
    'PURCHASE': 'purchase',
    'SALE': 'sale',
}


class Operation:
    def __init__(self, date, op_type, ticker, quantity, price, commission, op_sum):
        self.date = date
        self.op_type = op_type
        self.ticker = ticker
        self.quantity = quantity
        self.price = price
        self.commission = commission
        self.op_sum = op_sum

    def __repr__(self):
        return repr((self.date.strftime("%Y-%m-%d %H:%M:%S"), self.op_type, self.ticker))


def data_error(line_nr, row, error_key):
    sys.stdout.write("Error on line {}: {} \nData was: {}\n\n".format(line_nr, ERRORS[error_key], row))
    sys.exit(-1)


def process_type(text, line_nr):
    if text.strip() == 'Pirkimo sandoris':
        return OPERATION_TYPES['PURCHASE']
    if text.strip() == 'Pardavimo sandoris':
        return OPERATION_TYPES['SALE']
    sys.stdout.write("Error on line {}: wrong operation type {}".format(line_nr, text))
    sys.exit(-1)


# def process_description(text):
#     for operation_type in OPERATION_TYPES:
#         try:
#             text.index(operation_type['text'])
#             return operation_type['key']
#         except ValueError:
#             pass
#     return text[:LINE_LENGTH]
#
#

#
# def print_result(array):
#     for (key, value) in array:
#         descr = [item['description'] for item in OPERATION_TYPES if item['key'] == key]
#         description = descr[0] if len(descr) > 0 else key
#         sys.stdout.write("{}\t\t{}\n".format(int(value), description))
#
#
# def print_report(dictionary, sort_column):
#     sys.stdout.write("-" * 40 + "\n")
#     print_result(sorted(dictionary.items(), key=operator.itemgetter(sort_column)))
#     # print_result(sorted(dictionary.items(), key=operator.itemgetter(sort_column)))
#     sys.stdout.write("-" * 40 + "\n\n")
#
#
def read_data(input_file):
    with open(input_file, 'r') as csv_input:
        reader = csv.reader(csv_input, delimiter=',', quotechar='"')
        line_nr = 0
        data_array = []
        for row in reader:
            print(row)
            line_nr += 1
            if len(row) != NUMBER_OF_COLS:
                data_error(line_nr, row, 'columns')
            date = datetime.strptime(row[0], '%y-%m-%d %H:%M')
            op_type = process_type(row[1], line_nr)
            ticker = row[2]
            quantity = row[3]
            price = process_currency(row[4])
            commission = process_currency(row[5])
            op_sum = process_currency(row[6])

            data_array.append(Operation(date, op_type, ticker, quantity, price, commission, op_sum))
            if line_nr > 50:
                s = sorted(data_array, key=lambda operation: operation.date, reverse=True)
                print(s)
                exit(0)

        total_balance = 0
        sys.stdout.write("Total balance: {}€\n".format(int(total_balance)))


if __name__ == '__main__':
    if not len(sys.argv) == 2:
        sys.stdout.write("Usage: {} file_name\n".format(sys.argv[0]))
        sys.exit(-1)
    read_data(sys.argv[1])
