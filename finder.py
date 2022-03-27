"""
# finder.py - CS481-GA-PATHFINDER
# Martin Miglio
#
# This file contains the finder class, an object
#   to be controlled by the GA. This class handles
#   the drawing, updating, and fitness calculations.
"""

import math
from chromosome import Chromosome
from vector import Vector
from lib.graphics import Circle, Point


class Finder:

    def __init__(self, chromosome=None, lifespan=0, start_position=Vector()):
        """Finder constructor

        Args:
            chromosome (Chromosome, optional): the genetic information for the
                finder. Defaults to None.
            lifespan (int, optional): the number of steps for a finder.
                Defaults to 0.
            start_position (Vector, optional): a vector describing the
                position to start. Defaults to Vector([0, 0]).
        """
        if chromosome is None:
            self.chromosome = Chromosome()
        else:
            self.chromosome = chromosome
        self.lifespan = lifespan
        self.start_position = start_position
        self.position = self.start_position
        self.velocity = Vector([0, 0])
        self.acceleration = Vector([0, 0])
        self.alive_duration = 0
        self.completed = False
        self.crashed = False
        self.too_old = False
        self.fitness = 0
        self.step = 0
        self.shape = Circle(Point(self.start_position.x(),
                            self.start_position.y()), 5)
        self.shape.setFill('red')

    def calculate_fitness(self, environment):
        """A function to calculate a finder's fitness

        Args:
            environment (Environment): An environment to calculate the
                fitness from

        Returns:
            float: the fitness of the finder
        """
        self.shape.undraw()  # cleanup
        fitness_total = 0
        max_distance = 1.414*500  # the diagonal of the environment area

        # inverse proportionality to distance
        # fitness_total += max_distance / \
        #     self.position.distance_from(environment.target.position)
        # proportionality to distance from start
        fitness_total += self.position.distance_from(
            self.start_position) / max_distance
        # proportionality to duration
        fitness_total += self.alive_duration/self.lifespan
        if self.crashed:
            fitness_total -= 2  # crashed, take away fitness
        if self.too_old:
            fitness_total -= .5  # too old, take away fitness
        if self.completed:
            fitness_total += 10  # finished, add fitness
        self.fitness = fitness_total
        return fitness_total

    def update(self, environment):
        """A function to update a finder

        Args:
            environment (Environment): an environment to update the finder in
        """
        if not self.crashed and not self.completed and not self.too_old:
            # update the physics
            self.position += self.velocity
            self.velocity += self.acceleration
            self.acceleration = self.calculate_acceleration(environment)
            # test collision, completion, and age
            self.crashed = environment.test_collision(
                self.position,
                self.velocity
            )
            self.completed = environment.test_finish(self.position)
            self.too_old = self.step >= self.lifespan
            # step counters
            self.alive_duration += 1
        self.step += 1

    def draw(self, window):
        """A function to draw a finder

        Args:
            window (GraphWin): a window to update the finder in
        """
        if self.step == 0:
            # draw the first frame
            self.shape.draw(window)
        elif not self.crashed and not self.completed and not self.too_old:
            # update the graphic
            self.shape.move(self.velocity.x(), self.velocity.y())
        else:
            # update colors
            if self.crashed:
                self.shape.setFill("pink")
            elif self.completed:
                self.shape.setFill("yellow")
            elif self.too_old:
                self.shape.setFill("gray")

    @staticmethod
    def make_rays(n, mag):
        """A static method to create rays at regular intervals

        Args:
            n (int): number of rays to create
            mag (float): magnitude of rays

        Returns:
            list[Vector]: generated rays
        """
        c = 2*math.pi/n
        return [mag * Vector([math.cos(c*k), math.sin(c*k)]) for k in range(n)]

    def calculate_acceleration(self, env):
        """A function to calculate this step's acceleration

        Args:
            env (Environment): the finder's environment

        Returns:
            Vector: the calulated acceleration
        """
        # create vision rays
        rays = Finder.make_rays(n=8, mag=50)
        # test vision rays for collisions,
        ray_tests = [
            -1 if env.test_collision(self.position, ray) else 1 for ray in rays
        ]
        # supply nn w data
        output = self.chromosome.run(ray_tests)
        # return acceleration based off nn output
        acceleration = Vector([0, 0])
        for (direction, magnitude) in zip(rays, output):
            acceleration += (direction.normalize() * magnitude[0])
        return acceleration

    def get_child(self, other):
        """A function to create a child finder with another

        Args:
            other (Finder): the other finder to make a child with

        Returns:
            Finder: the newly created child finder
        """
        child_chromosome = self.chromosome.crossover(other.chromosome)
        child_chromosome = child_chromosome.get_mutation(rate=0.2)
        return Finder(chromosome=child_chromosome,
                      start_position=self.start_position,
                      lifespan=self.lifespan
                      )
