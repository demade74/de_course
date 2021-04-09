import random
import math

# generate list of prices
goods_prices = []
for _ in range(20):
    if random.random() > 0.5:
        goods_prices.append(round(random.random() * 100, 2))
    else:
        goods_prices.append(random.randint(1, 100))

print(goods_prices)
# A
print('item A')
for price in goods_prices:
    parts = math.modf(price)
    print(f'{parts[1]:.0f} руб {int(round(parts[0] * 100, 0)):02} коп')

# output example
# [58.29, 13.05, 70.89, 27, 82, 63, 40, 53, 3, 70.44, 64, 100, 8.68, 57.37, 10.93, 1, 70.38, 6, 43.03, 92]
# 58 руб 29 коп
# 13 руб 05 коп
# 70 руб 89 коп
# 27 руб 00 коп
# 82 руб 00 коп
# 63 руб 00 коп
# 40 руб 00 коп
# 53 руб 00 коп
# 3 руб 00 коп
# 70 руб 44 коп
# 64 руб 00 коп
# 100 руб 00 коп
# 8 руб 68 коп
# 57 руб 37 коп
# 10 руб 93 коп
# 1 руб 00 коп
# 70 руб 38 коп
# 6 руб 00 коп
# 43 руб 03 коп
# 92 руб 00 коп

# B
print('item B')
print(f'list before sorting {goods_prices}, ID = {id(goods_prices)}')
goods_prices.sort()
print(f'list after sorting {goods_prices}, ID = {id(goods_prices)}')

# output example
# list before sorting [58.29, 13.05, 70.89, 27, 82, 63, 40, 53, 3, 70.44, 64, 100, 8.68, 57.37, 10.93, 1, 70.38, 6, 43.03, 92], ID = 2838598638464
# list after sorting [1, 3, 6, 8.68, 10.93, 13.05, 27, 40, 43.03, 53, 57.37, 58.29, 63, 64, 70.38, 70.44, 70.89, 82, 92, 100], ID = 2838598638464

# C
print('item C')
sorted_goods_prices = sorted(goods_prices, reverse=True)
print(f'list after sorting {sorted_goods_prices}, ID = {id(sorted_goods_prices)}')

# D
print('item D')
print(list(sorted(goods_prices))[-5:])

# output example
# [73.02, 92.65, 95, 96.39, 99.68]
