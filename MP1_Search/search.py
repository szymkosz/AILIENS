# Import all the necessary packages
from maze import Maze
from node import Node
import heapq

"""
-------------------------------------------------------------------------------
THIS SECTION IS FOR HELPER FUNCTIONS!
-------------------------------------------------------------------------------
"""

# Computes the Manhattan distance d from node1 to node2 as:
#
# m = abs(node1.x - node2.x) + abs(node1.y - node2.y)
#
# where abs() is the absolute value function.
def ManhattanDistance(node1, node2):
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)


# Adds a new node to the frontier within the greedy best-first search algorithm for MP 1.1
def GreedyBestFirstSearch_AddToFrontier(curNode, newNode, goalNode, counter, frontier):
    newNode.parent = curNode
    newHeuristic = ManhattanDistance(newNode, goalNode)
    heapq.heappush(frontier, (newHeuristic, counter, newNode))


# Adds a new node to the frontier within the A* algorithm for MP 1.1
def AStar_AddToFrontier(curNode, newNode, goalNode, counter, frontier):
    newNode.parent = curNode
    newNode.pathCost = curNode.pathCost + 1
    newHeuristic = ManhattanDistance(newNode, goalNode)
    heapq.heappush(frontier, (newNode.pathCost + newHeuristic, counter, newNode))


"""
-------------------------------------------------------------------------------
MP 1.1 STARTS HERE!

EACH PROBLEM INSTANCE AND SEARCH ALGORITHM MUST RETURN THE FOLLOWING:

1. The solution, displayed by putting a '.' in every maze square visited on the path.
2. The path cost of the solution, defined as the number of steps taken to get from
   the initial state to the goal state.
3. Number of nodes expanded by the search algorithm.
-------------------------------------------------------------------------------
"""

def DepthFirstSearch(maze):
    s = []
    start = maze.startingNode
    goal = maze.food_array[0]

    s.append(start)

    # Initialize a counter to count the number of nodes that get expanded
    expandedNodes = 0

    while len(s) > 0:
        current = s.pop(-1)

        if not current.visited:
            current.visited = True
            expandedNodes += 1

            adj = maze.getAdjacent(current)

            while len(adj) > 0:
                node = adj.pop()
                if not node.visited:
                    node.parent = current
                    s.append(node)

    current = goal
    totalMazeCost = 0
    while (current != start):
        totalMazeCost += 1
        current.char = '.'
        current = current.parent

    print("Path Cost: " + str(totalMazeCost))
    print("Expanded Nodes: " + str(expandedNodes))
    maze.printMaze()
    maze.writeMaze("dfs")


def BreadthFirstSearch(maze):
    q = []
    start = maze.startingNode
    goal = maze.food_array[0]

    q.append(start)

    # Initialize a counter to count the number of nodes that get expanded
    expandedNodes = 0

    while len(q) > 0:
        current = q.pop(0)

        if not current.visited:
            current.visited = True
            expandedNodes += 1

            adj = maze.getAdjacent(current)

            for node in adj:
                if not node.visited:
                    node.parent = current
                    q.append(node)

    current = goal
    totalMazeCost = 0
    while (current != start):
        totalMazeCost += 1
        current.char = '.'
        current = current.parent

    print("Path Cost: " + str(totalMazeCost))
    print("Expanded Nodes: " + str(expandedNodes))
    maze.printMaze()
    maze.writeMaze("bfs")


