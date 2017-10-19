import math


def add(vec1, vec2):
    """
    Sečte dva vektory
    :param vec1:
    :param vec2:
    :return: součet vektorů
    """
    return tuple(sum(res_vec) for res_vec in zip(vec1, vec2))


def load_arena(path):
    """
    Načte ze souboru arénu z X a mezer a vrátí ji jako seznam v seznamu
    :param path:
    :return: arena_list
    """

    arena_list = []
    arena_file = open(path, "rt")

    for arena_line in arena_file:
        points_line = []
        for point in arena_line.rstrip('\n'):
            points_line.append(1 if point == 'x' else 0)
        arena_list.append(points_line)

    arena_file.close()
    return arena_list


def area(path, my_dict):
    """
    Vypočítá obsahy pro obrazce ze souboru
    :param path:
    :param my_dict:
    """
    area_file = open(path, "rt")
    for area_line in area_file:
        try:
            line = area_line.rstrip().split()
            fce = my_dict[line[0]]
            shape = line[0]
            line.pop(0)
            params = tuple(map(float, line))
            print(shape + " = " + str(fce(*params)))
        except KeyError:
            print('Unknown formula')
        except IndexError:
            print('Blank line')


print("Úloha 1:")

tup3 = add((-1, 0, 6), (2, 3, -2))
print(tup3)
print("-----")

print("Úloha 2:")
arena = load_arena("arena.txt")
print(arena[3][1])
print("-----")

print("Úloha 3:")
shapes = {
    'kruh': lambda r: math.pi * (r ** 2),
    'ctverec': lambda x: x ** 2,
    'obdelnik': lambda x, y: x * y,
    'krychle': lambda x: 6 * x ** 2,
    'kvadr': lambda a, b, c: 2 * (a * b + b * c + a * c)
}

area("test.txt", shapes)
