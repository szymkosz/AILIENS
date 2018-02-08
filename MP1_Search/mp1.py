import sys
import search
from node import Node
from maze import Maze

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

## Obtain maze text file from command line
# try:
#     fileName = sys.argv[1]
# except:
#     print("Must include maze text file name as input. For example:")
#     print(" $ python %s file.txt" % sys.argv[0])
#     quit()

# ## Prints the maze to standard output
# def printMaze():
#     maze = Node.maze
#     for i in range(len(maze)):
#         #sys.stdout.write("%3d  " % i)  # Adds row numbers
#         sys.stdout.write(' '.join(n.__repr__() for n in maze[i]))
#     sys.stdout.write("\n")
#
# ## Prints each node of the maze as a string -> (x, y) char
# def printAllNodes():
#     maze = Node.maze
#     for i in range(len(maze)):
#         for j in range(len(maze[i])):
#             print(maze[i][j])
#
# ## Write the current state of the maze nodes into a txt file
# def writeMaze():
#     idx = fileName.find('.txt')
#     solutionFileName = fileName[0:idx] + "_sol" + fileName[idx:]
#     f = open(solutionFileName, 'w')
#     for i in range(len(maze)):
#         for j in range(len(maze[i])):
#             f.write(maze[i][j].value)
#     f.close()

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

maze = Maze("mediumMaze.txt")
# parseMazeFile()
# Node.maze[3][1].value = '.'
# print(Node.maze[3][1])
# Node.maze[4][1].value = '.'
#
# maze.printMaze()
# maze.writeMaze()

maze.printMaze()
#
# print(Node.maze[4][4].startingNode)
# print(Node.maze[15][12].startingNode)
# writeMaze()
# printAllNodes()
