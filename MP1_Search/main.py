"""
-------------------------------------------------------------------------------
This file is for running the search algorithms on the different files.

To run a particular algorithm on a particular maze for part 1.1,
run the following command:

python main.py <part> <file> <algorithm>

where

<part> = "1.1", "mp1.1", "mp 1.1", "MP1.1", or "MP 1.1"
<file> = "mediumMaze.txt", "bigMaze.txt", or "openMaze.txt"
<algorithm> = "dfs" or "DFS" when running depth-first search
            : "bfs" or "BFS" when running breadth-first search
            : "greedy" or "GREEDY" when running greedy best-first search
            : "A*" or "Astar" or "AStar" when running A* search


To run part 1.2 on a particular maze, run the following command:

python main.py <part> <file>

where

<part> = "1.2", "mp1.2", "mp 1.2", "MP1.2", or "MP 1.2"
<file> = "tinySearch.txt", "smallSearch.txt", or "mediumSearch.txt"
-------------------------------------------------------------------------------
"""

import sys
import search
from node import Node
from maze import Maze


if __name__ == "__main__":
    incorrectUsageError = "Incorrect Usage: Expected " \
                        + "\"python %s <part> <file> " % sys.argv[0] \
                        + "<algorithm>\""

    incorrectUsageError2 = "Incorrect Usage: Expected " \
                         + "\"python %s <part> <file>\"" % sys.argv[0]

    assert len(sys.argv) > 2 and len(sys.argv) <= 4, incorrectUsageError

    part1Path = "mp1.1MazeFiles/"
    part2Path = "mp1.2MazeFiles/"

    # Run algorithms for MP 1.1
    if sys.argv[1] == "1.1" or sys.argv[1] == "mp1.1" or \
    sys.argv[1] == "mp 1.1" or sys.argv[1] == "MP1.1" or sys.argv[1] == "MP 1.1":
        assert len(sys.argv) == 4, incorrectUsageError

        # Load the maze if possible
        try:
            maze = Maze(part1Path + sys.argv[2])
        except:
            sys.exit("FileNotFoundError: Is the file spelled correctly?")

        # Run the appropriate search algorithm
        if sys.argv[3] == "dfs" or sys.argv[3] == "DFS":
            search.DepthFirstSearch(maze)
        elif sys.argv[3] == "bfs" or sys.argv[3] == "BFS":
            search.BreadthFirstSearch(maze)
        elif sys.argv[3] == "greedy" or sys.argv[3] == "GREEDY":
            search.GreedyBestFirstSearch(maze)
        elif sys.argv[3] == "A*" or sys.argv[3] == "Astar" or sys.argv[3] == "AStar":
            search.AStar(maze)
        else:
            sys.exit("AlgorithmNotRecognizedError: Is the algorithm spelled correctly?")

    # Run algorithm for MP 1.2
    elif sys.argv[1] == "1.2" or sys.argv[1] == "mp1.2" or \
    sys.argv[1] == "mp 1.2" or sys.argv[1] == "MP1.2" or sys.argv[1] == "MP 1.2":
        assert len(sys.argv) == 3, incorrectUsageError2

        # Load the maze if possible
        try:
            maze = Maze(part2Path + sys.argv[2])
        except:
            sys.exit("FileNotFoundError: Is the file spelled correctly?")

        search.AStarMultiSearch(maze)

    else:
        sys.exit("PartNotRecognizedError: Is the part spelled correctly?")





# import heapq

# frontier = []
# heapq.heappush(frontier, (3, Node(1,1,'P')))
# heapq.heappush(frontier, (5, Node(2,1,' ')))
# heapq.heappush(frontier, (7, Node(1,2,' ')))

# print(heapq.heappop(frontier))
# print(heapq.heappop(frontier))
# print(heapq.heappop(frontier))