def GreedyBestFirstSearch(maze):
    # Initialize the frontier (represented as a priority queue),
    # the true path cost, and identify the start and goal Nodes
    frontier = []
    start = maze.startingNode
    goal = maze.food_array[0]

    # Add the start to the frontier
    startHeuristic = ManhattanDistance(start, goal)
    counter = 1
    heapq.heappush(frontier, (startHeuristic, counter, maze.startingNode))

    # Initialize a counter to count the number of nodes that get expanded
    expandedNodes = 0

    while len(frontier) > 0:
        # Remove node from frontier
        curNode = heapq.heappop(frontier)[2]

        # Expand this node only if it hasn't been expanded (visited) yet
        if not curNode.visited:
            curNode.visited = True
            expandedNodes += 1

            # If the expanded node is the goal,
            # end the search
            if curNode == goal:
                break

            neighbors = maze.getAdjacent(curNode)

            # Iterate through all the neighbors and add them to the frontier
            # if they haven't been visited
            for neighbor in neighbors:
                if not neighbor.visited:
                    counter += 1
                    GreedyBestFirstSearch_AddToFrontier(curNode, neighbor, goal, counter, frontier)

    current = goal
    totalMazeCost = 0
    while (current != start):
        totalMazeCost += 1
        current.char = '.'
        current = current.parent

    print("Path Cost: " + str(totalMazeCost))
    print("Expanded Nodes: " + str(expandedNodes))
    maze.printMaze()
    maze.writeMaze("greedy")

    """
    frontier = PQ()

    #add the startingNode to the frontier
    P = maze.startingNode
    P.parent = None
    P.cost = 0
    P.visited = True
    goal = maze.food_array[0]
    P_MH = ManhattanDistance(P, goal)
    # frontier.put(P.cost + P_MH, P)
    heapq.heappush(frontier, (P.cost + P_MH, P))

    #check all directions of neighbors and add them on the frontier
    while(frontier.qsize() > 0):
	# currNode = frontier.get()
	currNode = heapq.heappop(frontier)[1]

	if(currNode == goal):
		break

	for direction in range(0, 4):
		if(maze.canTravel(currNode, direction) and not currNode.visited):
			newNode = maze.getNode(currNode, direction)
			AStar_AddToFrontier(currNode, newNode, goal, frontier)
    """


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
def AStar(maze):
    # Initialize the frontier (represented as a priority queue),
    # the true path cost, and identify the start and goal Nodes
    frontier = []
    start = maze.startingNode
    goal = maze.food_array[0]
    trueCost = float("inf")

    # Mark the start with a cost of 0, compute its heuristic, initialize a counter
    # for breaking ties in the frontier, and add the start to the frontier
    start.pathCost = 0
    startHeuristic = ManhattanDistance(start, goal)
    counter = 1
    heapq.heappush(frontier, (start.pathCost + startHeuristic, counter, maze.startingNode))

    # Initialize a counter to count the number of nodes that get expanded
    expandedNodes = 0

    while len(frontier) > 0:
        # Remove node from frontier
        curNode = heapq.heappop(frontier)[2]
        curNodeHeuristic = ManhattanDistance(curNode, goal)

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

            neighbors = maze.getAdjacent(curNode)

            # Iterate through all the neighbors and add them to the frontier
            # if they haven't been visited
            for neighbor in neighbors:
                """
                if neighbor == goal:
                    goal.visited = False
                """
                if not neighbor.visited:
                    counter += 1
                    AStar_AddToFrontier(curNode, neighbor, goal, counter, frontier)

    current = goal
    totalMazeCost = 0
    while (current != start):
        totalMazeCost += 1
        current.char = '.'
        current = current.parent

    assert totalMazeCost == trueCost, "ERROR: True cost doesn't match final cost"

    print("Path Cost: " + str(totalMazeCost))
    print("Expanded Nodes: " + str(expandedNodes))
    maze.printMaze()
    maze.writeMaze("AStar")


"""
-------------------------------------------------------------------------------
MP 1.2 STARTS HERE!
-------------------------------------------------------------------------------
"""

# Computes the heuristic for MP 1.2.
def AStarMultiSearch_ComputeHeuristic(maze, curNode):
    curMinDistanceToPellet = min(ManhattanDistance(curNode, pellet) for pellet in maze.food_array)
    return maze.MSTCost + curMinDistanceToPellet


