class Worker:
    def __init__(self, name, surname, position, income):
        self.name = name
        self.surname = surname
        self.position = position
        if isinstance(income, dict):
            self._income = income
        else:
            self._income = {}

    def get_income(self):
        return self._income


class Position(Worker):
    def get_full_name(self):
        return self.name + ' ' + self.surname

    def get_total_income(self):
        return sum(self.get_income().values())


position_1 = Position('Ivan', 'Ivanov', 'Programmer', {'wage': 100000, 'bonus': 12000})
print(position_1.name)
print(position_1.surname)
print(position_1.position)
print(position_1._income)
print(position_1.get_full_name())
print(position_1.get_total_income())

# C:\Users\demad\AppData\Local\Programs\Python\Python38\python.exe D:/VSCodeFiles/de_python_course/Kulushev_Konstantin_dz_9_task_3.py
# Ivan
# Ivanov
# Programmer
# {'wage': 100000, 'bonus': 12000}
# Ivan Ivanov
# 112000
#
# Process finished with exit code 0
