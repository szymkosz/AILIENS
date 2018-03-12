"""
HELPER FUNCTIONS GO IN THIS FILE!
"""

def addToCountDictionary(patternCounts, stoneColor, stoneCount):
    if stoneColor is None:
        patternCounts[("EMPTY", 0)] += 1
    elif stoneColor == "MIXED":
        patternCounts[("MIXED", 0)] += 1
    else:
        patternCounts[(stoneColor, stoneCount)] += 1


def loopOverBlock(game, x, y, dir):
    stoneColor = None
    stoneCount = 0

    for i in range(5):
        position = None

        if dir == "HORIZONTAL":
            position = game.board[x+i][y]
        elif dir == "VERTICAL":
            position = game.board[x][y+i]
        elif dir == "DIAGUPRIGHT":
            position = game.board[x+i][y+i]
        elif dir == "DIAGDOWNRIGHT":
            position = game.board[x+i][y-i]
        else:
            raise ValueError("dir must be 'HORIZONTAL', 'VERTICAL'," + \
                             "'DIAGUPRIGHT', or 'DIAGDOWNRIGHT'!")

        if position.char != '.':
            if stoneColor is None:
                stoneColor = position.color
            elif position.color != stoneColor:
                stoneColor = "MIXED"
                break

            stoneCount += 1

    return (stoneColor, stoneCount)


def addToBlockCoordinatesDictionary(blockCoordinates, stoneColor, stoneCount, x, y, dir):
    if stoneColor is None:
        blockCoordinates[("EMPTY", 0)].append((x, y, dir))
    elif stoneColor == "MIXED":
        blockCoordinates[("MIXED", 0)].append((x, y, dir))
    else:
        blockCoordinates[(stoneColor, stoneCount)].append((x, y, dir))

def loopOverBlockCoordinates(game, x, y, dir):
    stoneColor = None
    stoneCount = 0
    bestMove = None

    for i in range(5):
        position = None
        posCoordinates = None

        if dir == "HORIZONTAL":
            posCoordinates = (x+i, y)
            position = game.board[x+i][y]
        elif dir == "VERTICAL":
            posCoordinates = (x, y+i)
            position = game.board[x][y+i]
        elif dir == "DIAGUPRIGHT":
            posCoordinates = (x+i, y+i)
            position = game.board[x+i][y+i]
        elif dir == "DIAGDOWNRIGHT":
            posCoordinates = (x+i, y-i)
            position = game.board[x+i][y-i]
        else:
            raise ValueError("dir must be 'HORIZONTAL', 'VERTICAL'," + \
                             "'DIAGUPRIGHT', or 'DIAGDOWNRIGHT'!")

        if position.char != '.':
            if stoneColor is None:
                stoneColor = position.color
            elif position.color != stoneColor:
                stoneColor = "MIXED"
                break

            stoneCount += 1
        elif bestMove is None:
            leftAdjacent = None
            rightAdjacent = None

            if dir == "HORIZONTAL":
                if (x+i -1) >= x:
                    leftAdjacent = game.board[x+i-1][y]
                if (x+i +1) <= (x+4):
                    rightAdjacent = game.board[x+i+1][y]
            elif dir == "VERTICAL":
                if (y+i -1) >= y:
                    leftAdjacent = game.board[x][y+i-1]
                if (y+i +1) <= (y+4):
                    rightAdjacent = game.board[x][y+i+1]
            elif dir == "DIAGUPRIGHT":
                if (x+i -1) >= x and (y+i -1) >= y:
                    leftAdjacent = game.board[x+i-1][y+i-1]
                if (x+i +1) <= (x+4) and (y+i +1) <= (y+4):
                    rightAdjacent = game.board[x+i+1][y+i+1]
            elif dir == "DIAGDOWNRIGHT":
                if (x+i -1) >= x and (y-i +1) <= y:
                    leftAdjacent = game.board[x+i-1][y-i+1]
                if (x+i +1) <= (x+4) and (y-i -1) >= (y-4):
                    rightAdjacent = game.board[x+i+1][y-i-1]
            else:
                raise ValueError("dir must be 'HORIZONTAL', 'VERTICAL'," + \
                                 "'DIAGUPRIGHT', or 'DIAGDOWNRIGHT'!")

            if ((leftAdjacent is not None) and leftAdjacent.char != '.') or\
               ((rightAdjacent is not None) and rightAdjacent.char != '.'):
               bestMove = posCoordinates

    return (stoneColor, stoneCount, bestMove)

def findCoordinates(game):
    blockCoordinates = {}
    blockPlaceMove = {}
    blockCoordinates[("EMPTY", 0)] = []
    blockCoordinates[("MIXED", 0)] = []

    directions = ["HORIZONTAL", "VERTICAL", "DIAGUPRIGHT", "DIAGDOWNRIGHT"]

    for i in range(1, 6):
        blockCoordinates[("RED", i)] = []
        blockCoordinates[("BLUE", i)] = []

    # Loop over all horizontal blocks of 5 consecutive squares
    for x in range(game.dim - 4):
        for y in range(game.dim):
            stoneColor, stoneCount, bestMove =  loopOverBlockCoordinates(game, x, y, directions[0])
            addToBlockCoordinatesDictionary(blockCoordinates, stoneColor, stoneCount, x, y, directions[0])
            blockPlaceMove[(x, y, directions[0])] = bestMove

    # Loop over all vertical blocks of 5 consecutive squares
    for x in range(game.dim):
        for y in range(game.dim - 4):
            stoneColor, stoneCount, bestMove =  loopOverBlockCoordinates(game, x, y, directions[1])
            addToBlockCoordinatesDictionary(blockCoordinates, stoneColor, stoneCount, x, y, directions[1])
            blockPlaceMove[(x, y, directions[1])] = bestMove

    # Loop over all diagonal upright blocks of 5 consecutive squares
    for x in range(game.dim - 4):
        for y in range(game.dim - 4):
            stoneColor, stoneCount, bestMove =  loopOverBlockCoordinates(game, x, y, directions[2])
            addToBlockCoordinatesDictionary(blockCoordinates, stoneColor, stoneCount, x, y, directions[2])
            blockPlaceMove[(x, y, directions[2])] = bestMove

    # Loop over all diagonal downright blocks of 5 consecutive squares
    for x in range(game.dim - 4):
        for y in range(4, game.dim):
            stoneColor, stoneCount, bestMove =  loopOverBlockCoordinates(game, x, y, directions[3])
            addToBlockCoordinatesDictionary(blockCoordinates, stoneColor, stoneCount, x, y, directions[3])
            blockPlaceMove[(x, y, directions[3])] = bestMove

    return (blockCoordinates, blockPlaceMove)


