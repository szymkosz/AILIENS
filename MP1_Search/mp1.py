import sys

## Obtain maze text file from command line
try:
    fileName = sys.argv[1]
except:
    print("Must include maze text file name as input. For example:")
    print("$ python %s file.txt" % sys.argv[0])
    quit()

class Node:
    # Initializes value of the starting node
    startingNode = False
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

        # Updates the value of the starting node once found
        if value == 'P':
            Node.startingNode = self

    def __repr__(self):
        return "{0}".format(self.value)

    def __str__(self):
        return "({0}, {1}) {2}".format(self.x, self.y, self.value)

## Open and create matrix data structure
maze = []
with open(fileName, 'r') as file:
    h = 0
    for line in file:
        maze.append([ Node(h,w,line[w]) for w in range(len(line)) ])
        h+=1

def printMaze():
    for i in range(len(maze)):
        sys.stdout.write(' '.join(n.__repr__() for n in maze[i]))
    sys.stdout.write("\n")

def printAllNodes():
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            print(maze[i][j])

#printMaze()
#printAllNodes()
