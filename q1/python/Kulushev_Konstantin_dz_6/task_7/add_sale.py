import argparse

FILENAME = 'bakery.csv'
ENCODING = 'utf-8'

parser = argparse.ArgumentParser()
parser.add_argument('sum', type=str, help='Sum')
args = parser.parse_args()

with open(FILENAME, 'a', encoding=ENCODING) as f:
    f.write(args.sum + '\n')
