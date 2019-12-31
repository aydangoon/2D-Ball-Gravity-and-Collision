#Copyright (C) 2019 Aydan Gooneratne

from pygame import Vector2
import math

RADIUS_FACTOR = 10
SPEED_FACTOR = 0.05
MASS_FACTOR = 10

class Planet:
    def __init__(self, pos: Vector2, vel: Vector2, radius):
        self._radius = radius
        self._acc = Vector2(0, 0)
        self._vel = vel
        self._pos = pos
        self.UNMOVABLE = False

    def shift_radius(self, shift):
        self._radius = self._radius + shift

    def shift_vel(self, v: Vector2):
        self._vel.update(self._vel.x + v.x, self._vel.y + v.y)

    def set_vel(self, v: Vector2):
        self._vel.update(v)

    def set_vel(self, pos):
        self._vel.update(pos[0], pos[1])

    def set_acc(self, a: Vector2):
        self._acc.update(a)

    def shift_acc(self, a: Vector2):
        self._acc.update(self._acc.x + a.x, self._acc.y + a.y)

    def get_radius(self):
        return int(self._radius)

    def get_mass(self):
        return 3.14 * math.pow(self._radius, 2)

    def get_color(self):
        val = self._radius if self._radius < 20 else 20
        return 100 + (155 * (val / 20)), 200, 100

    def get_pos(self):
        return int(self._pos.x), int(self._pos.y)

    def get_vel(self):
        return self._vel.x, self._vel.y

    def move(self):
        #self.shift_vel(self._acc)
        self._pos.update(self._pos.x + SPEED_FACTOR * self._vel.x, self._pos.y + SPEED_FACTOR * self._vel.y)

    def set_pos(self, pos):
        self._pos.update(pos[0], pos[1])

    def shift_pos(self, x, y):
        self._pos.update(self._pos.x + x, self._pos.y + y)

    def shift_pos(self, v: Vector2):
        self._pos.update(self._pos.x + v.x, self._pos.y + v.y)
