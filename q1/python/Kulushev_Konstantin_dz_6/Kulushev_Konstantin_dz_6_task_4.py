import sys
import argparse
from itertools import zip_longest

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
    return count + 1

# parse arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument('users_file', type=str, help='users info filename')
parser.add_argument('hobby_file', type=str, help='hobby info filename')
parser.add_argument('output_file', type=str, help='output filename')
args = parser.parse_args()

# count rows
users_file_rows_count = count_rows(args.users_file)
hobby_file_rows_count = count_rows(args.hobby_file)

if users_file_rows_count < hobby_file_rows_count:
    print('the number of users is less than the corresponding number of hobbies')
    sys.exit(1)
else:
    users = open(args.users_file, encoding='utf-8')
    hobby = open(args.hobby_file, encoding='utf-8')

    with open(args.output_file, 'w', encoding='utf-8') as result:
        for user_row, hobby_row in zip_longest(users, hobby):
            result.write('{}: {}\n'.format(user_row.strip(), hobby_row.strip() if hobby_row else None))

    users.close()
    hobby.close()