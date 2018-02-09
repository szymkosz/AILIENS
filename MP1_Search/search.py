# Import all the necessary packages
from maze import Maze
from node import Node
from asyncio import Queue as Q
from asyncio import PriorityQueue as PQ
from asyncio import LifoQueue as S


# Define the values for representing the directions
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3


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
    newNode.visited = True
    newHeuristic = ManhattanDistance(newNode, goalNode)
    frontier.put(newNode.cost + newHeuristic, newNode)

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
    pass


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
    frontier = PQ()
    start = maze.startingNode
    goal = maze.food_array[0]

    #Mark the start as visited with a cost of 0 and add it to the frontier
    start.cost = 0
    start.visited = True
    startHeuristic = ManhattanDistance(start, goal)
    frontier.put(start.cost + startHeuristic, maze.startingNode)

    expandedNodes = 0

    while(not frontier.empty()):
        # Expand node on frontier
        curNode = frontier.get()
        expandedNodes += 1

        # Look at rightward node
        if(maze.canTravel(curNode, RIGHT)):
            rightNode = maze[curNode.y][curNode.x+1]

            # This is the goal node.
            if(rightNode.char == '.'):
                pass

            if(not rightNode.visited):
                AStar_AddToFrontier(curNode, rightNode, goal, frontier)

        # Look at downward node
        if(maze.canTravel(curNode, DOWN)):
            downNode = maze[curNode.y+1][curNode.x]

            if(not downNode.visited):
                AStar_AddToFrontier(curNode, downNode, goal, frontier)

        # Look at leftward node
        if(maze.canTravel(curNode, LEFT)):
            leftNode = maze[curNode.y][curNode.x-1]

            if(not leftNode.visited):
                AStar_AddToFrontier(curNode, leftNode, goal, frontier)

        # Look at upward node
        if(maze.canTravel(curNode, UP)):
            upNode = maze[curNode.y-1][curNode.x]

            if(not curNode.visited):
                AStar_AddToFrontier(curNode, upNode, goal, frontier)


"""
-------------------------------------------------------------------------------
MP 1.2 STARTS HERE!
-------------------------------------------------------------------------------
"""
def AStarMultiSearch(maze):
    pass
