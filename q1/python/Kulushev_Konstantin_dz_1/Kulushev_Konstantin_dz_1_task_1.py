duration = ''
while True:
    try:
        duration = int(input("Введите продолжительность промежутка времени в секундах: "))
    except ValueError:
        print("Необходимо ввести целое число. Попробуйте еще раз.")
        continue

    if duration < 0:
        print("Необходимо ввести положительное число. Попробуйте еще раз.")
        continue
    else:
        break

days = duration // 86400
hours = (duration - days * 86400) // 3600
minutes = (duration - days * 86400 - hours * 3600) // 60
seconds = duration - days * 86400 - hours * 3600 - minutes * 60 

print(
    f'{days} дн ' if days else '',
    f'{hours} час ' if hours else '',
    f'{minutes} мин ' if minutes else '',
    f'{seconds} сек' if seconds else '',
    sep=''
)
