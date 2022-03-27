"""
# chromosome.py - CS481-GA-PATHFINDER
# Martin Miglio
#
# This class handles the genetic processing, including
#   the crossover and mutation functions.
"""

import random

import numpy as np

from nueralnetwork import NueralNetwork


class Chromosome:
    def __init__(self, genes=None, magnitude=1):
        """Chromosome constructor

        Args:
            genes (Chromosome, optional): the genetic information to start
                with. Defaults to None.
            lifespan (int, optional): the number of steps to hold information
                for. Defaults to None.
            magnitude (int, optional): the maximum magnitude for genetic
                information. Defaults to 1.
        """
        # Recieves genes and create a dna object
        self.magnitude = magnitude
        if genes is not None:
            self.genes = genes
        # If no genes just create random dna
        else:
            self.genes = NueralNetwork(8, 8, 4, 4)

    def crossover(self, partner):
        """A function to crossover two chromosomes

        Args:
            partner (Chromosome): another Chromosome object

        Returns:
            Chromosome: the crossedover chromosome
        """

        new = Chromosome(magnitude=self.magnitude)

        new.genes.weights_in_hidden_A = self.crossover_weights(
            self.genes.weights_in_hidden_A,
            partner.genes.weights_in_hidden_A
        )

        new.genes.weights_hidden_A_hidden_B = self.crossover_weights(
            self.genes.weights_hidden_A_hidden_B,
            partner.genes.weights_hidden_A_hidden_B
        )

        new.genes.weights_hidden_B_out = self.crossover_weights(
            self.genes.weights_hidden_B_out,
            partner.genes.weights_hidden_B_out
        )

        return new

    @staticmethod
    def crossover_weights(weights_A, weights_B):
        shape = weights_A.shape
        flat_A = weights_A.flatten()
        flat_B = weights_B.flatten()
        split = random.randrange(0, len(flat_A))
        new = np.append(flat_A[:split], flat_B[split:])
        return new.reshape(shape)

    def get_mutation(self, rate=0.5):
        """A function to get a mutated chromosome

        Args:
            rate (float, optional): the rate of mutation. Defaults to 0.5.

        Returns:
            Chromosome: the mutated chromosome
        """
        new = Chromosome(magnitude=self.magnitude)

        weights_list = [
            self.genes.weights_in_hidden_A,
            self.genes.weights_hidden_A_hidden_B,
            self.genes.weights_hidden_B_out
        ]

        for index, weights in enumerate(weights_list):
            shape = weights.shape
            flat = weights.flatten()
            random_indecies = random.sample(
                range(0, len(flat)), int(len(flat)*rate))
            for random_index in random_indecies:
                flat[random_index] *= random.uniform(-1, 1)
            weights_list[index] = flat.reshape(shape)

        new.genes.weights_in_hidden_A = weights_list[0]
        new.genes.weights_hidden_A_hidden_B = weights_list[1]
        new.genes.weights_hidden_B_out = weights_list[2]

        return new

    def run(self, input):
        return self.genes.run(input)
