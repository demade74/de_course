def val_checker(callback_func):
    def my_decorator(func):
        def wrapper(x):
            if callback_func(x):
                return func(x)
            else:
                raise ValueError(f'wrong value {x}')
        return wrapper
    return my_decorator

@val_checker(lambda x: x > 0)
def calc_cube(x):    
    return x ** 3

a = calc_cube(123)
print(a) # 1860867

a = calc_cube(-123)
print(a)
# Traceback (most recent call last):
#   File "d:/VSCodeFiles/de_python_course/Kulushev_Konstantin_dz_8_task_4.py", line 18, in <module>
#     a = calc_cube(-123)
#   File "d:/VSCodeFiles/de_python_course/Kulushev_Konstantin_dz_8_task_4.py", line 7, in wrapper
#     raise ValueError(f'wrong value {x}')
# ValueError: wrong value -123