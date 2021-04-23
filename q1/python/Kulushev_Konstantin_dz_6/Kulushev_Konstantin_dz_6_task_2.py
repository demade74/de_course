import re
from collections import Counter

# task 1
result = []
remote_addr_pattern = r'(\d{1,3}\.){3}\d{1,3}'
mac_address_pattern = r'^([0-9a-fA-F]{2,4}[:]{1,}){2,}'
request_and_source_pattern = r'(GET|HEAD)\s/downloads/product_\d'

with open('nginx_logs.txt') as f:
    for line in f:
        # skip MAC-address which will meet instead of IP-address
        if re.match(mac_address_pattern, line):
            continue

        remote_addr = re.search(remote_addr_pattern, line).group(0)
        request_data = re.search(request_and_source_pattern, line).group(0)
        result.append((remote_addr, *request_data.split()))

print(result)

# task 2*
addrs = [element[0] for element in result]
spammer_addr = Counter(addrs).most_common(1)[0][0]
print(f'spammer detected at {spammer_addr}')

