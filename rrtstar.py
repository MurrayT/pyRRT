__author__ = 'Murray Tannock'

from probabilistic_search import *


def step():
    """
    One step of RRT* generation, see paper for more details
    """
    x_rand = sample_free()
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
        # I deviate from the stated implementation here to check for new goal paths
        if shared.root_path:
            goal_path_resolve(shared.root_path[0])
        goal_path_resolve(shared.nodes[-1])


step.__name__ = "RRT*"