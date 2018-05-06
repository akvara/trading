def process_currency(item, delimiter_thous='.', delimiter_dec=','):
    value = item.replace('-- ', '').replace(' €', '').replace(delimiter_thous, '').replace(delimiter_dec, '.')
    if not value:
        value = 0
    return float(value)
