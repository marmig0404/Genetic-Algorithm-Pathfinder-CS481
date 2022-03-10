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
        return Chromosome(newgenes, magnitude=self.magnitude)

    def mutation(self, rate=0.5):
        # Adds random mutation to the genes to add variance.
        for i in range(len(self.genes)):
            adjrand = random.random()
            if adjrand < rate:
                self.genes[i] = self.magnitude * \
                    Vector(random=True).averageWith(self.genes[i]).normalize()
