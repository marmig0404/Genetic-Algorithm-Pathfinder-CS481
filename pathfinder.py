"""
# pathfinder.py - CS481-GA-PATHFINDER
# Martin Miglio
#
# Pathfinder runs a genetic algorithm to control
#   finders to intercept a target in an environment
#   while avoiding walls.
"""

import time
from vector import Vector
from environment import Environment, Border, Target, Wall
from population import Population
from lib.graphics import GraphWin, update


if __name__ == "__main__":
    # make window to display GUI
    window = GraphWin("Path Finder", 500, 550, autoflush=False)

    # swerve is a challeneging environment for testing
    swerve = Environment(
        border=Border(Vector([20, 20]), Vector([480, 480])),
        target=Target(Vector([450, 250])),
        walls=[
            Wall(Vector([150, 20]), Vector([0, 230])),
            Wall(Vector([230, 480]), Vector([0, -230])),
            Wall(Vector([310, 20]), Vector([0, 230]))
        ]
    )

    # simple is an almost empty environment for testing
    simple = Environment(
        border=Border(Vector([20, 20]), Vector([480, 480])),
        target=Target(Vector([450, 250])),
        walls=[]
    )

    # select environment from above and display
    environment = swerve
    environment.show(window)

    # define the population
    population = Population(
        size=35,
        lifespan=250,
        start_position=Vector([50, 250]),
        window=window
    )

    # run the window
    while(not window.isClosed()):
        # process the population
        population.run(window, environment)
        # update the window
        update()
        # sleep for a short time between frames
        time.sleep(1/500)
