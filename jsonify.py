__author__ = 'murraytannock'

import shared
import json
import sys
import os

import obstacle
import node


def json_dump():
    my_dict = {"nodes": {
        "1": {
            "x": shared.nodes[0].x/shared.xrange,
            "y": (shared.nodes[0].y-shared.ydomain[0])/shared.yrange,
            "type": shared.nodes[0].type
        },
        "2": {
            "x": shared.goal.x/shared.xrange,
            "y": (shared.goal.y-shared.ydomain[0])/shared.yrange,
            "type": shared.goal.type
        }
    }, "obstacles": {}}

    for i, obs in enumerate(shared.obstacles):
        my_dict["obstacles"][str(i)] = {
            "x": obs.x/shared.xrange,
            "y": (obs.y-shared.ydomain[0])/shared.yrange,
            "width": obs.width/shared.xrange,
            "height": obs.height/shared.yrange
        }
    i = 0
    outfile = shared.outfile_base+str(i)+shared.outfile_ext
    while os.path.exists(outfile):
        i += 1
        outfile = shared.outfile_base+str(i)+shared.outfile_ext
    with open(outfile, "w") as r:
        json.dump(my_dict, r)


def parse_infile(infile):
    import os

    root_set = False
    goal_set = False

    if not os.path.exists(infile):
        print("Error: Infile {} does not exist.".format(infile), file=sys.stderr)
        exit(1)
    if not os.path.splitext(infile)[-1] == ".json":
        print("Error: Infile {} does not have correct extension.".format(infile), file=sys.stderr)
        exit(1)
    with open(infile) as json_file:
        json_obj = json.load(json_file)
        if 'obstacles' in json_obj:
            obstacles = json_obj["obstacles"]
            for obs in obstacles:
                print(obstacles[obs])
                this_obstacle = obstacles[obs]
                x = this_obstacle["x"]*shared.xrange
                y = (this_obstacle["y"]*shared.yrange)+shared.ydomain[0]
                width = this_obstacle["width"]*shared.xrange
                height = this_obstacle["height"]*shared.yrange
                shared.obstacles.append(obstacle.Obstacle(x, y, width, height))
        if 'nodes' in json_obj:
            nodes = json_obj["nodes"]
            for my_node in nodes:
                this_node = nodes[my_node]
                if this_node["type"] == "root":
                    x = this_node["x"]*shared.xrange
                    y = (this_node["y"]*shared.yrange)+shared.ydomain[0]
                    for obs in shared.obstacles:
                        if obs.collides_with(x, y):
                            print("Error: Specified root node collides with an obstacle.".format(infile), file=sys.stderr)
                            exit(1)
                    shared.nodes.append(node.Node(x, y, None, "root"))
                    root_set = True

                if this_node["type"] == "goal":
                    x = this_node["x"]*shared.xrange
                    y = (this_node["y"]*shared.yrange)+shared.ydomain[0]
                    for obs in shared.obstacles:
                        if obs.collides_with(x, y):
                            print("Error: Specified root node collides with an obstacle.".format(infile), file=sys.stderr)
                            exit(1)
                    shared.goal = node.Node(x, y, None, "goal")
                    goal_set = True
    return root_set, goal_set