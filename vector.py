"""
# vector.py - CS481-GA-PATHFINDER
# Martin Miglio
# 
# This class is a useful datastructure for use throughout
#   this project: position, velocity and acceleration, as
#   well as storing each sequence in a chromosome. This class
#   contains useful functions for working with vectors.
"""

from math import sqrt
import random
import numpy as np


def make_random_vector():
    return random.uniform(-1, 1) * np.random.random((1, 2))[0]


class Vector:
    def __init__(self, array=np.array([0, 0]), random=False):
        if(random):
            self.value = make_random_vector()
        elif isinstance(array, Vector):
            self.value = array.value
        elif isinstance(array, np.ndarray):
            self.value = array
        elif isinstance(array, list):
            self.value = np.array(array)
        else:
            return NotImplemented

    def x(self):
        return self.value[0]

    def y(self):
        return self.value[1]

    def normalize(self):
        if not np.array_equal(self.value, np.array([0, 0])):
            self.value = (self.value) / np.linalg.norm(self.value)
        return self

    def average_with(self, other):
        return Vector((self + other) / 2)

    def distance_from(self, other):
        # sub = (self - other)
        # return sub.magnitude() # slower (see distance_calc_timing.py)
        return sqrt((self.x() - other.x()) ** 2 + (self.y() - other.y()) ** 2)

    def magnitude(self):
        return sqrt(self.x()*self.x() + self.y()*self.y())

    def cross(self, other):
        if isinstance(other, Vector):
            return np.cross(self.value, other.value)
        else:
            return NotImplemented

    def equals(self, other):
        if isinstance(other, Vector):
            return np.array_equal(self.value, other.value, equal_nan=False)
        else:
            return NotImplemented
    # region Overrides

    def __add__(self, other):
        if isinstance(other, np.ndarray):
            return Vector(self.value + other)
        elif isinstance(other, Vector):
            return Vector(self + other.value)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, np.ndarray):
            return Vector(self.value - other)
        elif isinstance(other, Vector):
            return Vector(self - other.value)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.value * other)
        else:
            return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.value * other)
        else:
            return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.value / other)
        else:
            return NotImplemented

    def __str__(self):
        return self.value.__str__()

    def __repr__(self):
        return f'(x:{self.value[0]:.5f} y:{self.value[1]:.5f})'
    # endregion
