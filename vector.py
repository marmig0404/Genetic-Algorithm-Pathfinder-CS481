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


class Vector:
    def __init__(self, array=np.array([0, 0]), random=False):
        """Vector constructor

        Args:
            array (Vector OR np.ndarray OR list, optional): values to
                initalize the vector. Defaults to np.array([0, 0]).
            random (bool, optional): if true, will create a random vector.
                Defaults to False.

        Returns:
            _type_: _description_
        """
        if(random):
            self.value = Vector.make_random_vector()
        elif isinstance(array, Vector):
            self.value = array.value
        elif isinstance(array, np.ndarray):
            self.value = array
        elif isinstance(array, list):
            self.value = np.array(array)
        else:
            return NotImplemented

    @staticmethod
    def make_random_vector():
        """A function to create a random numpy vector

        Returns:
            numpy.ndarray: a random numpy vector
        """
        return random.uniform(-1, 1) * np.random.random((1, 2))[0]

    def x(self):
        """a function to get the x component of the vector

        Returns:
            int: the x component of the vector
        """
        return self.value[0]

    def y(self):
        """a function to get the y component of the vector

        Returns:
            int: the y component of the vector
        """
        return self.value[1]

    def normalize(self):
        """A function to normalize a vector

        Returns:
            Vector: the normalized vector
        """
        if not np.array_equal(self.value, np.array([0, 0])):
            self.value = (self.value) / np.linalg.norm(self.value)
        return self

    def average_with(self, other):
        """A function to average two vectors

        Args:
            other (Vector): a vector to be averaged with

        Returns:
            Vector: the averaged vector
        """
        return Vector((self + other) / 2)

    def distance_from(self, other):
        """A function to find the distance between vectors

        Args:
            other (Vector): a vector to find the distance from

        Returns:
            float: the distance from the other vector
        """
        # sub = (self - other)
        # return sub.magnitude() # slower (see distance_calc_timing.py)
        return sqrt((self.x() - other.x()) ** 2 + (self.y() - other.y()) ** 2)

    def magnitude(self):
        """A function to retrieve the magnitude of the vector

        Returns:
            float: the vector's magnitude
        """
        return sqrt(self.x()*self.x() + self.y()*self.y())

    def cross(self, other):
        """A function to calculate the cross product of two vectors

        Args:
            other (Vector): the vector to cross with

        Returns:
            int: the vectors' cross product
        """
        if isinstance(other, Vector):
            return np.cross(self.value, other.value)
        else:
            return NotImplemented

    def equals(self, other):
        """A function for testing vector equality

        Args:
            other (Vector): a vector to compare to

        Returns:
            bool: a boolean describing equality
        """
        if isinstance(other, Vector):
            return np.array_equal(self.value, other.value, equal_nan=False)
        else:
            return NotImplemented
    # region Overrides

    def __add__(self, other):
        """A function to add vectors

        Args:
            other (Vector): the vector to operate with

        Returns:
            Vector: the operated vector
        """
        if isinstance(other, np.ndarray):
            return Vector(self.value + other)
        elif isinstance(other, Vector):
            return Vector(self + other.value)
        else:
            return NotImplemented

    def __sub__(self, other):
        """A function to subtract vectors

        Args:
            other (Vector): the vector to operate with

        Returns:
            Vector: the operated vector
        """
        if isinstance(other, np.ndarray):
            return Vector(self.value - other)
        elif isinstance(other, Vector):
            return Vector(self - other.value)
        else:
            return NotImplemented

    def __mul__(self, other):
        """A function to multiply vectors

        Args:
            other (Vector): the vector to operate with

        Returns:
            Vector: the operated vector
        """
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.value * other)
        else:
            return NotImplemented

    def __rmul__(self, other):
        """A function to reverse multiply vectors

        Args:
            other (Vector): the vector to operate with

        Returns:
            Vector: the operated vector
        """
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.value * other)
        else:
            return NotImplemented

    def __truediv__(self, other):
        """A function to divide vectors

        Args:
            other (Vector): the vector to operate with

        Returns:
            Vector: the operated vector
        """
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.value / other)
        else:
            return NotImplemented

    def __str__(self):
        """A function to create a string representation of a vector

        Returns:
            String: a string representation
        """
        return self.value.__str__()

    def __repr__(self):
        """A function to create a string representation of a vector

        Returns:
            String: a string representation
        """
        return f'(x:{self.value[0]:.5f} y:{self.value[1]:.5f})'
    # endregion
