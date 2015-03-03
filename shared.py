__author__ = 'murraytannock'
import sys

import pyglet

STEP_SIZE = 20
neighbourhood_size = STEP_SIZE
window_width = 800
window_height = int(10/16 * window_width)
running = False
batch = pyglet.graphics.Batch()
node_count = 0
max_nodes = 1000
goal = None
root_path = []
root_path_length = sys.maxsize
nodes = []
obstacles = []
xdomain = 0, window_width
ydomain = 50, window_height
method = None
fullscreen = True
region = None