__author__ = 'Murray Tannock'

import json
import sys
import os

import shared
import obstacle
import node


def json_dump():
    """
    Dumps JSON description of a level to a file. In future may make this dynamic through cl arguments
    :return: None
    """
    my_dict = {"nodes": {
        "1": {
            "x": shared.nodes[0].x / shared.x_range,
            "y": (shared.nodes[0].y - shared.y_domain[0]) / shared.y_range,
            "type": shared.nodes[0].type
        },
        "2": {
            "x": shared.goal.x / shared.x_range,
            "y": (shared.goal.y - shared.y_domain[0]) / shared.y_range,
            "type": shared.goal.type
        }
    }, "obstacles": {}}

    for i, obs in enumerate(shared.obstacles):
        my_dict["obstacles"][str(i)] = {
            "x": obs.x / shared.x_range,
            "y": (obs.y - shared.y_domain[0]) / shared.y_range,
            "width": obs.width / shared.x_range,
            "height": obs.height / shared.y_range
        }
    i = 0
    outfile = shared.outfile_base + str(i) + shared.outfile_ext
    while os.path.exists(outfile):
        i += 1
        outfile = shared.outfile_base + str(i) + shared.outfile_ext
    with open(outfile, "w") as r:
        json.dump(my_dict, r)


def parse_infile(infile):
    """
    Parses a JSON file into a level
    :param infile: filename to read from
    :return: Tuple indicating whether root node and goal node have been set.
    """
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
                this_obstacle = obstacles[obs]
                x = this_obstacle["x"] * shared.x_range
                y = (this_obstacle["y"] * shared.y_range) + shared.y_domain[0]
                width = this_obstacle["width"] * shared.x_range
                height = this_obstacle["height"] * shared.y_range
                shared.obstacles.append(obstacle.Obstacle(x, y, width, height))
        if 'nodes' in json_obj:
            nodes = json_obj["nodes"]
            for my_node in nodes:
                this_node = nodes[my_node]
                if this_node["type"] == "root":
                    x = this_node["x"] * shared.x_range
                    y = (this_node["y"] * shared.y_range) + shared.y_domain[0]
                    for obs in shared.obstacles:
                        if obs.collides_with(x, y):
                            print("Error: Specified root node collides with an obstacle.".format(infile),
                                  file=sys.stderr)
                            exit(1)
                    shared.nodes.append(node.Node(x, y, None, "root"))
                    root_set = True

                if this_node["type"] == "goal":
                    x = this_node["x"] * shared.x_range
                    y = (this_node["y"] * shared.y_range) + shared.y_domain[0]
                    for obs in shared.obstacles:
                        if obs.collides_with(x, y):
                            print("Error: Specified root node collides with an obstacle.".format(infile),
                                  file=sys.stderr)
                            exit(1)
                    shared.goal = node.Node(x, y, None, "goal")
                    goal_set = True
    return root_set, goal_set