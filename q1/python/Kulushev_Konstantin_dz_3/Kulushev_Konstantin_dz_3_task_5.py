from random import choice


def get_jokes(amount, only_one_use=True):
    """
    function generates given amount of jokes by selecting random word from three lists
    :param amount: number of jokes to be generated
    :param only_one_use: prohibit the use of each word more than once
    :return: list
    """

    nouns = ["автомобиль", "лес", "огонь", "город", "дом"]
    adverbs = ["сегодня", "вчера", "завтра", "позавчера", "ночью"]
    adjectives = ["веселый", "яркий", "зеленый", "утопичный", "мягкий"]
    result = []

    if not only_one_use:
        for _ in range(amount):
            result.append(choice(nouns) + ' ' + choice(adverbs) + ' ' + choice(adjectives))
    else:
        for _ in range(amount):
            try:
                noun = choice(nouns)
                adverb = choice(adverbs)
                adjective = choice(adjectives)
            except IndexError:
                break

            result.append(noun + ' ' + adverb + ' ' + adjective)
            nouns.remove(noun)
            adverbs.remove(adverb)
            adjectives.remove(adjective)

    return result


print(get_jokes(10, only_one_use=False))
print(get_jokes(10, only_one_use=True))

