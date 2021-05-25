class MatrixAdditionError(Exception):
    pass


class Matrix:
    def __init__(self, elements=None):
        self.elements = elements if elements else []
        self.rows = len(self.elements)
        self.columns = len(self.elements[0]) if elements else 0
        self.dimension = (self.rows, self.columns)

    def __str__(self):
        return '\n'.join(' '.join(str(element) for element in row) for row in self.elements)

    def __add__(self, other):
        if self.dimension != other.dimension:
            raise MatrixAdditionError('Dimensions of matrices must be the same')

        new_matrix = [
            [element_1 + element_2 for element_1, element_2 in zip(row_1, row_2)]
            for row_1, row_2 in zip(self.elements, other.elements)
        ]

        return Matrix(new_matrix)


a = Matrix([[1, 2, 3], [4, 5, 6]])
b = Matrix([[10, 32.3, 4], [-10, 0, 54.9]])
c = Matrix([[1, 2], [3, 4]])
print(a + b)
print(type(a + b))
print(a + c)

# output example

# 11 34.3 7
# -6 5 60.9
# <class '__main__.Matrix'>
# Traceback (most recent call last):
#   File "D:/VSCodeFiles/de_python_course/Kulushev_Konstantin_dz_10_task_1.py", line 32, in <module>
#     print(a + c)
#   File "D:/VSCodeFiles/de_python_course/Kulushev_Konstantin_dz_10_task_1.py", line 17, in __add__
#     raise MatrixAdditionError('Dimensions of matrices must be the same')
# __main__.MatrixAdditionError: Dimensions of matrices must be the same
