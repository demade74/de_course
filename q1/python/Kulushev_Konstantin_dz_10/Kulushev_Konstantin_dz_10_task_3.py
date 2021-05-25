class Cell:
    def __init__(self, cells):
        self.cells = cells

    @staticmethod
    def check_operand_type(other):
        if not isinstance(other, Cell):
            raise TypeError('Second operand must be of type Cell')

    def __add__(self, other):
        Cell.check_operand_type(other)
        return Cell(self.cells + other.cells)

    def __sub__(self, other):
        Cell.check_operand_type(other)
        if self.cells - other.cells < 0:
            return 'Result of subtraction is less than 0'
        return Cell(self.cells - other.cells)

    def __mul__(self, other):
        Cell.check_operand_type(other)
        return Cell(self.cells * other.cells)

    def __floordiv__(self, other):
        Cell.check_operand_type(other)
        return Cell(self.cells // other.cells)

    def make_order(self, cells_per_row):
        common_count = '*' * self.cells
        return '\n'.join(common_count[i:i + cells_per_row] for i in range(0, self.cells, cells_per_row))


cell1 = Cell(12)
cell2 = Cell(7)
cell3 = Cell(15)
cell4 = Cell(0)

# check operations
print(
    (cell1 + cell2).cells, (cell1 - cell2).cells, (cell1 * cell2).cells, (cell1 // cell2).cells, sep='\n'
)
print('=' * 20)
print(cell3.make_order(6))
print('=' * 20)
print(cell2 - cell1)
print('=' * 20)

# 19
# 5
# 84
# 1
# ====================
# ******
# ******
# ***
# ====================
# Result of subtraction is less than 0
# ====================
