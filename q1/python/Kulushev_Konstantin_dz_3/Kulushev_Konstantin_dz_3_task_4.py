import pprint


def thesaurus_adv(*args, sorting_keys=True):
    # Не реализована сортировка по ключам вложенных словарей
    # Вместо этого итоговый словарь выводится функцией pprint модуля pprint, которая сортирует словарь самостоятельно
    result = {}

    for arg in args:
        current_name_key, current_surname_key = [k[0] for k in arg.split()]

        if current_surname_key not in result:
            result.setdefault(current_surname_key, {current_name_key: [arg]})
        elif current_name_key in result[current_surname_key]:
            result[current_surname_key][current_name_key] += [arg]
        else:
            result[current_surname_key].setdefault(current_name_key, [arg])

    return dict(sorted(result.items())) if sorting_keys else result


pprint.pprint(thesaurus_adv("Иван Сергеев",
                            "Инна Серова",
                            "Петр Алексеев",
                            "Илья Иванов",
                            "Константин Коробков",
                            "Борис Кочергин",
                            "Иван Скворцов",
                            "Андрей Своргин",
                            "Петр Алексеев",
                            "Иван Ильнов",
                            "Федор Селин",
                            "Кирилл Ипатьев",
                            "Анна Савельева"))