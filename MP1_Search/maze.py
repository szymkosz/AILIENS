from node import Node
import sys

class Maze:
    def __init__(self, fileName=None, origMaze=None, remove_pellet=None, startingNode=None):
        self.fileName = fileName
        self.maze = []
        self.food_array = []
        self.startingNode = None

        if filename != None:
            ## Open file and create matrix data structure
            with open(fileName, 'r') as file:
                h = 0
                ## Unfortunately, the way the file is read and parsed, the coordinates
                ##  are backwards, so the array should be indexed with y first, then x
                ##  i.e. maze[y][x]
                for line in file:
                    # self.maze.append([ Node(w,h,line[w]) for w in range(len(line)) ])
                    row = []
                    for w in range(len(line)):
                        row.append(Node(w,h,line[w]))
                        if line[w] == 'P':
                            self.startingNode = row[w]
                        if line[w] == '.':
                            self.food_array.append(row[w])
                    self.maze.append(row)
                    h+=1

        elif origMaze != None:
            for i in range(len(origMaze.maze)):
                row = []
                for j in range(len(origMaze.maze[i])):
                    origNode = origMaze.maze[i][j]
                    newNode = Node(origNode.x, origNode.y, origNode.char)
                    row.append(newNode)
                    if newNode.char == 'P':
                        self.startingNode = newNode
                    if newNode.char == '.':
                        self.food_array.append(newNode)
                self.maze.append(row)

        if remove_pellet != None:
            isNotPellet = lambda x: x is not remove_pellet
            self.food_array = filter(isNotPellet, self.food_array)

        if startingNode != None:
            self.startingNode = startingNode

        self.MSTCost = computeMSTCost(self)
        """
        # Initialize the food list for every node in the maze
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                self.maze[i][j].food = list(self.food_array)
        """

    ## Overloaded operator []
    def __getitem__(self, index):
        return self.maze[index]

    ## Returns maze height
    def height(self):
        return len(self.maze)

    ## Returns maze width
    def width(self):
        return len(self[0])

    ## Prints the maze to standard output
    def printMaze(self):
        maze = self.maze
        for i in range(len(maze)):
            sys.stdout.write(' '.join(n.__repr__() for n in maze[i]))
        sys.stdout.write("\n")

    ## Prints each node of the maze as a string -> (x, y) char
    def printAllNodes(self):
        maze = self.maze
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                print(maze[i][j])

    ## Write the current state of the maze nodes into a txt file
    def writeMaze(self):
        maze = self.maze
        idx = self.fileName.find('.txt')
        solutionFileName = self.fileName[0:idx] + "_sol" + self.fileName[idx:]
        f = open(solutionFileName, 'w')
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                f.write(maze[i][j].char)
        f.close()

    ## Returns boolean whether or not can move in the desired direction
    def canTravel(self, node, dir):
        RIGHT = 0
        DOWN = 1
        LEFT = 2
        UP = 3

        if node.char == '%':
            raise ValueError("Invalid node passed as parameter. Must be a non-wall node.")

        if ((node.x == 0 and dir == LEFT) or \
        (node.y == 0 and dir == UP) or \
        (node.x == len(self.maze[0]) - 1 and dir == RIGHT) or \
        (node.y == len(self.maze) - 1 and dir == DOWN)):
            return False

        if dir == RIGHT:
            return not self.maze[node.y][node.x+1].char == "%"
        elif dir == DOWN:
            return not self.maze[node.y+1][node.x].char == "%"
        elif dir == LEFT:
            return not self.maze[node.y][node.x-1].char == "%"
        elif dir == UP:
            return not self.maze[node.y-1][node.x].char == "%"
        else:
            raise ValueError("Invalid direction parameter(s) passed into canTravel()")

    ## Returns the Node in the desired direction
    def getNode(self, node, dir):
        RIGHT = 0
        DOWN = 1
        LEFT = 2
        UP = 3

        if self.canTravel(node, dir):
            if dir == RIGHT:
                return self[node.y][node.x+1]
            elif dir == DOWN:
                return self[node.y+1][node.x]
            elif dir == LEFT:
                return self.maze[node.y][node.x-1]
            elif dir == UP:
                return self.maze[node.y-1][node.x]

    # Returns a list of adjacent nodes for which canTravel() = True.
    # Returns an empty list otherwise.
    def getAdjacent(self, node):
        RIGHT = 0
        DOWN = 1
        LEFT = 2
        UP = 3

        adj = []
        if self.canTravel(node, RIGHT):
            adj.append(self.getNode(node, RIGHT))
        if self.canTravel(node, DOWN):
            adj.append(self.getNode(node, DOWN))
        if self.canTravel(node, LEFT):
            adj.append(self.getNode(node, LEFT))
        if self.canTravel(node, UP):
            adj.append(self.getNode(node, UP))

        return adj

def computeMSTCost(maze):
    # Initialize the input list to BuildMST and counters of the numbers
    # of edges and vertices
    edges = []
    numEdges = 0
    numVertices = len(maze.food_array)

    # Build the input list to BuildMST
    for i in range(numVertices):
        vertexA = maze.food_array[i]

        for j in range(i+1, numVertices):
            vertexB = maze.food_array[j]
            numEdges += 1

            edges.append( (ManhattanDistance(vertexA, vertexB), numEdges, (vertexA, vertexB)) )

    # Compute the MST cost and return it
    curMST = BuildMST(edges, numVertices)
    return sum(edge[0] for edge in curMST)
