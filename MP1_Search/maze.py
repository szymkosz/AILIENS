from node import Node
import sys

class Maze:
    def __init__(self, fileName):
        self.fileName = fileName
        self.maze = []
        self.food_array = []

        ## Open file and create matrix data structure
        with open(fileName, 'r') as file:
            h = 0

            ## Unfortunately, the way the file is read and parsed, the coordinates
            ## are backwards, so the array should be indexed with y first, then x
            ## i.e. Node.maze[y][x]
            for line in file:
                self.maze.append([ Node(w,h,line[w]) for w in range(len(line)) ])
                h+=1

    def printMaze(self):
        maze = self.maze
        for i in range(len(maze)):
            sys.stdout.write(' '.join(n.__repr__() for n in maze[i]))
        sys.stdout.write("\n")

    ## Prints each node of the maze as a string -> (x, y) char
    def printAllNodes(self):
        maze = self.maze
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                print(maze[i][j])

    ## Write the current state of the maze nodes into a txt file
    def writeMaze(self):
        maze = self.maze
        idx = self.fileName.find('.txt')
        solutionFileName = self.fileName[0:idx] + "_sol" + self.fileName[idx:]
        f = open(solutionFileName, 'w')
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                f.write(maze[i][j].char)
        f.close()
