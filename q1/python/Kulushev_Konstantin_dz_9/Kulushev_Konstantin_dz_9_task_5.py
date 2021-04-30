class Stationery:
    def __init__(self, title):
        self.title = title

    def draw(self):
        print(f'{self.title} start drawing')


class Pen(Stationery):
    def draw(self):
        print(f'{self.title} start drawing')


class Pencil(Stationery):
    def draw(self):
        print(f'{self.title} start drawing')


class Handle(Stationery):
    def draw(self):
        print(f'{self.title} start drawing')


pen = Pen('Sokolov')
pencil = Pencil('Erich Krause')
handle = Handle('Touch Cool')

pen.draw()
pencil.draw()
handle.draw()


# C:\Users\demad\AppData\Local\Programs\Python\Python38\python.exe D:/VSCodeFiles/de_python_course/Kulushev_Konstantin_dz_9_task_5.py
# Sokolov start drawing
# Erich Krause start drawing
# Touch Cool start drawing
#
# Process finished with exit code 0