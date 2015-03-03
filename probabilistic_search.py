__author__ = 'Murray Tannock'
import shared
import node


def goal_path_resolve(new_node):
    if new_node.dist_to((shared.goal.x, shared.goal.y)) < shared.STEP_SIZE:
        # we can step to the goal node
        new_root_path_cost = new_node.cost + new_node.dist_to((shared.goal.x, shared.goal.y))
        if new_root_path_cost < shared.root_path_length:
            shared.root_path_length = new_root_path_cost
            shared.goal.node.delete()
            shared.goal = node.Node(shared.goal.x, shared.goal.y, new_node, "goal")
            shared.nodes.append(shared.goal)
            # backtrace to the root
            for current_node in shared.root_path:
                current_node.deroot_path_color()
            shared.root_path = []
            shared.root_path.append(shared.goal)
            current_node = shared.goal
            while current_node.parent is not None:
                current_node.root_path_color()
                current_node = current_node.parent
                shared.root_path.append(current_node)
            if not shared.continual:
                shared.running = False
            return True
        return False
