# Import all the necessary packages
from maze import Maze
from node import Node
from asyncio import Queue as Q
from asyncio import PriorityQueue as PQ

# Define the values for representing the directions
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

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

"""
Computes the Manhattan distance d from coordinates (x1, y1) to (x2, y2) as:

m = abs(x1 - x2) + abs(y1 - y2)

where abs() is the absolute value function.
"""
def ManhattanDistance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def ManhattanDistanceNode(node1, node2):
    return abs(node1.x - node2.x) + abs(node2.y - node2.y)

def DepthFirstSearch(maze):
    pass

def BreadthFirstSearch(maze):
    pass

def GreedyBestFirstSearch(maze):
    pass

"""
Searches for the food pellet using the A* algorithm.
In A*, unexpanded nodes on the frontier are sorted with a min Priority Queue.
The priority f(n) of a node n is computed as:

f(n) = g(n) + h(n) , where

g(n) = cost so far to reach n (path cost)
h(n) = estimated cost from n to goal (heuristic)

The heuristic h(n) is computed as the Manhattan distance from n to the goal.
"""
def AStar(maze):
    #Initialize priority queue and identify the start and goal Nodes
    frontier = PQ()
    start = maze.startingNode
    goal = maze.food_array[0]

    #Mark the start as visited and add it
    start.cost = 0
    start.visited = True
    startHeuristic = ManhattanDistance(start.x, start.y, goal.x, goal.y)
    frontier.put(start.cost + startHeuristic, maze.startingNode)

    expandedNodes = 0

    while(not frontier.empty()):
        curNode = frontier.get()
        expandedNodes += 1

        if(maze.canTravel(curNode, RIGHT)):
            if(not curNode.visited):
                rightNode = maze[curNode.y][curNode.x+1]

                rightNode.cost = curNode.cost + 1
                rightNode.visited = True
                rightHeuristic = ManhattanDistance(rightNode.x, rightNode.y, goal.x, goal.y)
                frontier.put(rightNode.cost + rightHeuristic, rightNode)
        if(maze.canTravel(curNode, DOWN)):
            pass
        if(maze.canTravel(curNode, LEFT)):
            pass
        if(maze.canTravel(curNode, UP)):
            pass


"""
-------------------------------------------------------------------------------
MP 1.2 STARTS HERE!
-------------------------------------------------------------------------------
"""
def AStarMultiSearch(maze):
    pass
