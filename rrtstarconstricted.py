__author__ = 'Murray Tannock'
import sys

import ellipse
from probabilistic_search import *


def step():
    """
    One step of constricted RRT* generation, see paper for more details
    """
    x_rand = sample()
    x_nearest = new_nearest_neighbour(x_rand)
    x_new = steer(x_nearest, x_rand)
    if obstacle_free(x_nearest, x_new):
        X_near = new_neighbourhood(x_new)
        x_min = x_nearest
        c_min = x_nearest.cost + x_nearest.dist_to(x_new)
        for x_near in X_near:
            if obstacle_free(x_near, x_new) and (x_near.cost + x_near.dist_to(x_new) < c_min):
                x_min = x_near
                c_min = (x_near.cost + x_near.dist_to(x_new) < c_min)
        x_new_node = add_node(x_new, x_min, True)
        for x_near in X_near:
            if obstacle_free(x_near, x_new) and (x_new_node.cost + x_near.dist_to(x_new) < x_near.cost):
                x_near.change_parent(x_new_node)
    # Here I check for goal paths and draw the circle
    updated = False
    if shared.root_path:
        updated = goal_path_resolve(shared.root_path[0])
    updated = updated or goal_path_resolve(shared.nodes[-1])
    if updated:
        diameter = shared.root_path_length
        center = ((shared.root_path[0].x + shared.root_path[-1].x) / 2,
                  (shared.root_path[0].y + shared.root_path[-1].y) / 2)
        if shared.region:
            shared.region.remove_from_batch()
        shared.region = ellipse.Ellipse(center[0], center[1], diameter)
        shared.region.add_to_batch()


def sample():
    """
    sampling method for constricted RRT* paper gives more details.
    """
    if shared.root_path_length < sys.maxsize:
        # We make a circle
        center = ((shared.root_path[0].x + shared.root_path[-1].x) / 2,
                  (shared.root_path[0].y + shared.root_path[-1].y) / 2)
        r = shared.root_path_length / 2
        while True:
            x, y = sample_unit_ball()
            x *= r
            y *= r
            x += center[0]
            y += center[1]
            if shared.x_domain[1] > x > shared.x_domain[0] and shared.y_domain[1] > y > shared.y_domain[0]:
                return x, y
    else:
        return sample_free()


step.__name__ = "cRRT*"