"""
# population.py - CS481-GA-PATHFINDER
# Martin Miglio
# 
# This file handles the genetic algorithm,
#   running a trial, calling for breeding,
#   and repeating.
"""

import random

from finder import Finder
from lib.graphics import Point, Text


class Population:

    def __init__(self, size, lifespan, start_position, window):
        self.size = size
        self.finders = []
        for _ in range(size):
            self.finders.append(
                Finder(lifespan=lifespan, start_position=start_position))
        self.fitness_readout = Text(Point(250, 520), "")
        self.fitness_readout.draw(window)

    def run(self, window, environment):
        alive_count = 0
        for finder in self.finders:
            finder.update(window, environment)
            if not (finder.crashed or finder.completed):
                alive_count += 1
        if alive_count == 0:
            self.step(environment)

    def step(self, environment):
        sorted_finders = sorted(
            self.finders,
            key=lambda finder: finder.calculate_fitness(environment),
            reverse=True
        )
        average_fitness = sum(
                finder.fitness for finder in self.finders)/len(self.finders)
        self.fitness_readout.setText(
            f"Last round's average fitness: {average_fitness}")
        cutoff = self.size / 2 if self.size % 2 == 0 else (self.size + 1) / 2
        mating_pool = sorted_finders[0:int(cutoff) + 1]
        new_finders = []
        for _ in range(self.size):
            first_parent = random.choice(mating_pool)
            second_parent = random.choice(mating_pool)
            new_finders.append(first_parent.get_child(second_parent))
        self.finders = new_finders[0:self.size]
