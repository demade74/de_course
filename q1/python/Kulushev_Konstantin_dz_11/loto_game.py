from random import sample
from loto_card import LotoCard
from random import random


class LotoGame:
    NUMBERS_IN_GAME = 90
    AI_ERROR_PROBABILITIES_BY_LEVEL = {
        1: 0.2,
        2: 0.07,
        3: 0
    }

    def __init__(self, player_1, player_2):
        self.player_1_card = LotoCard(player_1)
        self.player_2_card = LotoCard(player_2)
        self.game_finished = False
        self.numbers_in_game_left = 90
        self.numbers_generator = self.numbers_generator()
        self.error_probability = self.select_level()

    @staticmethod
    def greeting():
        print('Добро пожаловать в игру лото!')

    def select_level(self):
        self.greeting()
        while True:
            level = input('Выберите уровень сложности:\n1 - простой\n2 - средний\n3 - тяжелый\n')
            if level not in ['1', '2', '3']:
                print('Некорректный ввод. Попробуйте еще раз.')
            else:
                return self.AI_ERROR_PROBABILITIES_BY_LEVEL[int(level)]

    @staticmethod
    def numbers_generator():
        min_number = 1
        max_number = 90
        numbers_count = 90
        numbers_sample = sample(range(min_number, max_number + 1), numbers_count)
        for number in numbers_sample:
            yield number

    @staticmethod
    def show_game_step(current_number, numbers_left, *cards):
        print('=' * 30)
        print(f'Новый бочонок: {current_number} (осталось {numbers_left})')
        for card in cards:
            print(card)

    @staticmethod
    def request_user_input():
        while True:
            user_input = input('Зачеркнуть число? (y/n). y - да, n - продолжить\n')
            if user_input not in ['y', 'n']:
                print('Некорректный ввод. Попробуйте еще раз.')
            else:
                return user_input

    def finish_game(self, player_name, player_loose=False):
        if player_loose:
            print(f'Игрок {player_name} проиграл. Игра завершена.')
        else:
            print(f'Игрок {player_name} победил. Игра завершена.')

        self.game_finished = True

    def auto_turn(self, number):
        if random() > self.error_probability:
            if self.player_2_card.has_number(number):
                self.player_2_card.try_stoke_number(number)
                if self.player_2_card.all_numbers_stroked:
                    self.finish_game(self.player_2_card.player)

        else:
            self.finish_game(self.player_2_card.player, True)

    def start(self):
        self.game_processing()

    def game_processing(self):
        while not self.game_finished:
            current_number = next(self.numbers_generator)
            self.numbers_in_game_left -= 1
            self.show_game_step(
                current_number, self.numbers_in_game_left, self.player_1_card, self.player_2_card
            )

            user_input = self.request_user_input()
            if user_input == 'y':
                if not self.player_1_card.has_number(current_number):
                    self.finish_game(self.player_1_card.player, True)
                else:
                    self.player_1_card.try_stoke_number(current_number)
                    if self.player_1_card.all_numbers_stroked:
                        self.finish_game(self.player_1_card.player)

                self.auto_turn(current_number)

            elif user_input == 'n':
                if self.player_1_card.has_number(current_number):
                    self.finish_game(self.player_1_card.player, True)
                else:
                    self.auto_turn(current_number)
                    continue


if __name__ == '__main__':
    game = LotoGame('Kostya', 'AI')
    game.start()
