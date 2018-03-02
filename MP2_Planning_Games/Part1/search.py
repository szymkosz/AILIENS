"""
-------------------------------------------------------------------------------
This file contains all the code for the search algorithms used in part 1.

EACH PROBLEM INSTANCE AND SEARCH ALGORITHM MUST RETURN THE FOLLOWING:

1. The solution, represented as a string of the sequence of factories to visit
2. The cost of the solution, defined as either the number of stops or the
   distance traveled
3. The number of nodes expanded by the search algorithm
-------------------------------------------------------------------------------
"""

# Import all the necessary packages
import widget
import heapq
import helper

"""
-------------------------------------------------------------------------------
PART 1.1 STARTS HERE!
-------------------------------------------------------------------------------
"""

# Computes the factory sequence with the smallest number of stops using the A* algorithm.
# In A*, unexpanded nodes on the frontier are sorted with a min Priority Queue.
# The priority f(n) of a node n is computed as:
#
# f(n) = g(n) + h(n) , where
#
# g(n) = cost so far to reach n (path cost)
# h(n) = estimated cost from n to goal state (heuristic)
#
# The heuristic h(n) is computed as the longest common subsequence among
# the sequences of remaining widget components.
def AStar_MinStops(recipes):
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
def AStar_MinDistance(recipes):
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
PART 1.3 STARTS HERE!
-------------------------------------------------------------------------------
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
def UCS_MinStops(recipes):
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
def UCS_MinDistance(recipes):
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
