import random


def max_value_index(l):
    max = l[0]
    index = 0
    for i in range(len(l)):
        if l[i] > max:
            max = l[i]
            index = i
    return index


def set_born_value(val):
    if val > 250:
        val = 250
    if val < -250:
        val = -250
    return val


def set_rand_pos():
    return 500 * (random.random() - 0.5)
