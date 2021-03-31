#pip install russian-names
import csv
import random

from russian_names import RussianNames
from datetime import date, timedelta

def get_random_date(start='1970-01-01', end='2003-01-01', times=1000000):
    date_start = date.fromisoformat(start)
    date_end = date.fromisoformat(end)
    dates = []

    for _ in range(times):
        new_date = date_start + timedelta(days=random.randint(1, (date_end - date_start).days))
        dates.append(str(new_date))
    
    return dates 

if __name__ == '__main__':
    rn = RussianNames(count=1000000, surname=False, patronymic=False)
    with open('users_enc.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(list(zip(rn.get_batch(), get_random_date())))