from abc import ABC, abstractmethod


class Clothes(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def cloth_consumption(self):
        pass


class Coat(Clothes):
    def __init__(self, name, size):
        super().__init__(name)
        self.size = size

    @property
    def cloth_consumption(self):
        return self.size / 6.5 + 0.5


class Suit(Clothes):
    def __init__(self, name, height):
        super().__init__(name)
        self.height = height

    @property
    def cloth_consumption(self):
        return 2 * self.height + 0.3


coat = Coat('coat', 12.4)
suit = Suit('suit', 23.8)
print(f'common cloth consumption is {coat.cloth_consumption + suit.cloth_consumption:.3f}')
