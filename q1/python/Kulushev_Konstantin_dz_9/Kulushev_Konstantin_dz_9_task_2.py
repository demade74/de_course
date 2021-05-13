class Road:
    def __init__(self, length, width, weight, height):
        self._length = length
        self._width = width
        self._weight = weight
        self._height = height

    def calculate_mass(self):
        mass = self._length * self._width * self._weight * self._height
        print(f'required asphalt mass {mass / 1000} t')
        return mass


road = Road(5000, 20, 25, 5)
road.calculate_mass()

