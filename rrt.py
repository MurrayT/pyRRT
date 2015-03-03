__author__ = 'Murray Tannock'
import random

from probabilistic_search import *


def step():
    rand = (random.randint(shared.x_domain[0], shared.x_domain[1]),
            random.randint(shared.y_domain[0], shared.y_domain[1]))
    nearest_in = node.nearest_neighbour(rand[0], rand[1])
    next_node = nearest_in.step_to(rand)
    if next_node is not None:
        shared.nodes.append(next_node)
        shared.node_count += 1
        goal_path_resolve(shared.nodes[-1])


step.__name__ = "RRT"