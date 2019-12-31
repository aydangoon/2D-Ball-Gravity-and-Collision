#Copyright (C) 2019 Aydan Gooneratne

import math

def add(t1, t2):
    return t1[0] + t2[0], t1[1] + t2[1]


def subtract(t1, t2):
    return add(t1, scale(t2, -1))


def scale(t, c):
    return t[0]*c, t[1] * c

def dist_squared(t1, t2):
    return math.pow(t1[0]-t2[0], 2) + math.pow(t1[1] - t2[1], 2)

def dist(t1, t2):
    return math.sqrt(dist_squared(t1, t2))
