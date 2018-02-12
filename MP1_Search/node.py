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
        self.pathCost = float("inf")

        #self.mazeIndex = mazeIndex

        # Stores the nodes of the pellets to allow nodes to be uniquely distinguished
        # by both remaining pellet configurations and Pacman's location.
        #
        # This variable is only for the A* algorithm in part 1.2.
        #self.food = []

        # This instance variable stores the cost of the Minimum Spanning Tree (MST)
        # formed by the remaining pellets represented by this Node.
        #self.MSTCost = float("inf")

    # Specific-use node representation (Characters only)
    def __repr__(self):
        return "{0}".format(self.char)

    # String representation of node -> (x, y) char
    def __str__(self):
        return "({0}, {1}) {2}".format(self.x, self.y, self.char)

"""
nodeA = Node(1, 2, ' ')
nodeB = Node(2, 3, ' ')

pelletA = Node(5, 4, '.')
pelletB = Node(2, 6, '.')
pelletC = Node(5, 1, '.')

nodeA.food.append(pelletA)
#nodeA.food.append(pelletB)
nodeA.food.append(pelletC)

nodeB.food.append(pelletB)
nodeB.food.append(pelletA)

print(nodeA.food)
print(nodeB.food)

if set(nodeA.food) == set(nodeB.food):
    print("The food arrays are equal.")
else:
    print("The food arrays are NOT equal.")
"""
