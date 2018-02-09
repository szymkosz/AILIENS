# Import all the necessary packages
from maze import Maze
from node import Node
# from asyncio import Queue as Q
# from asyncio import PriorityQueue as PQ
# from asyncio import LifoQueue as S

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

# Adds a new node to the frontier within the A* algorithm for MP 1.1
def AStar_AddToFrontier(curNode, newNode, goalNode, frontier):
    newNode.parent = curNode
    newNode.cost = curNode.cost + 1
    newHeuristic = ManhattanDistance(newNode, goalNode)
    print(newNode)
    print((newNode.cost + newHeuristic, newNode))
    #frontier.put_nowait((newNode.cost + newHeuristic, newNode))
    heapq.heappush(frontier, (newNode.cost + newHeuristic, newNode))
    print(frontier)


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
    while (len(s) > 0):
        current = s.pop(-1)
        if not current.visited:
            current.visited = True
            adj = maze.getAdjacent(current)
            while len(adj) > 0:
                node = adj.pop()
                if not node.visited:
                    node.parent = current
                    s.append(node)
    current = goal
    maze.cost = 0
    while (current != start):
        maze.cost += 1
        current.char = '.'
        current = current.parent

def BreadthFirstSearch(maze):
    q = []
    start = maze.startingNode
    goal = maze.food_array[0]

    q.append(start)
    while len(q) > 0:
        current = q.pop(0)
        if not current.visited:
            current.visited = True
            adj = maze.getAdjacent(current)
            for node in adj:
                if not node.visited:
                    node.parent = current
                    q.append(node)
    current = goal
    maze.cost = 0
    while (current != start):
        maze.cost += 1
        current.char = '.'
        current = current.parent

def GreedyBestFirstSearch(maze):
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
    #Initialize priority queue and identify the start and goal Nodes
    frontier = []
    start = maze.startingNode
    goal = maze.food_array[0]
    trueCost = float("inf")

    #Mark the start as visited with a cost of 0 and add it to the frontier
    start.cost = 0
    startHeuristic = ManhattanDistance(start, goal)
    #frontier.put_nowait((start.cost + startHeuristic, maze.startingNode))
    heapq.heappush(frontier, (start.cost + startHeuristic, maze.startingNode))

    expandedNodes = 0
    #print(start)
    #print(goal)
    #print(frontier)

    while len(frontier) > 0:
        # Expand node on frontier
        #curNode = frontier.get_nowait()[1]
        curNode = heapq.heappop(frontier)[1]
        #print(curNode)
        curNodeHeuristic = ManhattanDistance(curNode, goal)

        if not curNode.visited and (curNode.cost+curNodeHeuristic) < trueCost:
            curNode.visited = True
            expandedNodes += 1

            # Compute the cost
            if curNode == goal:
                pathCost = 0
                current = goal

                while current != start:
                    pathCost += 1
                    current = current.parent

                if pathCost < trueCost:
                    trueCost = pathCost

            neighbors = maze.getAdjacent(curNode)
            for neighbor in neighbors:
                print("I am here")
                if not neighbor.visited:
                    AStar_AddToFrontier(curNode, neighbor, goal, frontier)

    current = goal
    maze.cost = 0
    while (current != start):
        maze.cost += 1
        current.char = '.'
        current = current.parent


"""
-------------------------------------------------------------------------------
MP 1.2 STARTS HERE!
-------------------------------------------------------------------------------
"""
def AStarMultiSearch(maze):
    pass
