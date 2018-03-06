# Import all the necessary packages
import node

import random
import heapq

counter = 0

"""
-------------------------------------------------------------------------------
SETUP HELPER FUNCTIONS START HERE!
-------------------------------------------------------------------------------
"""
def stopHeuristic(recipes):
    return max([len(recipe) for recipe in recipes])


def distanceHeuristic(recipes, distances, shortestPaths):
    maxDistance = 0;

    for recipe in recipes:
        curCost = 0

        for i in range(len(recipe) - 1):
            curLetter = recipe[i]
            nextLetter = recipe[i+1]

            path = (shortestPaths[curLetter][nextLetter])[1:]
            curPathLetter = curLetter

            for pathLetter in path:
                curCost += distances[curPathLetter][pathLetter]
                curPathLetter = pathLetter

        if curCost > maxDistance:
            maxDistance = curCost

    return maxDistance


def addNeighborsToFrontier(curNode, frontier, letters, isStops, heuristicFunction=None, distances=None, shortestPaths=None, curPathCost=0, curLetter=""):
    global counter

    for letter in letters:
        newRemainingRecipes = []
        isNewState = False

        for recipe in curNode.remainingRecipes:
            newRecipe = None

            if len(recipe) == 0:
                newRecipe = ""
            elif recipe[0] == letter:
                isNewState = True

                if len(recipe) == 1:
                    newRecipe = ""
                else:
                    newRecipe = recipe[1:]
            else:
                newRecipe = recipe[0:]

            newRemainingRecipes.append(newRecipe)

        if isNewState:
            if isStops:
                newNode = node.Node(newRemainingRecipes, curNode.progress + letter)

                newCost = len(newNode.progress)
                newHeuristic = None
                if heuristicFunction == stopHeuristic:
                    newHeuristic = heuristicFunction(newRemainingRecipes)
                else:
                    newHeuristic = 0

                counter += 1
                heapq.heappush(frontier, (newCost + newHeuristic, counter, newNode))
            else:
                # Initialize the path cost and progress of the neighboring Node.
                # If curNode is the start Node, these initial values are used
                # because no traveling occurs yet.
                newPathCost = 0
                newProgress = letter

                # If curNode is not the start Node, then compute the necessary
                # distance to travel from the current factory (curLetter) to
                # the factory represented by the neighboring Node (letter)
                if curNode.progress != "":
                    path = (shortestPaths[curLetter][letter])[1:]
                    newPathCost = curPathCost
                    newProgress = curNode.progress
                    curPathLetter = curLetter

                    for pathLetter in path:
                        newPathCost += distances[curPathLetter][pathLetter]
                        newProgress += pathLetter
                        curPathLetter = pathLetter

                newNode = node.Node(newRemainingRecipes, newProgress)
                newHeuristic = None
                if heuristicFunction == distanceHeuristic:
                    newHeuristic = heuristicFunction(newRemainingRecipes, distances, shortestPaths)
                else:
                    newHeuristic = 0

                counter += 1
                heapq.heappush(frontier, (newPathCost + newHeuristic, counter, newPathCost, newNode))
            #else:
            #    raise ValueError("The heuristic function must be 'stopHeuristic', 'distanceHeuristic' or 'None'")


def computeShortestPaths(distances, letters):
    shortestPaths = {}

    # Initialize every letter with an empty dictionary in shortestPaths
    for letter in letters:
        shortestPaths[letter] = {}

    for i in range(len(letters)):
        begginning = letters[i]

        for j in range(i+1, len(letters)):
            ending = letters[j]
            frontier = []

            # Mark the start with a cost of 0, initialize a counter for breaking ties
            # in the frontier, and add the start to the frontier
            startCost = 0
            counter = 1
            heapq.heappush(frontier, (startCost, counter, begginning))

            while len(frontier) > 0:
                # Remove node from frontier
                tup = heapq.heappop(frontier)
                curCost = tup[0]
                curProgress = tup[2]

                curLetter = curProgress[-1]

                # If the removed node is the goal state, end the search.
                # It should be okay to end the search here because the nodes were
                # expanded in order of increasing path cost.
                if curProgress[0] == begginning and curProgress[-1] == ending:
                    shortestPaths[begginning][ending] = [str(char) for char in curProgress]
                    shortestPaths[ending][begginning] = [str(char) for char in curProgress[::-1]]
                    break

                for letter in letters:
                    if curLetter != letter:
                        newNode = curProgress + letter

                        newCost = curCost + distances[curLetter][letter]
                        counter += 1
                        heapq.heappush(frontier, (newCost, counter, newNode))

    return shortestPaths


def generateWidgets(N, letters, numWidgets=5):
    newRecipes = []

    # Build a random recipe by picking each letter at random
    for i in range(numWidgets):
        newLetters = letters[0:]
        newRecipe = ""

        for j in range(N):
            newLetterIndex = round((len(newLetters)-1)*random.random())
            newLetter = newLetters[int(newLetterIndex)]
            newRecipe += newLetter

            nextNewLetters = letters[0:]
            nextNewLetters.remove(newLetter)
            newLetters = nextNewLetters

        newRecipes.append(newRecipe)

    return newRecipes


"""
-------------------------------------------------------------------------------
PART 1.1 HELPER FUNCTIONS START HERE!
-------------------------------------------------------------------------------
"""

# Takes in a list of 5 strings as one parameter and finds the Longest Common
# Subsequence (LCS) of those strings
def lcsOf5List(strings, printL=False):
    X, Y, Z, T, U = strings
    return lcsOf5(X, Y, Z, T, U, printL)

## Finds the length of the Longest Common Subsequence for 5 strings
def lcsOf5(X, Y, Z, T, U, printL=False):
    a, b, c, d, e = len(X), len(Y), len(Z), len(T), len(U)

    L = [[[[[0 for i in range(e+1)] for j in range(d+1)]
         for k in range(c+1)] for l in range(b+1)] for m in range(a+1)]

    for i in range(a+1):                    # X
        for j in range(b+1):                # Y
            for k in range(c+1):            # Z
                for l in range(d+1):        # T
                    for m in range(e+1):    # U
                        if (i == 0 or j == 0 or k == 0 or l == 0 or m == 0):
                            L[i][j][k][l][m] = 0

                        elif (X[i-1] == Y[j-1] and
                              X[i-1] == Z[k-1] and
                              X[i-1] == T[l-1] and
                              X[i-1] == U[m-1]):
                            L[i][j][k][l][m] = L[i-1][j-1][k-1][l-1][m-1] + 1

                        else:
                            L[i][j][k][l][m] = max(max(max(
                            max(L[i-1][j][k][l][m], L[i][j-1][k][l][m]),
                            L[i][j][k-1][l][m]), L[i][j][k][l-1][m]), L[i][j][k][l][m-1])

    # Prints the state of the L matrix before returning
    if printL:
        for i in range(len(L)):
            print("\n-------------- {0} --------------\n".format(i))
            for j in range(len(L[0])):
                for k in range(len(L[0][0])):
                    print(k, L[i][j][k])
                print("\n")

    return L[a][b][c][d][e]

def scsOf5List(strings, printL=False):
    return sum([len(string) for string in strings]) - lcsOf5List(strings, printL)


"""
-------------------------------------------------------------------------------
PART 1.3 HELPER FUNCTIONS START HERE!
-------------------------------------------------------------------------------
"""
