from node import Node
import sys
import heapq
import helper
import copy

class Maze:
    def __init__(self, fileName=None, origMaze=None, remove_pellet=None):
        self.fileName = fileName
        self.maze = []
        self.food_array = []
        self.startingNode = None
        self.paths = {}

        if fileName is not None:
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
        """
        elif origMaze is not None:
            for i in range(len(origMaze.maze)):
                row = []
                for j in range(len(origMaze.maze[i])):
                    origNode = origMaze.maze[i][j]
                    newNode = Node(origNode.x, origNode.y, origNode.char)
                    row.append(newNode)
                    if newNode.char == '.':
                        self.food_array.append(newNode)
                self.maze.append(row)

        if remove_pellet is not None:
            isNotPellet = lambda x: (x.x != remove_pellet.x or x.y != remove_pellet.y)
            self.food_array = list(filter(isNotPellet, self.food_array))
            print(len(self.food_array))
            print(self.food_array)
            self.startingNode = self.maze[remove_pellet.y][remove_pellet.x]
            self.startingNode.char = 'P'
            print("start: " + str(self.startingNode))
        """
        for i in range(len(self.food_array)):
            pelletA = self.food_array[i]
            pelletACoordinates = (pelletA.x, pelletA.y)

            for j in range(i+1, len(self.food_array)):
                pelletB = self.food_array[j]
                pelletBCoorinates = (pelletB.x, pelletB.y)

                pairwisePath = self.PairwiseAStar(pelletACoordinates, pelletBCoorinates)
                self.paths[(pelletACoordinates, pelletBCoorinates)] = pairwisePath

        startCoordinates = (self.startingNode.x, self.startingNode.y)
        for i in range(len(self.food_array)):
            pellet = self.food_array[i]
            pelletCoordinates = (pellet.x, pellet.y)

            pairwisePath = self.PairwiseAStar(startCoordinates, pelletCoordinates)
            self.paths[(startCoordinates, pelletCoordinates)] = pairwisePath

        #print(self.paths)



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
    def writeMaze(self, algorithm):
        maze = self.maze
        idx = self.fileName.find('.txt')
        solutionFileName = self.fileName[0:idx] + "_" + algorithm + "_sol" + self.fileName[idx:]
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

    # Searches for the food pellet using the A* algorithm.
    # In A*, unexpanded nodes on the frontier are sorted with a min Priority Queue.
    # The priority f(n) of a node n is computed as:
    #
    # f(n) = g(n) + h(n) , where
    #
    # g(n) = cost so far to reach n (path cost)
    # h(n) = estimated cost from n to goal (heuristic)
    #
    # The heuristic h(n) is computed as the Manhattan distance from n to the goal.
    def PairwiseAStar(self, startCoordinates, goalCoordinates):
        # Initialize the frontier (represented as a priority queue)
        # and the true path cost
        frontier = []
        start = self.maze[startCoordinates[1]][startCoordinates[0]]
        goal = self.maze[goalCoordinates[1]][goalCoordinates[0]]
        trueCost = float("inf")

        # Mark the start with a cost of 0, compute its heuristic, initialize a counter
        # for breaking ties in the frontier, and add the start to the frontier
        start.pathCost = 0
        startHeuristic = helper.ManhattanDistance(start, goal)
        counter = 1
        heapq.heappush(frontier, (start.pathCost + startHeuristic, counter, self.maze[startCoordinates[1]][startCoordinates[0]]))

        # Initialize a counter to count the number of nodes that get expanded
        expandedNodes = 0

        while len(frontier) > 0:
            # Remove node from frontier
            curNode = heapq.heappop(frontier)[2]
            curNodeHeuristic = helper.ManhattanDistance(curNode, goal)

            # Expand this node only if it hasn't been expanded (visited) yet
            # and its value of f(n) is less than the current discovered path
            # cost to the goal
            if not curNode.visited and (curNode.pathCost+curNodeHeuristic) < trueCost:
                curNode.visited = True
                expandedNodes += 1

                # If the expanded node is the goal,
                # compute the total path cost
                if curNode == goal:
                    pathCost = 0
                    current = goal

                    while current != start:
                        pathCost += 1
                        current = current.parent

                    if pathCost < trueCost:
                        trueCost = pathCost

                neighbors = self.getAdjacent(curNode)

                # Iterate through all the neighbors and add them to the frontier
                # if they haven't been visited
                for neighbor in neighbors:
                    """
                    if neighbor == goal:
                        goal.visited = False
                    """
                    if not neighbor.visited:
                        counter += 1
                        helper.AStar_AddToFrontier(curNode, neighbor, goal, counter, frontier)

        current = goal
        totalMazeCost = 0
        path = []
        while (current != start):
            totalMazeCost += 1
            path.append((current.x, current.y))
            current = current.parent

        assert totalMazeCost == trueCost, "ERROR: True cost doesn't match final cost"

        path.append((start.x, start.y))
        self.reset()

        return (totalMazeCost, path)


    # Reset all the nodes in the maze to prepare it for another pairwise A* search
    def reset(self):
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                self.maze[i][j].parent = None
                self.maze[i][j].visited = False
                self.maze[i][j].pathCost = float("inf")


