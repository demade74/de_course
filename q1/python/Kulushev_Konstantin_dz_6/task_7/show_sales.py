import argparse
from itertools import islice

FILENAME = 'bakery.csv'
ENCODING = 'utf-8'

parser = argparse.ArgumentParser()
parser.add_argument('start', type=int, nargs='?', help='start line index')
parser.add_argument('end', type=int, nargs='?', help='end line index')
args = vars(parser.parse_args())
start_index = args['start']
end_index = args['end']

if list(args.values()).count(None) == 2:
    with open(FILENAME, encoding=ENCODING) as f:
        for row in f:
            print(row.strip())
elif start_index and end_index is None:
    with open(FILENAME, encoding=ENCODING) as f:
        for row in islice(f, start_index - 1 if start_index > 0 else 0, None):
            print(row.strip())
else:
    with open(FILENAME, encoding=ENCODING) as f:
        for row in islice(f, start_index - 1 if start_index > 0 else 0, end_index):
            print(row.strip())