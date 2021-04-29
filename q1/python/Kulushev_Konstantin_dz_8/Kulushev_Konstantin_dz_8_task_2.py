import re

remote_addr_pattern = r'(\d{1,3}\.){3}\d{1,3}'
date_pattern = r'\d{2}/\w+/\d{4}:(\d{2}:){2}\d{2}\s+\+\d+'
mac_address_pattern = r'^([0-9a-fA-F]{2,4}[:]{1,}){2,}'
request_and_source_pattern = r'(GET|HEAD)\s(/downloads/product_\d)\s+HTTP/\d\.\d\"\s+(\d+)\s+(\d+)'

with open('nginx_logs.txt') as f:
    with open('parsed_logs.txt', 'w') as r:
        for line in f:
            # skip MAC-address which will meet instead of IP-address
            if re.match(mac_address_pattern, line):
                continue

            remote_addr = re.search(remote_addr_pattern, line).group(0)
            request_date = re.search(date_pattern, line).group(0)
            request_data = re.search(request_and_source_pattern, line)
            request_type, requested_source = request_data.group(1), request_data.group(2)
            response_code, response_size = request_data.group(3), request_data.group(4)

            r.write(', '.join((remote_addr, request_date, request_type, requested_source, response_code, response_size)) + '\n')