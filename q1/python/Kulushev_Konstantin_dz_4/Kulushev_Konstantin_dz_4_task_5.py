from utils import currency_rates_bs
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('currency_code', type=str, help='currency code (case insensitive)')
args = parser.parse_args()
currency_rates_bs(args.currency_code)