## Node class holding data for each cell of maze
class Node:
    # Constructor
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.char = char
        self.parent = None
        self.visited = False

        # This variable stores the lowest path cost seen thus far from the
        # start Node to this Node, initialized to positive infinity.
        #
        # This variable is only for the A* algorithms in parts 1.1 and 1.2.
        self.cost = float("inf")

        # Stores the nodes of the pellets to allow nodes to be uniquely distinguished
        # by both remaining pellet configurations and Pacman's location.
        #
        # This variable is only for the A* algorithm in part 1.2.
        self.food = []

    # Specific-use node representation (Characters only)
    def __repr__(self):
        return "{0}".format(self.char)

    # String representation of node -> (x, y) char
    def __str__(self):
        return "({0}, {1}) {2}".format(self.x, self.y, self.char)
