import os
from itertools import dropwhile

DIR = 'some_data'
result = dict.fromkeys([10 ** value for value in range(1, 6)], 0)
result_keys = [0] + list(result.keys())

def add_to_dict(path):
    size = os.stat(path).st_size
    try:
        current_key = list(dropwhile(lambda x: x <= size, result_keys))[0]
    except IndexError:
        print(f'file {f.name} is too large!')
    else:
        result[current_key] += 1


for root, dirs, files in os.walk(DIR):
    print(root)

    for f in os.scandir(root):
        if f.is_file():
            add_to_dict(f)

print(result)