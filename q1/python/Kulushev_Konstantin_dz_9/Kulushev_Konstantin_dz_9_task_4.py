class Car:
    def __init__(self, speed, color, name, is_police=False):
        self.speed = speed
        self.color = color
        self.name = name
        self.is_police = is_police

    def go(self):
        print(f'car {self.name} go')

    def stop(self):
        print(f'car {self.name} stop')

    def turn(self, direction):
        print(f'car {self.name} turn {direction}')

    def show_speed(self):
        print(f'current speed is {self.speed}')


class TownCar(Car):
    MAX_SPEED = 60

    def show_speed(self):
        if self.speed <= TownCar.MAX_SPEED:
            print(f'current speed is {self.speed}')
        else:
            print(f'speed exceeded! max speed is {TownCar.MAX_SPEED}')


class SportCar(Car):
    pass


class WorkCar(Car):
    MAX_SPEED = 40

    def show_speed(self):
        if self.speed <= WorkCar.MAX_SPEED:
            print(f'current speed is {self.speed}')
        else:
            print(f'speed exceeded! max speed is {WorkCar.MAX_SPEED}')


class PoliceCar(Car):
    pass


town_car = TownCar(60, 'red', 'Ford')
sport_car = SportCar(90, 'black', 'BMW')
work_car = WorkCar(62, 'silver', 'Gazel')
police_car = PoliceCar(80, 'white', 'Skoda', True)

for obj in [town_car, sport_car, work_car, police_car]:
    print('=' * 20)
    print(obj.name, obj.color, obj.speed, obj.is_police)
    obj.go()
    obj.turn('right')
    obj.show_speed()
    obj.stop()


# C:\Users\demad\AppData\Local\Programs\Python\Python38\python.exe D:/VSCodeFiles/de_python_course/Kulushev_Konstantin_dz_9_task_4.py
# ====================
# Ford red 60 False
# car Ford go
# car Ford turn right
# current speed is 60
# car Ford stop
# ====================
# BMW black 90 False
# car BMW go
# car BMW turn right
# current speed is 90
# car BMW stop
# ====================
# Gazel silver 62 False
# car Gazel go
# car Gazel turn right
# speed exceeded! max speed is 40
# car Gazel stop
# ====================
# Skoda white 80 True
# car Skoda go
# car Skoda turn right
# current speed is 80
# car Skoda stop
#
# Process finished with exit code 0
