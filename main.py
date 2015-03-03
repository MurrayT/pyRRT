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
    return next(meth_cycle)


def update(dt):
    pathcost = None
    if shared.running:
        if shared.node_count < shared.max_nodes:
            shared.method()
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glLoadIdentity()
    if shared.root_path_length != sys.maxsize:
        pathcost = pyglet.text.Label("Path Cost: %6.2f" % shared.root_path_length,
                                     font_size=18,
                                     x=shared.window_width//3, y=24,
                                     anchor_x='center', anchor_y='center',
                                     color=(128, 128, 128, 128))
    label = pyglet.text.Label(shared.method.__name__,
                              font_size=36,
                              x=shared.window_width-10, y=24,
                              anchor_x='right', anchor_y='center',
                              color=(128, 128, 128, 128))
    separator = pyglet.graphics.draw(4, gl.GL_QUADS,
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
            indicator = pyglet.graphics.draw(4, gl.GL_QUADS,
                                             ('v2f', (shared.window_width//5-20, 24 - 10,
                                                      shared.window_width//5-20, 24 + 10,
                                                      shared.window_width//5, 24 + 10,
                                                      shared.window_width//5, 24 - 10)),
                                             ('c4f', (0.5, 0.25, 0.0, 0.5,
                                                      0.5, 0.25, 0.0, 0.5,
                                                      0.5, 0.25, 0.0, 0.5,
                                                      0.5, 0.25, 0.0, 0.5)))
        else:
            indicator = pyglet.graphics.draw(4, gl.GL_QUADS,
                                             ('v2f', (shared.window_width//5-20, 24 - 10,
                                                      shared.window_width//5-20, 24 + 10,
                                                      shared.window_width//5, 24 + 10,
                                                      shared.window_width//5, 24 - 10)),
                                             ('c4f', (0.0, 0.5, 0.0, 0.5,
                                                      0.0, 0.5, 0.0, 0.5,
                                                      0.0, 0.5, 0.0, 0.5,
                                                      0.0, 0.5, 0.0, 0.5)))
    else:
        indicator = pyglet.graphics.draw(4, gl.GL_QUADS,
                                         ('v2f', (shared.window_width//5-20, 24 - 10,
                                                  shared.window_width//5-20, 24 + 10,
                                                  shared.window_width//5, 24 + 10,
                                                  shared.window_width//5, 24 - 10)),
                                         ('c4f', (0.5, 0.0, 0.0, 0.5,
                                                  0.5, 0.0, 0.0, 0.5,
                                                  0.5, 0.0, 0.0, 0.5,
                                                  0.5, 0.0, 0.0, 0.5)))
    shared.batch.draw()
    fps_display.draw()
    label.draw()
    if pathcost is not None:
        pathcost.draw()


def setup(is_set=(False, False)):
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
            root = random.random()*shared.window_width, random.random()*(shared.window_height-50)+50
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
            goal = random.random()*shared.window_width, random.random()*(shared.window_height-50)+50
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
    window = pyglet.window.Window(width=shared.window_width, height=shared.window_height)
    if shared.fullscreen:
        window.set_fullscreen(True, shared.screen)
        window.set_location(shared.screen.x, shared.screen.height-shared.default_screen.height)
    window.set_caption("Rapidly Expanding Random Trees - RRT - Stopped")

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == key.S:
            shared.running = not shared.running
            window.set_caption("Rapidly Expanding Random Trees - %s - %s" % (shared.method.__name__,
                                                                             'Running' if shared.running else 'Stopped'))
        if symbol == key.R:
            window.clear()
            setup()
            window.set_caption("Rapidly Expanding Random Trees - %s - %s" % (shared.method.__name__,
                                                                             'Running' if shared.running else 'Stopped'))
        if symbol == key.T:
            window.clear()
            setup((True, True))
            window.set_caption("Rapidly Expanding Random Trees - %s - %s" % (shared.method.__name__,
                                                                             'Running' if shared.running else 'Stopped'))
        if symbol == key.P:
            shared.method = method_cycle()
            setup((True, True))
            window.set_caption("Rapidly Expanding Random Trees - %s - %s" % (shared.method.__name__,
                                                                             'Running' if shared.running else 'Stopped'))
        if symbol == key.UP:
            shared.max_nodes *= 2

        if symbol == key.D:
            jsonify.json_dump()

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        if button == mouse.LEFT:
            shared.obstacles.append(obstacle.Obstacle(x, y, 0, 0))
        if button == mouse.RIGHT:
            for obs in shared.obstacles:
                if obs.collides_with(x, y):
                    obs.delete()

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        if button == mouse.LEFT:
            dx = x - shared.obstacles[-1].x
            dy = y - shared.obstacles[-1].y
            shared.obstacles[-1].x = min(x, shared.obstacles[-1].x)
            shared.obstacles[-1].y = min(y, shared.obstacles[-1].y)
            shared.obstacles[-1].width = abs(dx)
            shared.obstacles[-1].height = abs(dy)
            if shared.obstacles:
                for node in shared.nodes:
                    if shared.obstacles[-1].collides_with(node.x, node.y):
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


if __name__ == "__main__":
    import argparse
    nodes_set = (False, False)
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--screensaver",
                        help="run with a very high number of nodes, and no stopping after each pathfinding",
                        action="store_true")
    parser.add_argument("-f", "--infile",
                        help="use this file to set the environment up")
    args = parser.parse_args()
    shared.continual = args.screensaver
    if args.infile:
        nodes_set = jsonify.parse_infile(args.infile)
    print(nodes_set)
    main(nodes_set)
