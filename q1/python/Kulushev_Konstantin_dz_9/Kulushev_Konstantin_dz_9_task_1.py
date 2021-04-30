import time
from itertools import cycle


class TrafficLight:
    def __init__(self):
        self.__color = ''

    def running(self):
        iterator = cycle(['red', 'yellow', 'green'])
        try:
            while 1:
                self.__color = next(iterator)
                print(self.__color)
                if self.__color == 'red':
                    time.sleep(7)
                elif self.__color == 'yellow':
                    time.sleep(2)
                else:
                    time.sleep(10)
                    print('=' * 10)
        except KeyboardInterrupt:
            exit(0)


light = TrafficLight()
light.running()