# Consider the complete graph where the nodes are all the pellets remaining
# and the edges are all the possible pairwise distances between each of the
# remaining pellets.
#
# This function takes in a list called 'edges' representing the edges of this graph
# and returns the edges that belong to the minimum spanning tree (MST).
# The 'edges' parameter is of the form:
#
# [(d1, 1, (n1A, n1B)), (d2, 2, (n2A, n2B)) ... (di, i, (niA, niB)) ... (dm, m, (nmA, nmB))]
#
# where:
#
# niA, niB = the nodes representing the endpoints of the edge
# di = the weight of the ith edge (the Manhattan Distance between nodes niA and niB)
#
# The purpose of the second entry of each tuple in the input is to break ties in
# this function's priority queue when two edges have the same Manhattan Distance.
def BuildMST(edges, numVertices):
    # sort the edges
    edges.sort(key = lambda tup: tup[0])

    #breaking ties in sort
    for edge_index in range(len(edges)-1):
        if (edges[edge_index][0] == edges[edge_index+1][0]) and (edges[edge_index][1] > edges[edge_index+1][1]):
            edges[edge_index], edges[edge_index+1] = edges[edge_index+1], edges[edge_index]


    edge_index = 0

    #build mst_dict
    edge_list = []
    for edge_index in range(len(edges)):
        edge_list.append(edges[edge_index][2])


    mst_dict = dict()
    mst_len = 0
    edge_index = 0

    while(edge_index < len(edge_list)) and (mst_len < numVertices):
        new_edge = edge_list[edge_index]

        mst_dict_copy = copy.deepcopy(mst_dict)
        if(helper.formsCycle(mst_dict_copy, new_edge) == False):
            mst_dict = helper.mst_dict_append(mst_dict, new_edge)
            mst_len += 1

        edge_index += 1

    #remove the back-edges from the list of edges
    edge_index = 0
    mst_edges = []
    while edge_index < len(edges):
        x,y = edges[edge_index][2][0], edges[edge_index][2][1]
        if (x in mst_dict) and (y in mst_dict[x]):
            mst_edges.append(edges[edge_index])

        edge_index += 1

    return mst_edges


def computeMSTCost(maze, remainingPelletCoordinates):
    # Initialize the input list to BuildMST and counters of the numbers
    # of edges and vertices
    if len(remainingPelletCoordinates) == 0:
        return 0

    edges = []
    numEdges = 0
    numVertices = len(remainingPelletCoordinates)

    # Build the input list to BuildMST
    for i in range(numVertices):
        vertexA = remainingPelletCoordinates[i]

        for j in range(i+1, numVertices):
            vertexB = remainingPelletCoordinates[j]
            numEdges += 1

            indexA = (vertexA, vertexB)
            indexB = (vertexB, vertexA)

            EdgeWeight = 0
            if indexA in maze.paths:
                EdgeWeight = maze.paths[indexA][0]
            else:
                assert indexB in maze.paths, "ERROR: Missing pairwise distance"
                EdgeWeight = maze.paths[indexB][0]

            edges.append( (EdgeWeight, numEdges, (vertexA, vertexB)) )

    # Compute the MST cost and return it
    curMST = BuildMST(edges, numVertices)
    return sum(edge[0] for edge in curMST)
