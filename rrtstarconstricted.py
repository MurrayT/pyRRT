__author__ = 'Murray Tannock'

import random
import math
import ellipse
from probabilistic_search import *


def step():
    x_domain = shared.x_domain
    y_domain = shared.y_domain
    rand = (random.randint(x_domain[0], x_domain[1]), random.randint(y_domain[0], y_domain[1]))
    if shared.root_path:
        diameter = shared.root_path_length
        rho = math.sqrt(random.random())
        phi = random.random() * 2 * math.pi
        center = ((shared.root_path[0].x+shared.root_path[-1].x)/2,
                  (shared.root_path[0].y+shared.root_path[-1].y)/2)
        x = rho * math.cos(phi)
        y = rho * math.sin(phi)
        x *= diameter/2
        y *= diameter/2
        rand = (x+center[0], y+center[1])
    if x_domain[1] > rand[0] > x_domain[0] and y_domain[1] > rand[1] > y_domain[0]:
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
            updated = False
            if shared.root_path:
                updated = goal_path_resolve(shared.root_path[0])
            updated = updated or goal_path_resolve(shared.nodes[-1])
            if updated:
                diameter = shared.root_path_length
                center = ((shared.root_path[0].x+shared.root_path[-1].x)/2,
                          (shared.root_path[0].y+shared.root_path[-1].y)/2)
                if shared.region:
                    shared.region.remove_from_batch()
                shared.region = ellipse.Ellipse(center[0], center[1], diameter)
                shared.region.add_to_batch()
step.__name__ = "RRT*Constricted"