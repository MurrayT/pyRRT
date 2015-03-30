__author__ = 'Murray Tannock'
import random
import math

import shared
import node


def goal_path_resolve(new_node):
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
    if node1.dist_to(other) < shared.STEP_SIZE:
        return other[0], other[1]
    else:
        theta = math.atan2(other[1] - node1.y, other[0] - node1.x)
        x = node1.x + shared.STEP_SIZE * math.cos(theta)
        y = node1.y + shared.STEP_SIZE * math.sin(theta)
        return x, y


def obstacle_free(node1, other):
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
    n = node.Node(new[0], new[1], near)
    shared.nodes.append(n)
    shared.node_count += 1
    goal_path_resolve(shared.nodes[-1])
    if get_node:
        return n


def new_nearest_neighbour(point):
    current_nearest = shared.nodes[0]
    for this_node in shared.nodes:
        if this_node.dist_to(point) < current_nearest.dist_to(point):
            current_nearest = this_node
    return current_nearest


def new_neighbourhood(point):
    nh = []
    for this_node in shared.nodes:
        if this_node.dist_to(point) <= shared.neighbourhood_size:
            nh.append(this_node)
    return nh