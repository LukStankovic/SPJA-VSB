def add(a, b):
    a = a * 2
    return a + b


print (3/4);

print ("a + b = " + str(add(3, 7)))

a = 5
if a == 0:
    print ("zero")
elif a < 0:
    print ("negative")
else:
    print ("positive")

lst = []
for i in range(5):
    if i % 2 == 0:
        lst.append(i)
print (lst)

lst = [i*2 for i in range(10) if i % 2 == 0]

print (lst)

i = 0

while i < 5:
    print ("{0}. hodnota".format(i))
    i += 1
