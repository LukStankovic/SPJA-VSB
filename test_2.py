def invert(input_string):
    """
    Invertuje velikost znaků v řetězeci
    :param input_string:
    :return: inverted_string
    """
    inverted_string = ''
    for character in input_string:
        if character.islower():
            inverted_string += character.upper()
        else:
            inverted_string += character.lower()
    return inverted_string


def translate(eng_dict, eng_word):
    """
    Vrátí překlad pro slovník
    :param eng_dict:
    :param eng_word:
    :return:
    """
    if eng_word in eng_dict:
        return eng_dict[eng_word]
    else:
        print("Word is not in dictionary. Available is only: ", sorted(eng_dict))
        return None


def my_factorial(number):
    """
    Vypočte faktorial
    :param number:
    :return: factorial
    """
    factorial = 1
    while number > 1:
        factorial *= number
        number -= 1
    return factorial


def fu(x):
    return 3 * x + 5


def fu_map(values, fce):
    """
    Namapovaní funkce fu
    :param values:
    :param fce:
    :return:
    """
    lst = []
    for value in values:
        try:
            x = float(value)
            lst.append(fce(x))
        except (ValueError, TypeError):
            pass
    return lst


def fu2(x):
    return ((1 / 3) * x ** 3) - 2 * x ** 2 + x + 8


def integral(n, a, b):
    """
    Vypočítá určitý dvojitý integrál
    :param n:
    :param a:
    :param b:
    :return: určitý integrál
    """
    i = a
    value = 0
    dx = ((b - a) / n)
    while i <= b:
        value += dx * fu2(i)
        i += dx
    return value


# 1.
print("1. úloha")
print(invert("Ahoj"))
print(invert("JoJo"))

# 2.
print("2. úloha")
my_dict = {'zebra': 'zebra', 'car': 'auto', 'cat': 'kočka', 'dog': 'pes', 'mouse': 'myš', 'sun': 'slunce'}
print(translate(my_dict, 'caat'))

# 3.
print("3. úloha")
print(fu_map(["Hello world", "3.14", 0, 8.9, 5j], fu))

# 4.
print("4. úloha")
print(my_factorial(4))

# 5.
print("5. úloha")
print(integral(100000, 0, 6))
