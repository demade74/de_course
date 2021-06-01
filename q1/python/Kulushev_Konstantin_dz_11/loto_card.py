from random import sample, randint


class LotoCard:
    MAX_NUMBER = 90
    LINES_NUMBER = 3
    COLUMNS_NUMBER = 9
    NUMBERS_IN_CARD = 15
    NUMBERS_IN_LINE = 5
    SPACES_IN_LINE = 4
    MAX_FIELD_LEN = 3
    STROKED_NUMBERS_TO_WIN = 15

    def __init__(self, player):
        self.player = player
        self._numbers = sorted(sample(range(1, LotoCard.MAX_NUMBER + 1), LotoCard.NUMBERS_IN_CARD))
        self._numbers = [sorted(self._numbers[i:i + 5]) for i in range(0, len(self._numbers), 5)]
        self._numbers = [line + ([' '] * LotoCard.SPACES_IN_LINE) for line in self._numbers]

        for index, line in enumerate(self._numbers):
            self._numbers[index] = sorted(line, key=lambda x: x if isinstance(x, int) else randint(1, LotoCard.MAX_NUMBER))

        self._numbers_stroked = 0
        self.all_numbers_stroked = False

    def has_number(self, number):
        return bool(sum([number in line for line in self._numbers]))

    def try_stoke_number(self, number):
        for index, line in enumerate(self._numbers):
            for num_index, number_in_line in enumerate(line):
                if number == number_in_line:
                    self._numbers[index][num_index] = 'x'
                    self._numbers_stroked += 1
                    if self._numbers_stroked >= LotoCard.STROKED_NUMBERS_TO_WIN:
                        self.all_numbers_stroked = True

    def __str__(self):
        header = f'\n{self.player}:\n'
        body = '-' * 27 + '\n'
        for line in self._numbers:
            for field in line:
                body += str(field).ljust(LotoCard.MAX_FIELD_LEN)
            body += '\n'
        body += '-' * (LotoCard.COLUMNS_NUMBER * LotoCard.MAX_FIELD_LEN)
        return header + body
