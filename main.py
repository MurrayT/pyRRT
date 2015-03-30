#!/usr/bin/env python3
__author__ = 'Murray Tannock'
import sys
import random
from itertools import cycle

import pyglet
from pyglet import gl
from pyglet.window import key
from pyglet.window import mouse

import node
import obstacle
import rrt
import rrtstar
import rrtstarconstricted
import rrtstarinformed
import shared
import jsonify


methods = [rrt.step, rrtstar.step, rrtstarconstricted.step, rrtstarinformed.step]
meth_cycle = cycle(methods)

fps_display = pyglet.clock.ClockDisplay()


def method_cycle():
    """
    Gets next element in the cycle of methods
    :return: method
    """
    return next(meth_cycle)


# noinspection PyUnusedLocal
def update(dt):
    """
    pyglet update
    :param dt: We don't care about no dt
    :return: none
    """
    path_cost = None
    if shared.running:
        if shared.node_count < shared.max_nodes:
            shared.method()
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glLoadIdentity()
    if shared.root_path_length != sys.maxsize:
        path_cost = pyglet.text.Label("Path Cost: %6.2f" % shared.root_path_length,
                                      font_size=18,
                                      x=shared.window_width // 3, y=24,
                                      anchor_x='center', anchor_y='center',
                                      color=(128, 128, 128, 128))
    node_label = pyglet.text.Label("Nodes: %d" % shared.node_count,
                                   font_size=18,
                                   x=2 * shared.window_width // 3, y=24,
                                   anchor_x='center', anchor_y='center',
                                   color=(128, 128, 128, 128))
    label = pyglet.text.Label(shared.method.__name__,
                              font_size=36,
                              x=shared.window_width - 10, y=24,
                              anchor_x='right', anchor_y='center',
                              color=(128, 128, 128, 128))
    pyglet.graphics.draw(4, gl.GL_QUADS,
                         ('v2f', (0, 50,
                                  shared.window_width, 50,
                                  shared.window_width, 48,
                                  0, 48)),
                         ('c4f', (0.5, 0.5, 0.5, 0.5,
                                  0.5, 0.5, 0.5, 0.5,
                                  0.5, 0.5, 0.5, 0.5,
                                  0.5, 0.5, 0.5, 0.5)))
    if shared.running:
        if shared.node_count >= shared.max_nodes:
            pyglet.graphics.draw(4, gl.GL_QUADS,
                                 ('v2f', (shared.window_width // 5 - 20, 24 - 10,
                                          shared.window_width // 5 - 20, 24 + 10,
                                          shared.window_width // 5, 24 + 10,
                                          shared.window_width // 5, 24 - 10)),
                                 ('c4f', (0.5, 0.25, 0.0, 0.5,
                                          0.5, 0.25, 0.0, 0.5,
                                          0.5, 0.25, 0.0, 0.5,
                                          0.5, 0.25, 0.0, 0.5)))
        else:
            pyglet.graphics.draw(4, gl.GL_QUADS,
                                 ('v2f', (shared.window_width // 5 - 20, 24 - 10,
                                          shared.window_width // 5 - 20, 24 + 10,
                                          shared.window_width // 5, 24 + 10,
                                          shared.window_width // 5, 24 - 10)),
                                 ('c4f', (0.0, 0.5, 0.0, 0.5,
                                          0.0, 0.5, 0.0, 0.5,
                                          0.0, 0.5, 0.0, 0.5,
                                          0.0, 0.5, 0.0, 0.5)))
    else:
        pyglet.graphics.draw(4, gl.GL_QUADS,
                             ('v2f', (shared.window_width // 5 - 20, 24 - 10,
                                      shared.window_width // 5 - 20, 24 + 10,
                                      shared.window_width // 5, 24 + 10,
                                      shared.window_width // 5, 24 - 10)),
                             ('c4f', (0.5, 0.0, 0.0, 0.5,
                                      0.5, 0.0, 0.0, 0.5,
                                      0.5, 0.0, 0.0, 0.5,
                                      0.5, 0.0, 0.0, 0.5)))
    shared.batch.draw()
    fps_display.draw()
    label.draw()
    node_label.draw()
    if path_cost is not None:
        path_cost.draw()


def setup(is_set=(False, False)):
    """
    Set up the environment.
    :param is_set: Root and goal nodes are set.
    :return: None
    """
    if shared.method is None:
        shared.method = method_cycle()
    shared.running = False
    root = None
    if shared.nodes:
        root = shared.nodes[0]
    shared.region = None
    shared.nodes.clear()
    shared.node_count = 0
    shared.max_nodes = shared.base_max
    del shared.batch
    shared.batch = pyglet.graphics.Batch()
    for obs in shared.obstacles:
        obs.add_to_default_batch()
    if not is_set[0]:
        root = None
        while root is None:
            root = random.random() * shared.window_width, random.random() * (shared.window_height - 50) + 50
            for obs in shared.obstacles:
                if obs.collides_with(root[0], root[1]):
                    root = None
                    break
        root = node.Node(root[0], root[1], None, "root")
    else:
        root = node.Node(root.x, root.y, None, "root")
    if not is_set[1]:
        goal = None
        while goal is None:
            goal = random.random() * shared.window_width, random.random() * (shared.window_height - 50) + 50
            for obs in shared.obstacles:
                if obs.collides_with(goal[0], goal[1]):
                    goal = None
                    break
        goal = node.Node(goal[0], goal[1], None, "goal")
    else:
        goal = node.Node(shared.goal.x, shared.goal.y, None, "goal")
    shared.nodes.append(root)
    shared.goal = goal
    shared.root_path = []
    shared.root_path_length = sys.maxsize


def main(set_nodes):
    """
    Main method calls pyglet app run to run the app.
    :param set_nodes:boolean tuple if goal/root nodes are set
    :return:
    """
    window = pyglet.window.Window(width=shared.window_width, height=shared.window_height)
    window.set_fullscreen(shared.fullscreen, shared.screen)
    window.set_location(shared.screen.x, shared.screen.height - shared.default_screen.height)
    window.set_caption("Rapidly-exploring Random Trees - RRT - Stopped")

    # noinspection PyUnusedLocal
    @window.event
    def on_key_press(symbol, modifiers):
        """
        event listeners from keyboard
        :param symbol: Key press
        :param modifiers: modifier keys pressed
        :return: None
        """
        if symbol == key.S:
            shared.running = not shared.running
            window.set_caption("Rapidly-exploring Random Trees - %s - %s" %
                               (shared.method.__name__,
                                'Running' if shared.running else 'Stopped'))
        if symbol == key.T:
            window.clear()
            setup()
            window.set_caption("Rapidly-exploring Random Trees - %s - %s" %
                               (shared.method.__name__,
                                'Running' if shared.running else 'Stopped'))
        if symbol == key.R:
            window.clear()
            setup((True, True))
            window.set_caption("Rapidly-exploring Random Trees - %s - %s" %
                               (shared.method.__name__,
                                'Running' if shared.running else 'Stopped'))
        if symbol == key.P:
            shared.method = method_cycle()
            setup((True, True))
            window.set_caption("Rapidly-exploring Random Trees - %s - %s" %
                               (shared.method.__name__,
                                'Running' if shared.running else 'Stopped'))
        if symbol == key.UP:
            shared.max_nodes *= 2

        if symbol == key.D:
            jsonify.json_dump()

    # noinspection PyUnusedLocal
    @window.event
    def on_mouse_press(x, y, button, modifiers):
        """
        Mousedown event creates new obstacles, and deletes existing
        :param x: x position of press
        :param y: y position
        :param button: Left or Right LEft creates right deletes
        :param modifiers:
        :return:
        """
        if button == mouse.LEFT:
            shared.obstacles.append(obstacle.Obstacle(x, y, 0, 0))
        if button == mouse.RIGHT:
            for obs in shared.obstacles:
                if obs.collides_with(x, y):
                    obs.delete()

    # noinspection PyUnusedLocal
    @window.event
    def on_mouse_release(x, y, button, modifiers):
        """
        Releasing the mouse finalises the creation of an obstacle
        :param x: release pos
        :param y: release pos
        :param button: button released
        :param modifiers:
        :return:
        """
        if button == mouse.LEFT:
            dx = x - shared.obstacles[-1].x
            dy = y - shared.obstacles[-1].y
            shared.obstacles[-1].x = min(x, shared.obstacles[-1].x)
            shared.obstacles[-1].y = min(y, shared.obstacles[-1].y)
            shared.obstacles[-1].width = abs(dx)
            shared.obstacles[-1].height = abs(dy)
            if shared.obstacles:
                for this_node in shared.nodes:
                    if shared.obstacles[-1].collides_with(this_node.x, this_node.y):
                        shared.obstacles[-1].delete()
                if shared.obstacles[-1].collides_with(shared.goal.x, shared.goal.y):
                    shared.obstacles[-1].delete()
                else:
                    shared.obstacles[-1].add_to_default_batch()

    window.clear()
    setup(set_nodes)
    pyglet.clock.schedule(update)
    gl.glClearColor(0.0, 0.0, 0.0, 1.0)
    pyglet.app.run()


if __name__ == "__main__":  # This happens if you run
    import argparse

    nodes_set = (False, False)
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--screensaver",
                        help="run with a very high number of nodes, and no stopping after each pathfinding",
                        action="store_true")
    parser.add_argument("-i", "--infile",
                        help="use this file to set the environment up")
    parser.add_argument("-f", "--fullscreen",
                        help="run fullscreen on last screen available", action="store_true")
    args = parser.parse_args()
    shared.continual = args.screensaver
    if shared.continual:
        shared.base_max = sys.maxsize
    shared.fullscreen = args.fullscreen
    if shared.fullscreen:
        shared.window_width, shared.window_height = shared.screen_width, shared.screen_height
        shared.x_domain = 0, shared.window_width
        shared.y_domain = 50, shared.window_height
        shared.x_range = shared.x_domain[1] - shared.x_domain[0]
        shared.y_range = shared.y_domain[1] - shared.y_domain[0]
    if args.infile:
        nodes_set = jsonify.parse_infile(args.infile)
    main(nodes_set)
