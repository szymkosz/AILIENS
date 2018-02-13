# Import all the necessary packages
#from maze import Maze
from node import Node
import heapq

"""
-------------------------------------------------------------------------------
THIS FILE IS FOR HELPER FUNCTIONS!
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


# Computes the heuristic for MP 1.2.
def AStarMultiSearch_ComputeHeuristic(maze, curNode):
    curMinDistanceToPellet = min(helper.ManhattanDistance(curNode, pellet) for pellet in maze.food_array)
    return maze.MSTCost + curMinDistanceToPellet


# Adds a new node to the frontier within the A* algorithm for MP 1.2
def AStarMultiSearch_AddToFrontier(curNode, newNode, counter, mazes, mazeIndex, frontier):
    newNode.parent = curNode
    newNode.pathCost = curNode.pathCost + 1
    newHeuristic = AStarMultiSearch_ComputeHeuristic(mazes[mazeIndex], newNode)
    heapq.heappush(frontier, (newNode.pathCost + newHeuristic,
                              counter, mazeIndex, newNode))
                          
def AStarMultiSearch_TraceSolution(maze, pelletArray):
    solutionPath = []
    pathCost = 0
    for i in range(len(pelletArray)-1):
        if (pelletArray[i], pelletArray[i+1]) in maze.paths.keys():
            currentPath = maze.paths[(pelletArray[i], pelletArray[i+1])][1]
            for coord in range(len(currentPath)-1):
                pathCost += 1
                solutionPath.append(currentPath[coord])
        else:
            assert (pelletArray[i+1], pelletArray[i]) in maze.paths.keys(), "ERROR: Pellet Coordinate combination not in maze.paths"
            currentPath = maze.paths[(pelletArray[i+1], pelletArray[i])][1]
            for coord in range(len(currentPath)-1):
                pathCost += 1
                solutionPath.append(currentPath[len(currentPath) - 2 - coord])
    solutionPath.append(pelletArray[-1])
    return (pathCost, solutionPath)