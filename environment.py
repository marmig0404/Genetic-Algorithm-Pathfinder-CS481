"""
# environment.py - CS481-GA-PATHFINDER
# Martin Miglio
#
# This file contains the classes for handling the environment.
# Collision tracking and drawing are handled here.
"""

from lib.graphics import Circle, Line, Point
from vector import Vector


class Environment:
    def __init__(self, border, target, walls=[]):
        """Environment constructor

        Args:
            border (Border): a border to add to the environment
            target (Target): a target to add to the environment
            walls (list, optional): a list of walls to add to the environment.
                Defaults to [].
        """
        self.border = border
        self.target = target
        self.walls = walls

    def test_finish(self, other):
        """A function to test finish

        Args:
            other (Finder): A finder to test collision with
        """
        return self.target.test_finish(other)

    def test_collision(self, other):
        """A function to test collision

        Args:
            other (Finder): A finder to test collision with
        """
        if len(self.walls) > 0:
            w_collsions = any([w.test_collision(other) for w in self.walls])
        else:
            w_collsions = False
        border_collision = self.border.test_collision(other)
        return w_collsions or border_collision

    def show(self, window):
        """A function to display a border

        Args:
            window (GraphWin): window to add environment to
        """
        self.border.show(window)
        self.target.show(window)
        for wall in self.walls:
            wall.show(window)


class Target:
    def __init__(self, position):
        """Target constructor

        Args:
            position (Vector): A vector describing the target position
        """
        self.position = position
        self.radius = 20
        self.shape = Circle(
            Point(self.position.x(), self.position.y()),
            self.radius
        )
        self.shape.setFill('green')

    def test_finish(self, other):
        """A function to test finish

        Args:
            other (Finder): A finder to test collision with
        """
        return self.position.distance_from(other.position) <= self.radius

    def show(self, window):
        """A function to display a border

        Args:
            window (GraphWin): window to add target to
        """
        self.shape.draw(window)


class Border:
    def __init__(self, top_left, bottom_right):
        """Border constructor

        Args:
            top_left (Vector): A vector pointing to top left corner of border
            bottom_right (Vector): A vector pointing to bottom right
                corner of border
        """
        self.top_wall = Wall(
            top_left,
            Vector([bottom_right.x() - top_left.x(), 0])
        )
        self.left_wall = Wall(
            top_left,
            Vector([0, bottom_right.y() - top_left.y()])
        )
        self.right_wall = Wall(
            bottom_right,
            Vector([0, top_left.y() - bottom_right.y()])
        )
        self.bottom_wall = Wall(
            bottom_right,
            Vector([top_left.x() - bottom_right.x(), 0])
        )
        self.walls = [self.top_wall, self.bottom_wall,
                      self.left_wall, self.right_wall]

    def test_collision(self, other):
        """A function to test collision

        Args:
            other (Finder): A finder to test collision with
        """
        collisions = [wall.test_collision(other) for wall in self.walls]
        return any(collisions)

    def show(self, window):
        """A function to display a border

        Args:
            window (GraphWin): window to add border to
        """
        for wall in self.walls:
            wall.show(window, width=10, fill='gray')


class Wall:
    def __init__(self, position, vector):
        """Wall constructor

        Args:
            position (Vector): position as a vector
            vector (Vector): vector describing wall end-point
        """
        self.position = position
        self.vector = vector

    def test_collision(self, other):
        """A function to test collision

        Args:
            other (Finder): A finder to test collision with
        """
        # math from https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
        def ccw(A, B, C):
            return (C.y()-A.y()) * (B.x()-A.x()) > (B.y()-A.y()) * (C.x()-A.x())
        A = self.position
        B = self.position + self.vector
        C = other.position
        D = other.position + other.velocity
        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

    def show(self, window, width=5, fill='black'):
        """A function to display a wall

        Args:
            window (GraphWin): window to add wall to
            width (int, optional): width of wall in px. Defaults to 5.
            fill (str, optional): color of wall. Defaults to 'black'.
        """
        self.shape = Line(
            Point(self.position.x(), self.position.y()),
            Point(self.position.x() + self.vector.x(),
                  self.position.y() + self.vector.y())
        )
        self.shape.setWidth(width)
        self.shape.setFill(fill)
        self.shape.draw(window)
