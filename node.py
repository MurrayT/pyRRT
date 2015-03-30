__author__ = 'Murray Tannock'

import math

from pyglet import gl

import shared


class Node(object):
    """
    Node class for use in graphics manipulation, and cost calculations
    """
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
        # colours node based on itss type
        if node_type == "normal":
            self.node = shared.batch.add(4, gl.GL_QUADS, None,
                                         ('v2f', (self.x - 1, self.y + 1,
                                                  self.x + 1, self.y + 1,
                                                  self.x + 1, self.y - 1,
                                                  self.x - 1, self.y - 1)))
        if node_type == "root":
            self.node = shared.batch.add(4, gl.GL_QUADS, None,
                                         ('v2f', (self.x - 5, self.y + 5,
                                                  self.x + 5, self.y + 5,
                                                  self.x + 5, self.y - 5,
                                                  self.x - 5, self.y - 5)),
                                         ('c3B', (255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0)))
        if node_type == "goal":
            self.node = shared.batch.add(4, gl.GL_QUADS, None,
                                         ('v2f', (self.x - 5, self.y + 5,
                                                  self.x + 5, self.y + 5,
                                                  self.x + 5, self.y - 5,
                                                  self.x - 5, self.y - 5)),
                                         ('c3B', (0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0)))

    def __str__(self):
        return "(%s,%s)" % (self.x, self.y)

    def __repr__(self):
        return "(%s,%s)" % (self.x, self.y)

    def dist_to(self, other):
        """
        calculates distance between this node and another point
        :param other: other point
        :return: float distance between points
        """
        return math.sqrt((self.x - other[0]) * (self.x - other[0]) +
                         (self.y - other[1]) * (self.y - other[1]))

    def root_path_color(self):
        """
        Colours the path to the root, used in goal highlighting
        :return:
        """
        self.line.delete()
        self.line = shared.batch.add(2, gl.GL_LINES, None,
                                     ('v2f', (self.parent.x, self.parent.y,
                                              self.x, self.y)),
                                     ('c3B', (0, 255, 255,
                                              0, 255, 255)))
        if self.type == "normal":
            self.node.delete()
            self.node = shared.batch.add(4, gl.GL_QUADS, None,
                                         ('v2f', (self.x - 2.5, self.y + 2.5,
                                                  self.x + 2.5, self.y + 2.5,
                                                  self.x + 2.5, self.y - 2.5,
                                                  self.x - 2.5, self.y - 2.5)),
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
        """
        Removes colour from the root path, used when this is no longer the best path
        :return: None
        """
        if self.type != "root":
            self.line.delete()
            self.line = shared.batch.add(2, gl.GL_LINES, None,
                                         ('v2f', (self.parent.x, self.parent.y,
                                                  self.x, self.y)))
        if self.type == "normal":
            self.node.delete()
            self.node = shared.batch.add(4, gl.GL_QUADS, None,
                                         ('v2f', (self.x - 1, self.y + 1,
                                                  self.x + 1, self.y + 1,
                                                  self.x + 1, self.y - 1,
                                                  self.x - 1, self.y - 1)))

    def update_cost(self):
        """
        updates cost of reaching node after parent changes
        :return:
        """
        self.cost = self.parent.cost + self.dist_to((self.parent.x, self.parent.y))
        for child in self.children:
            child.update_cost()

    def change_parent(self, new_parent):
        """
        Changes the parent of node and updates graphics and costs
        :param new_parent:
        :return:
        """
        if self.parent:
            self.line.delete()
            self.parent.children.remove(self)

        new_parent.children.append(self)
        self.parent = new_parent
        self.update_cost()
        self.line = shared.batch.add(2, gl.GL_LINES, None,
                                     ('v2f', (self.parent.x, self.parent.y,
                                              self.x, self.y)))