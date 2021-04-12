def num_translate_adv(request):
    numbers_to_translate = {
        'one': 'oдин',
        'two': 'два',
        'three': 'три',
        'four': 'четыре',
        'five': 'пять',
        'six': 'шесть',
        'seven': 'семь',
        'eight': 'восемь',
        'nine': 'девять',
        'ten': 'десять'
    }
    
    if request == request.title():
        if request.lower() in numbers_to_translate:
            return numbers_to_translate.get(request.lower()).title()

    return numbers_to_translate.get(request)

print(num_translate_adv('Four'))