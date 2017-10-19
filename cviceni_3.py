import math


def add(tup1, tup2):
    return tuple([tup1[i] + tup2[i] for i in range(len(tup1))])


def load_arena(path):
    try:
        arena_file = open(path, "rt")
        try:
            arena_lst = []
            for line in arena_file:
                characters = []
                for character in line:
                    if character == 'x':
                        characters.append(1)
                    elif character == ' ':
                        characters.append(0)
                arena_lst.append(characters)
        finally:
            arena_file.close()
            return arena_lst
    except IOError as e:
        print(e)


def area(path, dict):
    try:
        arena_file = open(path, "rt")
        try:
            results = []
            for line in arena_file:
                line_result = line.split()

        finally:
            arena_file.close()

    except IOError as e:
        print(e)


tup3 = add((-1, 0, 6), (2, 3, -2))

print(tuple(tup3))
arena = load_arena("arena.txt")
print(arena[3][1])

dict = {'kruh': lambda r: math.pi * (r ** 2),
        'ctverec': lambda x: x ** 2,
        'obdelnik': lambda x, y: x * y,
        'krychle': lambda x: 6 * x ** 2,
        'kvadr': lambda a, b, c: 2 * (a * b + b * c + a * c)
        }


area("test.txt", dict)