tutors = ['Иван', 'Анастасия', 'Петр', 'Сергей', 'Дмитрий', 'Борис', 'Елена']
classes = ['9А', '7В', '9Б', '9В', '8Б', '10А', '10Б', '9А']

def tutor_class_gen(*iterables):
    tutors, classes = iterables
    for idx, name in enumerate(tutors):
        yield name, classes[idx] if idx < len(classes) else None

test_generator = tutor_class_gen(tutors, classes)
# check output
print(type(test_generator))
for tpl in test_generator:
    print(tpl)

print('=' * 20)
tutors = ['Иван', 'Анастасия', 'Петр', 'Сергей', 'Дмитрий', 'Борис', 'Елена']
classes = ['9А', '7В', '9Б', '9В']
test_generator_2 = tutor_class_gen(tutors, classes)
for tpl in test_generator_2:
    print(tpl)

# <class 'generator'>
# ('Иван', '9А')
# ('Анастасия', '7В')
# ('Петр', '9Б')
# ('Сергей', '9В')
# ('Дмитрий', '8Б')
# ('Борис', '10А')
# ('Елена', '10Б')
# ====================
# ('Иван', '9А')
# ('Анастасия', '7В')
# ('Петр', '9Б')
# ('Сергей', '9В')
# ('Дмитрий', None)
# ('Борис', None)
# ('Елена', None)
