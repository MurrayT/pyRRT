__author__ = 'Murray Tannock'

import math

from pyglet import gl

import shared


class Ellipse(object):
    segments = 40

    def __init__(self, x, y, width, height=None, rotation=0):
        if height is None:
            height = width
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation - math.pi
        self.line = None

    def add_to_batch(self):
        points = []
        colors = []
        for i in range(Ellipse.segments):
            angle = (i / Ellipse.segments) * 2 * math.pi
            x = math.cos(angle)
            y = math.sin(angle)
            x *= self.width / 2
            y *= self.height / 2
            x, y = x * math.cos(self.rotation) - y * math.sin(self.rotation), \
                   x * math.sin(self.rotation) + y * math.cos(self.rotation)
            x += self.x
            y += self.y
            points.append(x)
            points.append(y)
            colors.append(255)
            colors.append(0)
            colors.append(255)

        t = tuple(points)
        ct = tuple(colors)
        self.line = shared.batch.add(Ellipse.segments, gl.GL_LINE_LOOP, None, ('v2f', t), ('c3B', ct))

    def remove_from_batch(self):
        self.line.delete()
