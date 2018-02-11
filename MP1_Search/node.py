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
        #  start Node to this Node, initialized to positive infinity.
        self.cost = float("inf")

        # Only for 1.2
        self.food = []

    # Specific-use node representation (Characters only)
    def __repr__(self):
        return "{0}".format(self.char)

    # String representation of node -> (x, y) char
    def __str__(self):
        return "({0}, {1}) {2}".format(self.x, self.y, self.char)
