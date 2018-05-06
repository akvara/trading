import sys
import operator

def process_currency(item, delimiter_thous='.', delimiter_dec=','):
    value = item.replace('-- ', '').replace(' €', '').replace(delimiter_thous, '').replace(delimiter_dec, '.')
    if not value:
        value = 0
    return float(value)


def print_result(dictionary):
    for (key, value) in dictionary:
        sys.stdout.write("{}\t{}\n".format(int(value), key))


def print_report(by, dictionary, sort_column):
    sys.stdout.write("By {}\n".format(by))
    print_result(sorted(dictionary.items(), key=operator.itemgetter(sort_column)))
    sys.stdout.write("-" * 40 + "\n\n")
