## Node class holding data for each cell array
class Node:
    # Initializes char of the starting node
    startingNode = False
    food_array = []
    maze = []

    # Constructor
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.char = char
        self.parent = ()

        # Updates the char of the starting node once found
        if char == 'P':
            Node.startingNode = self
        if char == '.':
            Node.food_array.append((self,1e100))

    # Specific-use node representation (Characters only)
    def __repr__(self):
        return "{0}".format(self.char)

    # String representation of node -> (x, y) char
    def __str__(self):
        return "({0}, {1}) {2}".format(self.x, self.y, self.char)

    # Returns boolean whether or not can move in the desired direction
    def canTravel(self, dir):
        if ((self.x == 0 and dir == LEFT) or \
        (self.y == 0 and dir == UP) or \
        (self.x == len(Node.maze[0]) - 1 and dir == RIGHT) or \
        (self.y == len(Node.maze) - 1 and dir == DOWN)):
            return False

        if dir == RIGHT:
            return not Node.maze[self.y][self.x+1].char == "%"
        if dir == DOWN:
            return not Node.maze[self.y+1][self.x].char == "%"
        if dir == LEFT:
            return not Node.maze[self.y][self.x-1].char == "%"
        if dir == UP:
            return not Node.maze[self.y-1][self.x].char == "%"
