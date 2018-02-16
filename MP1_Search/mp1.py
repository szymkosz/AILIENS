import sys
import search
from node import Node
from maze import Maze

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

# maze = Maze("mp1.1MazeFiles/mediumMaze.txt")
# maze = Maze("mp1.2MazeFiles/extraTinySearch.txt")
# maze.printMaze()

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

# search.BFSMultiSearch(maze)
# maze.printMaze()

""" Part 1 Test """
files = ["mp1.1MazeFiles/mediumMaze.txt", "mp1.1MazeFiles/bigMaze.txt", "mp1.1MazeFiles/openMaze.txt"]
part1searches = [search.BreadthFirstSearch, search.DepthFirstSearch, search.GreedyBestFirstSearch, search.AStar]

for search in part1searches:
    for i in files:
        maze = Maze(i)
        print(str(search), str(i))
        search(maze)
        del(maze)
# maze.printMaze()
# maze.writeMaze()
# print(maze.cost)
