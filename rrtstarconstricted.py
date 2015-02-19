__author__ = 'murraytannock'

import random
import math
from probabilistic_search import *


def step():
    xdomain = shared.xdomain
    ydomain = shared.ydomain
    if shared.root_path:
        xvals = [point.x for point in shared.root_path]
        xdomain = (int(math.floor(min(xvals))), int(math.ceil(max(xvals))))
        yvals = [point.y for point in shared.root_path]
        ydomain = (int(math.floor(min(yvals))), int(math.ceil(max(yvals))))
    rand = (random.randint(xdomain[0], xdomain[1]), random.randint(ydomain[0], ydomain[1]))
    nearest_in = node.nearest_neighbour(rand[0], rand[1])
    next_node = nearest_in.step_to(rand)
    if next_node is not None:
        neighbourhood = next_node.neighbourhood()
        best_neighbour = next_node.best_neighbour(neighbourhood)
        if next_node.parent != best_neighbour:
            next_node.change_parent(best_neighbour)
        for neighbour in neighbourhood:
            if next_node.cost + next_node.dist_to((neighbour.x, neighbour.y)) < neighbour.cost:
                neighbour.change_parent(next_node)
        shared.nodes.append(next_node)
        shared.node_count += 1
        if shared.root_path:
            goal_path_resolve(shared.root_path[0])
        goal_path_resolve(shared.nodes[-1])

step.__name__ = "RRT*Constricted"