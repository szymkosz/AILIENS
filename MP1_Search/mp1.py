import sys
import search
from node import Node
from maze import Maze

# from asyncio import Queue as Q
# from asyncio import PriorityQueue as PQ

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

x = 1
y = 3

print(maze[y][x])
# print(maze.canTravel(maze.maze[y][x], RIGHT))
# print(maze.canTravel(maze.maze[y][x], DOWN))
# print(maze.canTravel(maze.maze[y][x], LEFT))
# print(maze.canTravel(maze.maze[y][x], UP))

print(maze.canTravel(maze[y][x], RIGHT))
print(maze.canTravel(maze[y][x], DOWN))
print(maze.canTravel(maze[y][x], LEFT))
print(maze.canTravel(maze[y][x], UP))
print(maze.width(), maze.height())

maze.printMaze()
# maze.printMaze()