# Adds a new node to the frontier within the A* algorithm for MP 1.2
def AStarMultiSearch_AddToFrontier(curNode, newNode, counter, mazes, mazeIndex, frontier):
    """
    # Represents the Node to be added to the frontier
    addNode = None

    # If the Node to be added to the frontier has a food pellet or
    # it's food array is different from that of curNode, a new Node
    # must be created to properly represent the state Pacman would be in
    # if he moved into the position of newNode.
    if newNode.char == '.' or set(curNode.food) != set(newNode.food):
        addNode = Node(newNode.x, newNode.y, newNode.char)
        addNode.food = list(curNode.food)

        # If the Node to be added to the frontier has a food pellet,
        # the pellet must be removed from the Node's food array to properly represent
        # the pellets that would remain if Pacman stepped onto this pellet.
        if addNode.char == '.':
            isNotNewNode = lambda x: x is not newNode
            addNode.food = filter(isNotNewNode, addNode.food)
    else:
        addNode = newNode

    # If the Node to be added doesn't have a food pellet, the cost of the
    # MST of the remaining pellets doesn't have to be recomputed.
    if addNode.char != '.':
        addNode.MSTCost = curNode.MSTCost
    """

    newNode.parent = curNode
    newNode.pathCost = curNode.pathCost + 1
    newHeuristic = AStarMultiSearch_ComputeHeuristic(mazes[mazeIndex], newNode)
    heapq.heappush(frontier, (newNode.pathCost + newHeuristic,
                              counter, mazeIndex, newNode))


def AStarMultiSearch(maze):
    mazes = []
    mazes.append(maze)

    # Initialize the frontier (represented as a priority queue),
    # the true path cost, the start Node, the index of the maze in mazes
    # the start Node belongs to, and the goal state
    frontier = []
    startMazeIndex = 0
    start = mazes[startMazeIndex].startingNode
    goal = None
    trueCost = float("inf")

    # Mark the start with a cost of 0, compute its heuristic, initialize a counter
    # for breaking ties in the frontier, and add the start to the frontier
    start.pathCost = 0
    startHeuristic = AStarMultiSearch_ComputeHeuristic(mazes[startMazeIndex], start)
    counter = 1
    heapq.heappush(frontier, (start.pathCost + startHeuristic,
                              counter, startMazeIndex, start))

    # Initialize a counter to count the number of nodes that get expanded
    expandedNodes = 0

    while len(frontier) > 0:
        # Remove node from frontier
        tup = heapq.heappop(frontier)
        curNode = tup[3]
        mazeIndex = tup[2]
        curNodeHeuristic = AStarMultiSearch_ComputeHeuristic(mazes[mazeIndex], curNode)

        # Expand this node only if it hasn't been expanded (visited) yet
        # and its value of f(n) is less than the current discovered path
        # cost to the goal
        if not curNode.visited and (curNode.pathCost+curNodeHeuristic) < trueCost:
            curNode.visited = True
            expandedNodes += 1

            # If the expanded node is a goal state,
            # compute the total path cost it took to get there
            if len(curNode.food) == 0:
                pathCost = 0
                current = curNode

                while current != start:
                    pathCost += 1
                    current = current.parent

                # If the total cost to reach this goal state is better than
                # the best total cost discovered so far, set the optimal goal
                # state to this one and update the optimal total cost
                if pathCost < trueCost:
                    goal = curNode
                    trueCost = pathCost

            neighbors = mazes[mazeIndex].getAdjacent(curNode)

            # Iterate through all the neighbors and add them to the frontier
            # if they haven't been visited
            for neighbor in neighbors:
                """
                if neighbor == goal:
                    goal.visited = False
                """
                if not neighbor.visited:
                    counter += 1

                    if neighbor.char == '.':
                        newMazeIndex = len(mazes)
                        mazes.append(Maze(origMaze=mazes[mazeIndex], remove_pellet=neighbor))
                        newNode = mazes[newMazeIndex].maze[neighbor.y][neighbor.x]
                        AStarMultiSearch_AddToFrontier(curNode, newNode, counter,
                                                       mazes, newMazeIndex, frontier)
                    else:
                        AStarMultiSearch_AddToFrontier(curNode, neighbor, counter,
                                                       mazes, mazeIndex, frontier)

    assert goal is not None, "ERROR: No goal state found"

    current = goal
    totalMazeCost = 0
    while (current != start):
        totalMazeCost += 1
        current.char = '.'
        current = current.parent

    assert totalMazeCost == trueCost, "ERROR: True cost doesn't match final cost"

    print("Path Cost: " + str(totalMazeCost))
    print("Expanded Nodes: " + str(expandedNodes))
    maze.printMaze()
    maze.writeMaze()
