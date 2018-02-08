import sys

## Obtain maze text file from command line
try:
    fileName = sys.argv[1]
except:
    print("Must include maze text file name as input. For example:")
    print(" $ python %s file.txt" % sys.argv[0])
    quit()


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
