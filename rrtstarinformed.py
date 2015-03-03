__author__ = 'murraytannock'

import random
import math
import ellipse
from probabilistic_search import *


def step():
    xdomain = shared.xdomain
    ydomain = shared.ydomain
    rand = (random.randint(xdomain[0], xdomain[1]), random.randint(ydomain[0], ydomain[1]))
    if shared.root_path:
        major = shared.root_path_length
        minor = math.sqrt(major**2 - shared.root_path[0].dist_to((shared.root_path[-1].x, shared.root_path[-1].y))**2)
        angle = math.atan2(shared.root_path[0].y-shared.root_path[-1].y, shared.root_path[0].x - shared.root_path[-1].x)
        rho = math.sqrt(random.random())
        phi = random.random() * 2 * math.pi
        center = ((shared.root_path[0].x+shared.root_path[-1].x)/2,
                  (shared.root_path[0].y+shared.root_path[-1].y)/2)
        x = rho * math.cos(phi)
        y = rho * math.sin(phi)
        x *= major/2
        y *= minor/2
        x, y = x*math.cos(angle)-y*math.sin(angle), \
               x*math.sin(angle)+y*math.cos(angle)
        if not shared.region:
            shared.region = ellipse.Ellipse(center[0], center[1], major, minor, angle)
            shared.region.add_to_batch()
        else:
            shared.region.remove_from_batch()
            shared.region = ellipse.Ellipse(center[0], center[1], major, minor, angle)
            shared.region.add_to_batch()
        rand = (x+center[0], y+center[1])
    if xdomain[1] > rand[0] > xdomain[0] and ydomain[1] > rand[1] > ydomain[0]:
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
                major = shared.root_path_length
                minor = math.sqrt(major**2 - shared.root_path[0].dist_to((shared.root_path[-1].x, shared.root_path[-1].y))**2)
                angle = math.atan2(shared.root_path[0].y-shared.root_path[-1].y, shared.root_path[0].x - shared.root_path[-1].x)
                center = ((shared.root_path[0].x+shared.root_path[-1].x)/2,
                          (shared.root_path[0].y+shared.root_path[-1].y)/2)
                if shared.region:
                    shared.region.remove_from_batch()
                shared.region = ellipse.Ellipse(center[0], center[1], major, minor, angle)
                shared.region.add_to_batch()

step.__name__ = "RRT*Informed"