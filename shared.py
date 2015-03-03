__author__ = 'murraytannock'
import sys

import pyglet

STEP_SIZE = 20
neighbourhood_size = STEP_SIZE
screen = None
default_screen = None
window_width = 800
window_height = 600
running = False
batch = pyglet.graphics.Batch()
node_count = 0
base_max = 1000
max_nodes = 1000
goal = None
root_path = []
root_path_length = sys.maxsize
nodes = []
obstacles = []
xdomain = 0, window_width
ydomain = 50, window_height
xrange = xdomain[1] - xdomain[0]
yrange = ydomain[1] - ydomain[0]
method = None
fullscreen = False
region = None
continual = True
outfile_base = "levels/level"
outfile_ext = ".json"


if continual:
    base_max = 1000000000000000000000

if fullscreen:
    screen = pyglet.window.get_platform().get_default_display().get_screens()[-1]
    default_screen = pyglet.window.get_platform().get_default_display().get_screens()[0]
    window_width = screen.width
    window_height = screen.height