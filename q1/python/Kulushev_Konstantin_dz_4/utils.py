import requests
from datetime import datetime, date
from decimal import Decimal
from bs4 import BeautifulSoup

def currency_rates_bs(currency_code, print_return_values=True):
    currency_code = currency_code.upper()
    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
    soup = BeautifulSoup(response.content, 'xml')

    if soup.find('CharCode', text=currency_code) is None:
        print('None')
        return None

    request_date = soup.find('ValCurs').attrs['Date']
    request_date = datetime.strptime(request_date, '%d.%m.%Y').strftime('%Y-%m-%d')
    request_rate = soup.find('CharCode', text=currency_code).find_next_sibling('Value').string
    
    if print_return_values:
        print(request_rate, request_date)
        return Decimal(request_rate.replace(',', '.')), date.fromisoformat(request_date)
    else:
        return Decimal(request_rate.replace(',', '.')), date.fromisoformat(request_date)