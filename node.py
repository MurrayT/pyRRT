__author__ = 'Murray Tannock'

import math
import shared
from pyglet import gl


class Node(object):

    def __init__(self, x, y, parent=None, node_type="normal"):
        self.x = x
        self.y = y
        self.parent = parent
        self.children = []
        self.type = node_type
        if self.parent is None:
            self.cost = 0
        else:
            self.cost = self.parent.cost + self.dist_to((self.parent.x, self.parent.y))

        if self.parent is not None:
            self.parent.children.append(self)
            self.line = shared.batch.add(2, gl.GL_LINES, None,
                                         ('v2f', (self.parent.x, self.parent.y,
                                                  self.x, self.y)))

        if node_type == "normal":
            self.node = shared.batch.add(4, gl.GL_QUADS, None,
                                         ('v2f', (self.x-1, self.y+1,
                                                  self.x+1, self.y+1,
                                                  self.x+1, self.y-1,
                                                  self.x-1, self.y-1)))
        if node_type == "root":
            self.node = shared.batch.add(4, gl.GL_QUADS, None,
                                         ('v2f', (self.x-5, self.y+5,
                                                  self.x+5, self.y+5,
                                                  self.x+5, self.y-5,
                                                  self.x-5, self.y-5)),
                                         ('c3B', (255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0)))
        if node_type == "goal":
            self.node = shared.batch.add(4, gl.GL_QUADS, None,
                                         ('v2f', (self.x-5, self.y+5,
                                                  self.x+5, self.y+5,
                                                  self.x+5, self.y-5,
                                                  self.x-5, self.y-5)),
                                         ('c3B', (0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0)))

    def __str__(self):
        return "(%s,%s)" % (self.x, self.y)

    def __repr__(self):
        return "(%s,%s)" % (self.x, self.y)

    def dist_to(self, other):
        return math.sqrt((self.x - other[0]) * (self.x - other[0]) +
                         (self.y - other[1]) * (self.y - other[1]))

    def step_to(self, other):
        if self.dist_to(other) < shared.STEP_SIZE:
            for obstacle in shared.obstacles:
                if obstacle.collides_with(other[0], other[1]):
                    return None
            n = Node(other[0], other[1], self)
        else:
            theta = math.atan2(other[1]-self.y, other[0]-self.x)
            x = self.x + shared.STEP_SIZE*math.cos(theta)
            y = self.y + shared.STEP_SIZE*math.sin(theta)
            for obstacle in shared.obstacles:
                if obstacle.collides_with(x, y):
                    return None
            n = Node(x, y, self)

        return n

    def step_to_point(self, other):
        if self.dist_to(other) <= shared.STEP_SIZE:
            for obstacle in shared.obstacles:
                if obstacle.collides_with(other[0], other[1]):
                    return None
            n = (other[0], other[1])
        else:
            theta = math.atan2(other[1]-self.y, other[0]-self.x)
            x = self.x + shared.STEP_SIZE*math.cos(theta)
            y = self.y + shared.STEP_SIZE*math.sin(theta)
            for obstacle in shared.obstacles:
                if obstacle.collides_with(x, y):
                    return None
            n = (x, y)

        return n

    def root_path_color(self):
        self.line.delete()
        self.line = shared.batch.add(2, gl.GL_LINES, None,
                                     ('v2f', (self.parent.x, self.parent.y,
                                              self.x, self.y)),
                                     ('c3B', (0, 255, 255,
                                              0, 255, 255)))
        if self.type == "normal":
            self.node.delete()
            self.node = shared.batch.add(4, gl.GL_QUADS, None,
                                         ('v2f', (self.x-2.5, self.y+2.5,
                                                  self.x+2.5, self.y+2.5,
                                                  self.x+2.5, self.y-2.5,
                                                  self.x-2.5, self.y-2.5)),
                                         ('c3B', (0, 255, 255,
                                                  0, 255, 255,
                                                  0, 255, 255,
                                                  0, 255, 255)))
            self.line.delete()
            self.line = shared.batch.add(2, gl.GL_LINES, None,
                                         ('v2f', (self.parent.x, self.parent.y,
                                                  self.x, self.y)),
                                         ('c3B', (0, 255, 255,
                                                  0, 255, 255)))

    def deroot_path_color(self):
        if self.type != "root":
            self.line.delete()
            self.line = shared.batch.add(2, gl.GL_LINES, None,
                                         ('v2f', (self.parent.x, self.parent.y,
                                                  self.x, self.y)))
        if self.type == "normal":
            self.node.delete()
            self.node = shared.batch.add(4, gl.GL_QUADS, None,
                                         ('v2f', (self.x-1, self.y+1,
                                                  self.x+1, self.y+1,
                                                  self.x+1, self.y-1,
                                                  self.x-1, self.y-1)))

    def update_cost(self):
        self.cost = self.parent.cost + self.dist_to((self.parent.x, self.parent.y))
        for child in self.children:
            child.update_cost()

    def change_parent(self, new_parent):
        if self.parent:
            self.line.delete()
            self.parent.children.remove(self)

        new_parent.children.append(self)
        self.parent = new_parent
        self.update_cost()
        self.line = shared.batch.add(2, gl.GL_LINES, None,
                                     ('v2f', (self.parent.x, self.parent.y,
                                              self.x, self.y)))

    def neighbourhood(self):
        nh = []
        for this_node in shared.nodes:
            if self.dist_to((this_node.x, this_node.y)) <= shared.neighbourhood_size:
                nh.append(this_node)
        return nh

    def best_neighbour(self, neighbourhood):
        current_best = self.parent
        for this_node in neighbourhood:
            if self.cost > this_node.cost + this_node.dist_to((self.x, self.y)):
                current_best = this_node
        return current_best


def nearest_neighbour(x, y):
    current_nearest = shared.nodes[0]
    for this_node in shared.nodes:
        if this_node.dist_to((x, y)) < current_nearest.dist_to((x, y)):
            current_nearest = this_node
    return current_nearest