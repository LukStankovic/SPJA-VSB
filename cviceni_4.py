class Counter(object):
    no_of_counters = 0

    def __init__(self, count=0):
        self.__count = count
        Counter.no_of_counters += 1

    def inc_counter(self):
        self.__count += 1

    def __add__(self, other):
        return Counter(self.__count + other.count)

    @staticmethod
    def print_no_of_counters():
        print("Total counters: " + str(Counter.no_of_counters))

    @property
    def count(self):
        return self.__count

    @count.setter
    def count(self, count):
        self.__count = count


first_counter = Counter(1)
second_counter = Counter(10)
third_counter = Counter()

Counter.print_no_of_counters()

fourth_counter = Counter(-5)

Counter.print_no_of_counters()

a = first_counter + second_counter + third_counter + fourth_counter

print(a.count)
