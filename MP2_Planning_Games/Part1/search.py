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
    # Initialize the frontier (represented as a priority queue)
    # and identify the start and goal Nodes
    frontier = []
    start = node.Node(list(recipes), "")
    goal = None

    # Mark the start with a cost of 0, compute its heuristic, initialize a counter
    # for breaking ties in the frontier, and add the start to the frontier
    startCost = 0
    startHeuristic = helper.scsOf5List(recipes)
    counter = 1
    heapq.heappush(frontier, (startCost + startHeuristic, counter, start))

    # Initialize a counter to count the number of nodes that get expanded
    expandedNodes = 0

    while len(frontier) > 0:
        # Remove node from frontier
        curNode = heapq.heappop(frontier)[2]
        expandedNodes += 1
        print(curNode.remainingRecipes)
        print(curNode.progress)

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

        for letter in letters:
            newRemainingRecipes = []
            isNewState = False

            for recipe in curNode.remainingRecipes:
                newRecipe = None

                if len(recipe) == 0:
                    newRecipe = ""
                elif recipe[0] == letter:
                    isNewState = True

                    if len(recipe) == 1:
                        newRecipe = ""
                    else:
                        newRecipe = recipe[1:]
                else:
                    newRecipe = recipe[0:]

                newRemainingRecipes.append(newRecipe)

            if isNewState:
                newNode = node.Node(newRemainingRecipes, curNode.progress + letter)

                print("New Node:")
                newCost = len(newNode.progress)
                print(newCost)
                newHeuristic = helper.scsOf5List(newNode.remainingRecipes)
                print(newHeuristic)
                counter += 1
                heapq.heappush(frontier, (newCost + newHeuristic, counter, newNode))

    print("Optimal Solution: " + goal.progress)
    print("Minimum Number of Stops: " + str(len(goal.progress)))
    print("Expanded Nodes: " + str(expandedNodes))


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
def AStar_MinDistance(recipes, startFactory, distances, letters):
    # Initialize the frontier (represented as a priority queue),
    # the true path cost, and identify the start and goal Nodes
    frontier = []
    start = node.Node(list(recipes), startFactory)
    goal = None
    trueCost = float("inf")

    # Mark the start with a cost of 0, initialize a counter for breaking ties
    # in the frontier, and add the start to the frontier
    startCost = 0
    startHeuristic = ?
    counter = 1
    heapq.heappush(frontier, (startCost + startHeuristic, counter, start))

    # Initialize a counter to count the number of nodes that get expanded
    expandedNodes = 0

    while len(frontier) > 0:
        # Remove node from frontier
        tup = heapq.heappop(frontier)
        curCost = tup[0]
        curNode = tup[2]
        expandedNodes += 1

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
            trueCost = curCost
            goal = curNode
            break

        for letter in letters:
            newRemainingRecipes = []
            isNewState = False

            for recipe in curNode.remainingRecipes:
                newRecipe = None

                if len(recipe) == 0:
                    newRecipe = ""
                elif recipe[0] == letter:
                    isNewState = True

                    if len(recipe) == 1:
                        newRecipe = ""
                    else:
                        newRecipe = recipe[1:]
                else:
                    newRecipe = recipe[0:]

                newRemainingRecipes.append(newRecipe)

            if isNewState:
                newNode = node.Node(newRemainingRecipes, curNode.progress + letter)

                newCost = curCost + distances[curNode.progress[-1]][letter]
                newHeuristic = ?
                counter += 1
                heapq.heappush(frontier, (newCost + newHeuristic, counter, newNode))

    print("Optimal Solution: " + goal.progress)
    print("Minimum Distance: " + str(trueCost))
    print("Expanded Nodes: " + str(expandedNodes))


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
    # Initialize the frontier (represented as a priority queue)
    # and identify the start and goal Nodes
    frontier = []
    start = node.Node(list(recipes), "")
    goal = None

    # Mark the start with a cost of 0, initialize a counter for breaking ties
    # in the frontier, and add the start to the frontier
    startCost = 0
    counter = 1
    heapq.heappush(frontier, (startCost, counter, start))

    # Initialize a counter to count the number of nodes that get expanded
    expandedNodes = 0

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
        # It should be okay to end the search here because the nodes were
        # expanded in order of increasing path cost.
        if isGoalNode:
            goal = curNode
            break

        for letter in letters:
            newRemainingRecipes = []
            isNewState = False

            for recipe in curNode.remainingRecipes:
                newRecipe = None

                if len(recipe) == 0:
                    newRecipe = ""
                elif recipe[0] == letter:
                    isNewState = True

                    if len(recipe) == 1:
                        newRecipe = ""
                    else:
                        newRecipe = recipe[1:]
                else:
                    newRecipe = recipe[0:]

                newRemainingRecipes.append(newRecipe)

            if isNewState:
                newNode = node.Node(newRemainingRecipes, curNode.progress + letter)

                newCost = len(newNode.progress)
                counter += 1
                heapq.heappush(frontier, (newCost, counter, newNode))

    print("Optimal Solution: " + goal.progress)
    print("Minimum Number of Stops: " + str(len(goal.progress)))
    print("Expanded Nodes: " + str(expandedNodes))


# Computes the factory sequence with the smallest distance using the
# uniform cost search algorithm.
# In uniform cost search, unexpanded nodes on the frontier are sorted with a
# min Priority Queue where the priority g(n) of a node n is the cost so far to
# reach n (path cost).
def UCS_MinDistance(recipes, startFactory, distances, letters):
    # Initialize the frontier (represented as a priority queue),
    # the true path cost, and identify the start and goal Nodes
    frontier = []
    start = node.Node(list(recipes), startFactory)
    goal = None
    trueCost = float("inf")

    # Mark the start with a cost of 0, initialize a counter for breaking ties
    # in the frontier, and add the start to the frontier
    startCost = 0
    counter = 1
    heapq.heappush(frontier, (startCost, counter, start))

    # Initialize a counter to count the number of nodes that get expanded
    expandedNodes = 0

    while len(frontier) > 0:
        # Remove node from frontier
        tup = heapq.heappop(frontier)
        curCost = tup[0]
        curNode = tup[2]
        expandedNodes += 1

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
            trueCost = curCost
            goal = curNode
            break

        for letter in letters:
            newRemainingRecipes = []
            isNewState = False

            for recipe in curNode.remainingRecipes:
                newRecipe = None

                if len(recipe) == 0:
                    newRecipe = ""
                elif recipe[0] == letter:
                    isNewState = True

                    if len(recipe) == 1:
                        newRecipe = ""
                    else:
                        newRecipe = recipe[1:]
                else:
                    newRecipe = recipe[0:]

                newRemainingRecipes.append(newRecipe)

            if isNewState:
                newNode = node.Node(newRemainingRecipes, curNode.progress + letter)

                newCost = curCost + distances[curNode.progress[-1]][letter]
                counter += 1
                heapq.heappush(frontier, (newCost, counter, newNode))

    print("Optimal Solution: " + goal.progress)
    print("Minimum Distance: " + str(trueCost))
    print("Expanded Nodes: " + str(expandedNodes))
