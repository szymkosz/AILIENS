"""
HELPER FUNCTIONS GO IN THIS FILE!
"""

import numpy as np

weights = np.asarray([1, 2, 3, 4, -1, -2, -3, -4])

# @param playerColor    The color of the agent calling this function.
#                       This parameter can either be the string "RED" for
#                       the red player or "BLUE" for the blue player.
#                       Otherwise, a ValueError is raised.
# @param patterns       A tuple of three dictionaries representing counts,
#                       the endpoints of chains of stones, and moves to
#                       complete these chains
def evalLayout(playerColor, patterns):
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
    # TODO: Add checks for guaranteed wins and losses

    # If this board layout has a chain of 4 stones of the opponent's color,
    # it is treated as an automatic loss and negative infinity is returned.
    numOpponentChainsOf4 = patternCount[(opponentColor, 4, True)]

    if numOpponentChainsOf4 > 0:
        return float("-inf")

    numPlayerChainsOf4 = patternCount[(playerColor, 4, True)]



    if numPlayerChainsOf4 >= 2 or \
       (numPlayerChainsOf4 == 1 and \
        ):
        pass
    
    # If this point is reached, the board layout has no guaranteed wins
    # or losses for this player within the next two moves, so a linear
    # combination of weights with the numbers of patterns should be
    # computed and returned.
    counts = []

    # Append this player's counts to the counts array first
    # to make sure they are assigned positive weights
    counts.append(patternCount[(playerColor, 1, True)])
    counts.append(patternCount[(playerColor, 2, True)])
    counts.append(patternCount[(playerColor, 3, True)])
    counts.append(patternCount[(playerColor, 4, True)])

    # Append the opponent's counts to the counts array next
    # to make sure they are assigned negative weights
    counts.append(patternCount[(opponentColor, 1, True)])
    counts.append(patternCount[(opponentColor, 2, True)])
    counts.append(patternCount[(opponentColor, 3, True)])
    counts.append(patternCount[(opponentColor, 4, True)])

    counts = np.asarray(counts)

    return np.dot(weights, counts)
