import argparse
import fileinput
import sys
from itertools import islice

FILENAME = 'bakery.csv'
ENCODING = 'utf-8'
CHUNK_SIZE = 65536

def count_rows(file):
    """
    safety and fast count the number of rows in case of large files
    """
    count = 0
    with open(file, 'rb') as fh:
        while True:
            buffer = fh.read(CHUNK_SIZE)
            if not buffer:
                break
            count += buffer.count(b'\n')
    return count

parser = argparse.ArgumentParser()
parser.add_argument('row_number', type=int, nargs='?', help='the number of row to edit')
parser.add_argument('new_value', type=str, nargs='?', help='new value for row')
args = vars(parser.parse_args())
row_number = args['row_number']
new_value = args['new_value']
row_count = count_rows(FILENAME)

if row_number < 1 or row_number > row_count:
    print(f'wrong row number! min - 1, max - {row_count}')
    sys.exit(1)
else:
    with fileinput.FileInput(FILENAME, inplace = True) as f:
        for line in f:
            if f.lineno() == row_number:
                print(new_value, end='\n')
            else:
                print(line, end='')
