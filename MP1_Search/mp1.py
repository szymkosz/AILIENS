import sys
import search
from node import Node
from maze import Maze

# Define the values for representing the directions
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

# # Obtain maze text file from command line
# try:
#     fileName = sys.argv[1]
# except:
#     print("Must include maze text file name as input. For example:")
#     print(" $ python %s file.txt" % sys.argv[0])
#     quit()

maze = Maze("mediumMaze.txt")

"""
q = Q(maxsize=-1)
q.put_nowait(3)
q.put_nowait(5)
q.put_nowait(7)

print(q.qsize())
print(q.get_nowait())
print(q.get_nowait())
print(q.get_nowait())
"""
"""
from asyncio import PriorityQueue as PQ
frontier = PQ()
frontier.put_nowait((3, Node(1,1,'P')))
frontier.put_nowait((5, Node(2,1,' ')))
frontier.put_nowait((7, Node(1,2,' ')))

print(frontier.get_nowait())
print(frontier.get_nowait())
print(frontier.get_nowait())
"""

# import heapq

# frontier = []
# heapq.heappush(frontier, (3, Node(1,1,'P')))
# heapq.heappush(frontier, (5, Node(2,1,' ')))
# heapq.heappush(frontier, (7, Node(1,2,' ')))

# print(heapq.heappop(frontier))
# print(heapq.heappop(frontier))
# print(heapq.heappop(frontier))

# x = 3
# y = 1
# testNode = maze[y][x]
# print(testNode)
#
# for node in maze.getAdjacent(testNode):
#     print(node)

# maze.getNode(testNode, 4)
# print(maze.canTravel(maze.maze[y][x], RIGHT))
# print(maze.canTravel(maze.maze[y][x], DOWN))
# print(maze.canTravel(maze.maze[y][x], LEFT))
# print(maze.canTravel(maze.maze[y][x], UP))


# print(maze.canTravel(maze[y][x], RIGHT))
# print(maze.canTravel(maze[y][x], DOWN))
# print(maze.canTravel(maze[y][x], LEFT))
# print(maze.canTravel(maze[y][x], UP))
# print(maze.width(), maze.height())

# maze.printMaze()
# maze.printMaze()

""" BFS/DFS Test """
# search.BreadthFirstSearch(maze)
# search.DepthFirstSearch(maze)
search.GreedyBestFirstSearch(maze)
# search.AStar(maze)
maze.printMaze()
# maze.writeMaze()
# print(maze.cost)