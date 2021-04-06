cubes_of_numbers = []
common_sum_1 = 0
common_sum_2 = 0

# prepare list of cubes
for num in range(1, 1001):
    if num % 2 != 0:
        cubes_of_numbers.append(num ** 3)

for item_a_num in cubes_of_numbers:
    # item a
    local_digits_sum = 0
    item_a_digits = [int(digit) for digit in str(item_a_num)]
    
    for digit in item_a_digits:
        local_digits_sum += digit
    
    if local_digits_sum % 7 == 0:
        common_sum_1 += item_a_num

    # print('item a', item_a_num, local_digits_sum, local_digits_sum % 7, common_sum_1, '<- done' if local_digits_sum % 7 == 0 else '')
    # item b
    item_b_num = item_a_num + 17
    local_digits_sum = 0
    item_b_digits = [int(digit) for digit in str(item_b_num)]

    for digit in item_b_digits:
        local_digits_sum += digit
    
    if local_digits_sum % 7 == 0:
        common_sum_2 += item_b_num   

    # print('item b', item_b_num, local_digits_sum, local_digits_sum % 7, common_sum_2, '<- done' if local_digits_sum % 7 == 0 else '')

print('item a sum =', common_sum_1, '\nitem b sum =', common_sum_2)