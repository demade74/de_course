percent = 'процент'
while True:
    try:
        percent_value = int(input("Введите количество процентов: "))
        break
    except ValueError:
        print("Необходимо ввести целое число. Попробуйте еще раз.")
        continue

if percent_value == 1:
    print(str(percent_value), percent)
elif 1 < percent_value <= 4:
    print(str(percent_value), percent + 'а')
else:
    print(str(percent_value), percent + 'ов')

# print all
print('=' * 20)
for number in range(1, 21):
    if number == 1:
        print(str(number), percent)
    elif 1 < number <= 4:
        print(str(number), percent + 'а')
    else:
        print(str(number), percent + 'ов')