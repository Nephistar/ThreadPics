import csv
from OklchConverter import Datum

def _read_csv(filename: str):
    with open(filename) as csvfile:
        data = csv.reader(csvfile)
        table = list(data)
    return table

def _get_column(table: list, col_idx: int):
    column = [row[col_idx] for row in table]
    return column

def _create_lookup(ids: list, values: list):
    dictionary = dict(zip(ids, values))
    return dictionary

def _parse_hexcode_to_rgb(hexcode: str):
    hexcode = hexcode.lstrip(' #')
    if hexcode.startswith('0x'):
        hexcode = hexcode[2:]
    rgb = tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))
    return rgb

def create_oklch_dict_from_hexcodes(filename: str):
    table = _read_csv(filename)
    ids = _get_column(table, 0)
    hexcodes = _get_column(table, 1)
    rgbs = [_parse_hexcode_to_rgb(hexcode) for hexcode in hexcodes]
    oklchs = [Datum(rgb) for rgb in rgbs]
    lookup = _create_lookup(ids, oklchs)
    return lookup

def create_url_dict(filename: str):
    table = _read_csv(filename)
    ids = _get_column(table, 0)
    urls = _get_column(table, 1)
    lookup = _create_lookup(ids, urls)
    return lookup

