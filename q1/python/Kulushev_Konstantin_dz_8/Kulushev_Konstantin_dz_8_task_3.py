def type_logger(func):
    def wrapper(*args):
        print(func.__name__ + '(' + ', '.join(f'{arg}: {type(arg)}' for arg in args) + ')')
        return func(*args)
    return wrapper

@type_logger
def calc_cube(*args):
    results = []
    for arg in args:
        results.append(arg ** 3)
    
    return results


print(calc_cube(6, 7, 8, 33))
# output example
# calc_cube(6: <class 'int'>, 7: <class 'int'>, 8: <class 'int'>, 33: <class 'int'>)
# [216, 343, 512, 35937]