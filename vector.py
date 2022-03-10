import numpy as np


def make_random_vector():
    return np.random.random((1, 2))[0]


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

    def averageWith(self, other):
        return Vector((self + other) / 2)

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
