__author__ = 'Murray Tannock'

from probabilistic_search import *


def step():
    """
    One step of RRT generation, see paper for more details
    """
    x_rand = sample_free()
    x_near = new_nearest_neighbour(x_rand)
    x_new = steer(x_near, x_rand)
    if obstacle_free(x_near, x_new):
        add_node(x_new, x_near)

step.__name__ = "RRT"