"""
# chromosome.py - CS481-GA-PATHFINDER
# Martin Miglio
# 
# This class handles the genetic processing, including
#   the crossover and mutation functions.
"""

import random

from vector import Vector


class Chromosome:
    def __init__(self, genes=None, lifespan=None, magnitude=1):
        # Recieves genes and create a dna object
        self.magnitude = magnitude
        if genes is not None:
            self.genes = genes
        # If no genes just create random dna
        else:
            self.genes = []
            for _ in range(lifespan):
                # Gives random vector
                random_vector = Vector(random=True).normalize()
                self.genes.append(magnitude*random_vector)

    def crossover(self, partner):
        # Performs a crossover with another member of the species
        newgenes = []
        # Picks random midpoint
        split_index = random.randint(1, len(self.genes))
        for index in range(len(self.genes)):
            if index > split_index:
                newgenes.append(self.genes[index])
            else:
                newgenes.append(partner.genes[index])
        # Gives DNA object an array
        return Chromosome(genes=newgenes, magnitude=self.magnitude)

    def get_mutation(self, rate=0.5):
        # Adds random mutation to the genes to add variance.
        mutated_genes = []
        for i in range(len(self.genes)):
            adjrand = random.random()
            if adjrand < rate:
                mutated_genes.append(
                    self.magnitude * Vector(random=True).average_with(self.genes[i]).normalize())
            else:
                mutated_genes.append(self.genes[i])
        return Chromosome(genes=mutated_genes, magnitude=self.magnitude)

    def get_value(self, index):
        return self.genes[index]
