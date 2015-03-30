__author__ = 'Murray Tannock'
"""
This module holds the base functions as described in the paper, as well as a method to resolve goal reachability
"""
import random
import math

import shared
import node


def goal_path_resolve(new_node):
    """
    Checks to see whether a path to the goal exists, updates shared information
    :param new_node: the node to resolve from
    :return: boolean true if new shorter goal path is found.
    """
    if new_node.dist_to((shared.goal.x, shared.goal.y)) < shared.STEP_SIZE:
        # we can step to the goal node
        new_root_path_cost = new_node.cost + new_node.dist_to((shared.goal.x, shared.goal.y))
        if new_root_path_cost < shared.root_path_length:
            shared.root_path_length = new_root_path_cost
            shared.goal.node.delete()
            shared.goal = node.Node(shared.goal.x, shared.goal.y, new_node, "goal")
            shared.nodes.append(shared.goal)
            # backtrace to the root
            for current_node in shared.root_path:
                current_node.deroot_path_color()
            shared.root_path = []
            shared.root_path.append(shared.goal)
            current_node = shared.goal
            while current_node.parent is not None:
                current_node.root_path_color()
                current_node = current_node.parent
                shared.root_path.append(current_node)
            if not shared.continual:
                shared.running = False
            return True
        return False


def sample_free():
    """
    Samples the free areas in the configuration space
    :return: (x,y) point in space
    """
    rand = None
    while rand is None:
        rand = (random.randint(shared.x_domain[0], shared.x_domain[1]),
                random.randint(shared.y_domain[0], shared.y_domain[1]))

        for obs in shared.obstacles:
            if obs.collides_with(rand[0], rand[1]):
                rand = None
                break
    return rand


def steer(node1, other):
    """
    Steers the nearest node towards the new point
    Here is where non-holonomicity would be integrated
    :param node1: point to start from
    :param other: target point to go towards
    :return: new point that results from steering
    """
    if node1.dist_to(other) < shared.STEP_SIZE:
        return other[0], other[1]
    else:
        theta = math.atan2(other[1] - node1.y, other[0] - node1.x)
        x = node1.x + shared.STEP_SIZE * math.cos(theta)
        y = node1.y + shared.STEP_SIZE * math.sin(theta)
        return x, y


def obstacle_free(node1, other):
    """
    Checks to see whether a path between two points intersects an obstacle,
    done by taking equidistant samples along the line between the points
    :param node1: node to work from
    :param other: point to work to
    :return: boolean true if path collides with no obstacles
    """
    dx = other[0] - node1.x
    dy = other[1] - node1.y
    collision_points = [(node1.x + round(i / shared.collision_divisions, 1) * dx,
                         node1.y + round(i / shared.collision_divisions, 1) * dy) for i in
                        range(shared.collision_divisions
                              + 1)]
    for i in collision_points:
        for obs in shared.obstacles:
            if obs.collides_with(i[0], i[1]):
                return False
    return True


def add_node(new, near, get_node=False):
    """
    Adds node to the tree
    :param new: position of new node
    :param near: nearest node in the tree
    :param get_node: boolean if want node returned
    :return: if get_node return node otherwise None
    """
    n = node.Node(new[0], new[1], near)
    shared.nodes.append(n)
    shared.node_count += 1
    goal_path_resolve(shared.nodes[-1])
    if get_node:
        return n


def new_nearest_neighbour(point):
    """
    finds the nearest node in tree to a point in the space
    :param point: point to work from, iterates through all the nodes in the tree,
                  there may be a better way
    :return: nearest node
    """
    current_nearest = shared.nodes[0]
    for this_node in shared.nodes:
        if this_node.dist_to(point) < current_nearest.dist_to(point):
            current_nearest = this_node
    return current_nearest


def new_neighbourhood(point):
    """
    finds the neighbourhood of a point in the tree
    :param point: point to work from
    :return: list of nodes in the tree within neighbourhood
    """
    nh = []
    for this_node in shared.nodes:
        if this_node.dist_to(point) <= shared.neighbourhood_size:
            nh.append(this_node)
    return nh


def sample_unit_ball():
    """
    samples a unit 2-sphere
    :return: x,y distances for the random point generated
    """
    rho = math.sqrt(random.random())
    phi = random.random() * 2 * math.pi
    x = rho * math.cos(phi)
    y = rho * math.sin(phi)
    return x, y