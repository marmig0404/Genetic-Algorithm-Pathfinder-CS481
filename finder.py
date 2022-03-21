"""
# finder.py - CS481-GA-PATHFINDER
# Martin Miglio
#
# This file contains the finder class, an object
#   to be controlled by the GA. This class handles
#   the drawing, updating, and fitness calculations.
"""

from chromosome import Chromosome
from vector import Vector
from lib.graphics import Circle, Point


class Finder:

    def __init__(self, chromosome=None, lifespan=0, start_position=Vector([0, 0])):
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
            self.chromosome = Chromosome(lifespan=lifespan)
        else:
            self.chromosome = chromosome
        self.lifespan = len(self.chromosome.genes)
        self.start_position = start_position
        self.position = self.start_position
        self.velocity = Vector([0, 0])
        self.acceleration = Vector([0, 0])
        self.alive_duration = 0
        self.completed = False
        self.crashed = False
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
        fitness_total = 0
        max_distance = 1.414*500  # the diagonal of the environment area
        distance_to_target = self.position.distance_from(
            environment.target.position)
        # inverse proportionality to distance
        fitness_total += max_distance/distance_to_target
        # proportionality to duration
        fitness_total += self.alive_duration/self.lifespan
        if self.crashed:
            fitness_total -= 2  # crashed, take away fitness
        if self.completed:
            fitness_total += 10  # finished, add fitness
        self.fitness = fitness_total
        return fitness_total

    def update(self, window, environment):
        """A function to update a finder

        Args:
            window (GraphWin): a window to update the finder in
            environment (Environment): an environment to update the finder in
        """
        # draw the first frame
        if self.step == 0:
            self.shape.draw(window)
        # if out of steps in chromosome, crash the finder
        if self.step >= self.lifespan:
            self.crashed = True
        if not self.crashed and not self.completed:
            self.alive_duration += 1
            # update the physics
            self.position += self.velocity
            self.velocity += self.acceleration
            self.acceleration = self.chromosome.get_value(self.step)
            # test collision and completion
            self.crashed = environment.test_collision(self)
            self.completed = environment.test_finish(self)
            # update the graphic
            self.shape.move(self.velocity.x(), self.velocity.y())
        if self.crashed:
            self.shape.setFill("pink")
        if self.completed:
            self.shape.setFill("yellow")
        self.step += 1

    def get_child(self, other):
        """A function to create a child finder with another

        Args:
            other (Finder): the other finder to make a child with

        Returns:
            Finder: the newly created child finder
        """
        mutation_rate = 0.05  # tuned mutation rate (5%)
        child_chromosome = self.chromosome.crossover(other.chromosome)
        child_chromosome = child_chromosome.get_mutation(mutation_rate)
        child = Finder(chromosome=child_chromosome,
                       start_position=self.start_position)
        return child
