import sys
from datetime import datetime
import os
import csv
from utils import process_currency, print_report

HISTORY_FILES_DIR = '/home/andrius/MEGA/OMX/SEB/'
HISTORY_FILES_PREFIX = 'Trades'
NUMBER_OF_COLS = 13
ERRORS = {
    'columns': 'Number of columns must be {}\n(date, op_type, ticker, quantity, price, commission, op_sum, ...)'.format(
        NUMBER_OF_COLS)
}


class OPERATION_TYPES:
    PURCHASE = 'purchase'
    SALE = 'sale'


class Operation:
    def __init__(self, date, op_type, quantity, price, commission, op_sum, settlement):
        self.date = date
        self.op_type = op_type
        self.quantity = quantity
        self.price = price
        self.commission = commission
        self.op_sum = op_sum
        self.settlement = settlement

    def __repr__(self):
        # self.date.strftime("%Y-%m-%d %H:%M")
        return "{} {} {} {}".format(self.settlement.strftime("%Y-%m-%d"), self.op_type, self.quantity, self.price)


def data_error(line_nr, row, error_key):
    sys.stdout.write("Error on line {}: {} \nData was: {}\n\n".format(line_nr, ERRORS[error_key], row))
    sys.exit(-1)


def process_type(text, line_nr):
    if text.strip() == 'Pirkimo sandoris':
        return OPERATION_TYPES.PURCHASE
    if text.strip() == 'Pardavimo sandoris':
        return OPERATION_TYPES.SALE
    sys.stdout.write("Error on line {}: wrong operation type {}".format(line_nr, text))
    sys.exit(-1)


def calculate_profit(ticker_ops, date_from, date_to):
    started = False
    profit = 0
    sold_balance = 0
    for op in ticker_ops:
        # print(op)
        if date_from <= op.settlement <= date_to and op.op_type == OPERATION_TYPES.SALE:
            started = True
            profit += op.op_sum
            sold_balance += op.quantity
            # print("balance", sold_balance)
        if started and sold_balance > 0 and op.op_type == OPERATION_TYPES.PURCHASE:
            if sold_balance - op.quantity <= 0:
                cost = op.op_sum / op.quantity * sold_balance
                profit -= cost
                sold_balance -= sold_balance
                # print("balance", sold_balance)
                break
            profit -= op.op_sum
            sold_balance -= op.quantity
            # print("balance", sold_balance)
    return profit, sold_balance


def read_data(input_files):
    aggregator = {}
    for input_file in input_files:
        sys.stdout.write("Reading file {} ...\n".format(input_file))
        with open(input_file, 'r') as csv_input:
            reader = csv.reader(csv_input, delimiter=',', quotechar='"')
            line_nr = 0
            for row in reader:
                line_nr += 1
                if len(row) != NUMBER_OF_COLS:
                    data_error(line_nr, row, 'columns')
                date = datetime.strptime(row[0], '%y-%m-%d %H:%M')
                op_type = process_type(row[1], line_nr)
                ticker = row[2].strip()
                quantity = int(row[3])
                price = process_currency(row[4])
                commission = process_currency(row[5])
                op_sum = process_currency(row[6])
                settlement = datetime.strptime(row[11], '%Y-%m-%d')

                if ticker not in aggregator:
                    aggregator[ticker] = []
                aggregator[ticker].append(Operation(date, op_type, quantity, price, commission, op_sum, settlement))

    return aggregator


def make_import_file_name(year):
    return HISTORY_FILES_DIR + HISTORY_FILES_PREFIX + str(year) + '.csv'


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.stdout.write("Usage: {} file_name date_from [date_to]\n".format(sys.argv[0]))
        sys.exit(-1)

    input_files = [sys.argv[1]]
    history_year = datetime.now().year - 1
    history_file_name = make_import_file_name(history_year)
    while os.path.exists(history_file_name):
        input_files.append(history_file_name)
        history_year -= 1
        history_file_name = make_import_file_name(history_year)
    data = read_data(input_files)
    date_from = datetime.strptime(sys.argv[2], '%Y-%m-%d')
    date_to = datetime.now()
    if len(sys.argv) > 3:
        date_to = datetime.strptime(sys.argv[3], '%Y-%m-%d')
    total = 0

    profit_aggregator = {}
    for ticker in data.keys():
        # ticker = 'IVL1L'
        profit, balance = calculate_profit(
            sorted(data[ticker], key=lambda operation: operation.date, reverse=True),
            date_from,
            date_to
        )
        if balance > 0:
            sys.stdout.write("ticker {} missing data: {}\n".format(ticker, balance))
        else:
            profit_aggregator[ticker] = profit
            total += profit

    print_report("profit", profit_aggregator, 1)
    sys.stdout.write("Total: {}€\n".format(int(total)))
