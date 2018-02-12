# Import all the necessary packages
from maze import Maze
from node import Node
import heapq
import helper

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

            ## If goal state is reached, stop algorithm
            if current == goal:
                break

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

            ## If the expanded node is the goal, end the search
            if current == goal:
                break

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
    startHeuristic = helper.ManhattanDistance(start, goal)
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
                    helper.GreedyBestFirstSearch_AddToFrontier(curNode, neighbor, goal, counter, frontier)

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
    P.visited = True
    goal = maze.food_array[0]
    P_MH = helper.ManhattanDistance(P, goal)
    heapq.heappush(frontier, (P_MH, P))

    #check all directions of neighbors and add them on the frontier
    while(len(frontier) > 0):
    	currNode = heapq.heappop(frontier)[1]

        if not currNode.visited:
            currNode.visited = True
            expandedNodes += 1

    	if(currNode == goal):
    		break

    	for direction in range(0, 4):
    		if(maze.canTravel(currNode, direction) and not currNode.visited):
    			newNode = maze.getNode(currNode, direction)
    			helper.GreedyBestFirstSearch_AddToFrontier(currNode, newNode, goalNode, counter, frontier):

    currNode = goal
    while(currNode != P)
        current.char = '.'
        current = current.parent

    print("Path Cost: " + str(totalMazeCost))
    print("Expanded Nodes: " + str(expandedNodes))
    maze.printMaze()
    maze.writeMaze("greedy")

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
    startHeuristic = helper.ManhattanDistance(start, goal)
    counter = 1
    heapq.heappush(frontier, (start.pathCost + startHeuristic, counter, maze.startingNode))

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
                    helper.AStar_AddToFrontier(curNode, neighbor, goal, counter, frontier)

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
    startHeuristic = helper.AStarMultiSearch_ComputeHeuristic(mazes[startMazeIndex], start)
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
        curNodeHeuristic = helper.AStarMultiSearch_ComputeHeuristic(mazes[mazeIndex], curNode)

        # Expand this node only if it hasn't been expanded (visited) yet
        # and its value of f(n) is less than the current discovered path
        # cost to the goal
        if not curNode.visited and (curNode.pathCost+curNodeHeuristic) < trueCost:
            curNode.visited = True
            expandedNodes += 1

            # If the expanded node is a goal state,
            # compute the total path cost it took to get there
            if len(mazes[mazeIndex].food_array) == 0:
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
                        helper.AStarMultiSearch_AddToFrontier(curNode, newNode, counter,
                                                       mazes, newMazeIndex, frontier)
                    else:
                        helper.AStarMultiSearch_AddToFrontier(curNode, neighbor, counter,
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

from string import ascii_lowercase
from string import ascii_uppercase

# This is an implementation of MP 1.2 with Breadth-First Search
# for debugging purposes.
def BFSMultiSearch(maze):
    """
    mazes = []
    mazes.append(maze)

    # Initialize the frontier (represented as a queue),
    # the start Node, the index of the maze in mazes
    # the start Node belongs to, and the goal state
    q = []
    startMazeIndex = 0
    start = mazes[startMazeIndex].startingNode
    goal = None

    q.append((startMazeIndex, start))

    # Initialize a counter to count the number of nodes that get expanded
    expandedNodes = 0

    while len(q) > 0:
        tup = q.pop(0)
        print("tup: " + str(tup))
        current = tup[1]
        print("current: " + str(current))
        mazeIndex = tup[0]

        if not current.visited:
            current.visited = True
            expandedNodes += 1

            if len(mazes[mazeIndex].food_array) == 0:
                goal = current
                break

            adj = mazes[mazeIndex].getAdjacent(current)

            for node in adj:
                if not node.visited:
                    if node.char == '.':
                        node.visited = True
                        newMazeIndex = len(mazes)
                        mazes.append(Maze(origMaze=mazes[mazeIndex], remove_pellet=node))
                        newNode = mazes[newMazeIndex].maze[node.y][node.x]

                        newNode.parent = current
                        q.append((newMazeIndex, newNode))
                    else:
                        node.parent = current
                        q.append((mazeIndex, node))
    """
    assert goal is not None, "ERROR: No goal state found"

    current = goal
    totalMazeCost = 0

    pelletCounter = 1
    outOfNumbers = False
    outOfLowerCaseLetters = False
    lowerCaseLetterIndex = 0
    outOfUpperCaseLetters = False
    upperCaseLetterIndex = 0
    while (current != start):
        totalMazeCost += 1
        if current.char == 'P':
            if not outOfNumbers:
                print(current)
                current.char = str(pelletCounter)
                print(current.char)
                pelletCounter += 1

                if pelletCounter >= 10:
                    outOfNumbers = True
            elif not outOfLowercaseLetters:
                current.char = str(ascii_lowercase[lowerCaseLetterIndex])
                lowerCaseLetterIndex += 1

                if lowerCaseLetterIndex >= len(ascii_lowercase):
                    outOfLowerCaseLetters = True
            else:
                current.char = str(ascii_uppercase[upperCaseLetterIndex])
                upperCaseLetterIndex += 1

                assert upperCaseLetterIndex < len(ascii_uppercase), "ERROR: Too many pellets to represent"
        else:
            current.char = '.'

        current = current.parent

    print("Path Cost: " + str(totalMazeCost))
    print("Expanded Nodes: " + str(expandedNodes))
    maze.printMaze()
    #maze.writeMaze("BFSMultiSearch")
