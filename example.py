import random

list2 = ['test1', 'two', 'three', 'four']

rand = random.randint(0, len(list2) - 1)

print(rand)

if rand > 2:
    print('rand > 2')