def findBlocks(game):
    patternCounts = {}
    patternCounts[("EMPTY", 0)] = 0
    patternCounts[("MIXED", 0)] = 0

    for i in range(1, 6):
        patternCounts[("RED", i)] = 0
        patternCounts[("BLUE", i)] = 0

    # Loop over all horizontal blocks of 5 consecutive squares
    for x in range(game.dim - 4):
        for y in range(game.dim):
            stoneColor, stoneCount =  loopOverBlock(game, x, y, "HORIZONTAL")
            addToCountDictionary(patternCounts, stoneColor, stoneCount)

    # Loop over all vertical blocks of 5 consecutive squares
    for x in range(game.dim):
        for y in range(game.dim - 4):
            stoneColor, stoneCount =  loopOverBlock(game, x, y, "VERTICAL")
            addToCountDictionary(patternCounts, stoneColor, stoneCount)

    # Loop over all diagonal upright blocks of 5 consecutive squares
    for x in range(game.dim - 4):
        for y in range(game.dim - 4):
            stoneColor, stoneCount =  loopOverBlock(game, x, y, "DIAGUPRIGHT")
            addToCountDictionary(patternCounts, stoneColor, stoneCount)

    # Loop over all diagonal downright blocks of 5 consecutive squares
    for x in range(game.dim - 4):
        for y in range(4, game.dim):
            stoneColor, stoneCount =  loopOverBlock(game, x, y, "DIAGDOWNRIGHT")
            addToCountDictionary(patternCounts, stoneColor, stoneCount)

    return patternCounts


import numpy as np

weights = np.asarray([1, 2, 3, 4, -1, -2, -3, -4])

# This is the evaluation function for the minimax and alpha-beta agents.
#
# Given a player color, dictionaries of information about chains of stones
# on the board, and a dictionary of information about blocks of 5 consecutive
# squares on the board, this function will check for guaranteed wins and losses
# for the given player color and return positive or negative infinity accordingly
# if any are found.  Otherwise, a linear combination of the weights with the numbers
# of blocks of each category is computed and returned.
# @param playerColor    The color of the agent calling this function.
#                       This parameter can either be the string "RED" for
#                       the red player or "BLUE" for the blue player.
#                       Otherwise, a ValueError is raised.
# @param patterns       A tuple of three dictionaries representing counts,
#                       the endpoints of chains of stones, and moves to
#                       complete these chains
# @param blocks         A dictionary of counts of the numbers of blocks with no
#                       stones, both red and blue stones, and a given number
#                       of red or blue stones.
def evalLayout(playerColor, patterns, blocks):
    # Using the playerColor parameter, deduce the color of the opponent.
    # If the playerColor parameter is invalid, a ValueError is raised.
    opponentColor = None
    if playerColor == "RED":
        opponentColor = "BLUE"
    elif playerColor == "BLUE":
        opponentColor = "RED"
    else:
        raise ValueError("playerColor must be 'RED' or 'BLUE'!")

    patternMovesToComplete = patterns[2]
    # TODO: Verify these checks for guaranteed wins and losses are correct

    # If this board layout has a chain of 4 stones of the opponent's color with an
    # empty adjacent square, it is treated as an automatic loss and negative infinity is returned.
    opponentChainOf4 = patternMovesToComplete[(opponentColor, 4, True)][True]

    if len(opponentChainOf4) >= 1:
        return float("-inf")

    # If this board layout has at least 2 empty squares that can complete a chain
    # of 4 stones of the player's color, it is treated as an automatic win and
    # positive infinity is returned.
    playerChainOf4 = patternMovesToComplete[(playerColor, 4, True)][True]
    emptyAdjacentSquares = 0

    # Compute the number of empty squares adjacent
    # to chains of 4 stones the player's color
    for moves in playerChainOf4:
        emptyAdjacentSquares += len(moves)

    if emptyAdjacentSquares >= 2:
        return float("inf")

    # If this point is reached, the board layout has no guaranteed wins
    # or losses for this player within the next two moves, so a linear
    # combination of weights with the numbers of patterns should be
    # computed and returned.
    counts = []

    # Append this player's counts to the counts array first
    # to make sure they are assigned positive weights
    counts.append(blocks[(playerColor, 1)])
    counts.append(blocks[(playerColor, 2)])
    counts.append(blocks[(playerColor, 3)])
    counts.append(blocks[(playerColor, 4)])

    # Append the opponent's counts to the counts array next
    # to make sure they are assigned negative weights
    counts.append(blocks[(opponentColor, 1)])
    counts.append(blocks[(opponentColor, 2)])
    counts.append(blocks[(opponentColor, 3)])
    counts.append(blocks[(opponentColor, 4)])

    counts = np.asarray(counts)
    # print(counts)
    # print(np.dot(weights, counts))
    # print(blocks)

    return np.dot(weights, counts)
