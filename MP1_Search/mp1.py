import sys

## Obtain maze text file from command line
try:
    fileName = sys.argv[1]
except:
    print("Must include maze text file name as input. For example:")
    print(" $ python %s file.txt" % sys.argv[0])
    quit()

## Node class holding data for each cell array
class Node:
    # Initializes value of the starting node
    startingNode = False
    food_array = []
    maze = []

    # Constructor
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

        # Updates the value of the starting node once found
        if value == 'P':
            Node.startingNode = self
        if value == '.':
            Node.food_array.append((self,1e100))

    # Specific-use node representation (Characters only)
    def __repr__(self):
        return "{0}".format(self.value)

    # String representation of node -> (x, y) char
    def __str__(self):
        return "({0}, {1}) {2}".format(self.x, self.y, self.value)

    # Returns boolean whether or not can move in the desired direction
    def canTravel(self, dir):
        if ((self.x == 0 and dir == LEFT) or \
        (self.y == 0 and dir == UP) or \
        (self.x == len(Node.maze[0]) - 1 and dir == RIGHT) or \
        (self.y == len(Node.maze) - 1 and dir == DOWN)):
            return False

        if dir == RIGHT:
            return not Node.maze[self.y][self.x+1].value == "%"
        if dir == DOWN:
            return not Node.maze[self.y+1][self.x].value == "%"
        if dir == LEFT:
            return not Node.maze[self.y][self.x-1].value == "%"
        if dir == UP:
            return not Node.maze[self.y-1][self.x].value == "%"


## Open file and create matrix data structure
def parseMazeFile():
    Node.maze = []
    Node.food_array = []
    with open(fileName, 'r') as file:
        h = 0

        ## Unfortunately, the way the file is read and parsed, the coordinates
        ## are backwards, so the array should be indexed with y first, then x
        ## i.e. Node.maze[y][x]
        for line in file:
            Node.maze.append([ Node(w,h,line[w]) for w in range(len(line)) ])
            h+=1

## Prints the maze to standard output
def printMaze():
    maze = Node.maze
    for i in range(len(maze)):
        #sys.stdout.write("%3d  " % i)  # Adds row numbers
        sys.stdout.write(' '.join(n.__repr__() for n in maze[i]))
    sys.stdout.write("\n")

## Prints each node of the maze as a string -> (x, y) char
def printAllNodes():
    maze = Node.maze
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            print(maze[i][j])

## Write the current state of the maze nodes into a txt file
def writeMaze():
    idx = fileName.find('.txt')
    solutionFileName = fileName[0:idx] + "_sol" + fileName[idx:]
    f = open(solutionFileName, 'w')
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            f.write(maze[i][j].value)
    f.close()

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

# parseMazeFile()
# Node.maze[3][1].value = '.'
# print(Node.maze[3][1])
# Node.maze[4][1].value = '.'
#
# printMaze()
# writeMaze()
# printAllNodes()
