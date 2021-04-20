import re
import requests
from datetime import datetime, date
from decimal import Decimal
from bs4 import BeautifulSoup

def currency_rates_str(currency_code):
    currency_code = currency_code.upper()
    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp').text
    if currency_code not in response:
        return None

    str_with_date, str_with_rate = response.split(currency_code)
    # search the date
    start = str_with_date.find('Date=')
    end = str_with_date.find(' name')
    request_date = str_with_date[start + len('Date="'):end].replace('"', '')
    request_date = datetime.strptime(request_date, '%d.%m.%Y').strftime('%Y-%m-%d')

    # search the rate
    start = str_with_rate.find('<Value>')
    end = str_with_rate.find('</Value>')
    request_rate = str_with_rate[start + len('<Value>'):end]
    
    return Decimal(request_rate.replace(',', '.')), date.fromisoformat(request_date)


def currency_rates_re(currency_code):
    currency_code = currency_code.upper()
    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp').text

    if currency_code not in re.findall(r'[A-Z]{3}', response):
        return None

    request_date = re.search(r'\d{2}\.\d{2}\.\d{4}', response).group(0)
    request_date = datetime.strptime(request_date, '%d.%m.%Y').strftime('%Y-%m-%d')
    request_rate = re.search(r'\d+,\d+', re.split(currency_code, response)[1]).group(0)
    
    return Decimal(request_rate.replace(',', '.')), date.fromisoformat(request_date)


def currency_rates_bs(currency_code):
    currency_code = currency_code.upper()
    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
    soup = BeautifulSoup(response.content, 'xml')

    if soup.find('CharCode', text=currency_code) is None:
        return None

    request_date = soup.find('ValCurs').attrs['Date']
    request_date = datetime.strptime(request_date, '%d.%m.%Y').strftime('%Y-%m-%d')
    request_rate = soup.find('CharCode', text=currency_code).find_next_sibling('Value').string
    
    return Decimal(request_rate.replace(',', '.')), date.fromisoformat(request_date)

print(currency_rates_bs('USD'))
print(currency_rates_bs('EUR'))