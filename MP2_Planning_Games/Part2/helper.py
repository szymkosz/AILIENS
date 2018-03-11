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

# @param playerColor    The color of the agent calling this function.
#                       This parameter can either be the string "RED" for
#                       the red player or "BLUE" for the blue player.
#                       Otherwise, a ValueError is raised.
# @param patterns       A tuple of three dictionaries representing counts,
#                       the endpoints of chains of stones, and moves to
#                       complete these chains
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

    patternCount = patterns[0]
    patternStartingPos = patterns[1]
    patternMovesToComplete = patterns[2]
    # TODO: Verify these checks for guaranteed wins and losses are correct

    # If this board layout has a chain of 4 stones of the opponent's color,
    # it is treated as an automatic loss and negative infinity is returned.
    numOpponentChainsOf4 = patternCount[(opponentColor, 4, True)]
    opponentChainOf4 = patternMovesToComplete[(opponentColor, 4, True)][True]

    if numOpponentChainsOf4 >=1 and len(opponentChainOf4) >= 1:
        return float("-inf")

    # If this board layout has at least 2 chains of 4 stones of the player's color
    # or at least 1 chain of 4 stones of the player's color with empty squares on both ends,
    # it is treated as an automatic win and positive infinity is returned.
    numPlayerChainsOf4 = patternCount[(playerColor, 4, True)]
    playerChainOf4 = patternMovesToComplete[(playerColor, 4, True)][True]

    if (numPlayerChainsOf4 >= 2 and len(playerChainOf4) >= 1) or \
       (numPlayerChainsOf4 == 1 and len(playerChainOf4) >= 2):
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
    print(counts)
    print(np.dot(weights, counts))
    print(blocks)

    return np.dot(weights, counts)
