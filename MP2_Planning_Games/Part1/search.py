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
import node
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
# The heuristic h(n) is computed as
def AStar_MinStops(recipes, letters):
    # Initialize the frontier (represented as a priority queue), identify
    # the goal Node, and initialize a counter for breaking ties in the frontier
    frontier = []
    start = node.Node(list(recipes), "")
    goal = None

    helper.addNeighborsToFrontier(start, frontier, letters, True, helper.stopHeuristic)

    # Initialize a counter to count the number of nodes that get expanded
    expandedNodes = 1

    while len(frontier) > 0:
        # Remove node from frontier
        curNode = heapq.heappop(frontier)[2]
        expandedNodes += 1

        # Check if the removed node is the goal state
        # (check if there are no components left to build in any recipe)
        isGoalNode = True
        for recipe in curNode.remainingRecipes:
            if len(recipe) is not 0:
                isGoalNode = False
                break

        # If the removed node is the goal state, end the search.
        # It should be okay to end the search here because the
        # heuristic is admissable and consistent.
        if isGoalNode:
            goal = curNode
            break

        helper.addNeighborsToFrontier(curNode, frontier, letters, True, helper.stopHeuristic)

    print("Optimal Solution: " + goal.progress)
    print("Minimum Number of Stops: " + str(len(goal.progress)))
    print("Expanded Nodes: " + str(expandedNodes))

    return expandedNodes


# Computes the factory sequence with the smallest number of stops using the A* algorithm.
# In A*, unexpanded nodes on the frontier are sorted with a min Priority Queue.
# The priority f(n) of a node n is computed as:
#
# f(n) = g(n) + h(n) , where
#
# g(n) = cost so far to reach n (path cost)
# h(n) = estimated cost from n to goal state (heuristic)
#
# The heuristic h(n) is computed as
def AStar_MinDistance(recipes, distances, shortestPaths, letters):
    # Initialize the frontier (represented as a priority queue),
    # the true path cost, and identify the start and goal Nodes
    frontier = []
    start = node.Node(list(recipes), "")
    goal = None
    trueCost = float("inf")

    helper.addNeighborsToFrontier(start, frontier, letters, False, helper.distanceHeuristic, distances, shortestPaths)

    # Initialize a counter to count the number of nodes that get expanded.
    # This counter includes picking the starting factory for the sequence.
    expandedNodes = 1

    while len(frontier) > 0:
        # Remove node from frontier
        tup = heapq.heappop(frontier)
        curPathCost = tup[2]
        curNode = tup[3]
        expandedNodes += 1

        curLetter = ""
        if len(curNode.progress) >= 1:
            curLetter = curNode.progress[-1]

        # Check if the removed node is the goal state
        # (check if there are no components left to build in any recipe)
        isGoalNode = True
        for recipe in curNode.remainingRecipes:
            if len(recipe) is not 0:
                isGoalNode = False
                break

        # If the removed node is the goal state, end the search.
        # It should be okay to end the search here because the nodes were
        # expanded in order of increasing path cost.
        if isGoalNode:
            trueCost = curPathCost
            goal = curNode
            break

        helper.addNeighborsToFrontier(curNode, frontier, letters, False, helper.distanceHeuristic, distances, shortestPaths, curPathCost, curLetter)

    print("Optimal Solution: " + goal.progress)
    print("Minimum Distance: " + str(trueCost))
    print("Expanded Nodes: " + str(expandedNodes))

    return expandedNodes


"""
-------------------------------------------------------------------------------
PART 1.3 STARTS HERE!
-------------------------------------------------------------------------------
"""

# Computes the factory sequence with the smallest number of stops using the
# uniform cost search algorithm.
# In uniform cost search, unexpanded nodes on the frontier are sorted with a
# min Priority Queue where the priority g(n) of a node n is the cost so far to
# reach n (path cost).
def UCS_MinStops(recipes, letters):
    # Initialize the frontier (represented as a priority queue), identify
    # the goal Node, and initialize a counter for breaking ties in the frontier
    frontier = []
    start = node.Node(list(recipes), "")
    goal = None

    helper.addNeighborsToFrontier(start, frontier, letters, True)

    # Initialize a counter to count the number of nodes that get expanded
    expandedNodes = 1

    while len(frontier) > 0:
        # Remove node from frontier
        curNode = heapq.heappop(frontier)[2]
        expandedNodes += 1

        # Check if the removed node is the goal state
        # (check if there are no components left to build in any recipe)
        isGoalNode = True
        for recipe in curNode.remainingRecipes:
            if len(recipe) is not 0:
                isGoalNode = False
                break

        # If the removed node is the goal state, end the search.
        # It should be okay to end the search here because the
        # heuristic is admissable and consistent.
        if isGoalNode:
            goal = curNode
            break

        helper.addNeighborsToFrontier(curNode, frontier, letters, True)

    print("Optimal Solution: " + goal.progress)
    print("Minimum Number of Stops: " + str(len(goal.progress)))
    print("Expanded Nodes: " + str(expandedNodes))

    return expandedNodes


# Computes the factory sequence with the smallest distance using the
# uniform cost search algorithm.
# In uniform cost search, unexpanded nodes on the frontier are sorted with a
# min Priority Queue where the priority g(n) of a node n is the cost so far to
# reach n (path cost).
def UCS_MinDistance(recipes, distances, shortestPaths, letters):
    # Initialize the frontier (represented as a priority queue),
    # the true path cost, and identify the start and goal Nodes
    frontier = []
    start = node.Node(list(recipes), "")
    goal = None
    trueCost = float("inf")

    helper.addNeighborsToFrontier(start, frontier, letters, False, None, distances, shortestPaths)

    # Initialize a counter to count the number of nodes that get expanded.
    # This counter includes picking the starting factory for the sequence.
    expandedNodes = 1

    while len(frontier) > 0:
        # Remove node from frontier
        tup = heapq.heappop(frontier)
        curPathCost = tup[2]
        curNode = tup[3]
        expandedNodes += 1

        curLetter = ""
        if len(curNode.progress) >= 1:
            curLetter = curNode.progress[-1]

        # Check if the removed node is the goal state
        # (check if there are no components left to build in any recipe)
        isGoalNode = True
        for recipe in curNode.remainingRecipes:
            if len(recipe) is not 0:
                isGoalNode = False
                break

        # If the removed node is the goal state, end the search.
        # It should be okay to end the search here because the nodes were
        # expanded in order of increasing path cost.
        if isGoalNode:
            trueCost = curPathCost
            goal = curNode
            break

        helper.addNeighborsToFrontier(curNode, frontier, letters, False, None, distances, shortestPaths, curPathCost, curLetter)

    print("Optimal Solution: " + goal.progress)
    print("Minimum Distance: " + str(trueCost))
    print("Expanded Nodes: " + str(expandedNodes))

    return expandedNodes
