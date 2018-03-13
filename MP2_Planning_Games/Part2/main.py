"""
------------------------------------------------------------------------------
This file is for running the different agent match-ups.

To run a particular match-up for part 2.2,
run the following command:

python main_part2.py <agent1> <agent2>

where:

<agent1> = "alpha-beta" or "ab" for the alpha-beta agent
          : "minimax" or "mm" for the minimax agent
          : "reflex" or "r" for the reflex agent
          : "human" or "h" for a human agent (for extra credit)
<agent2> = "alpha-beta" or "ab" for the alpha-beta agent
          : "minimax" or "mm" for the minimax agent
          : "reflex" or "r" for the reflex agent
          : "human" or "h" for a human agent (for extra credit)
-------------------------------------------------------------------------------
"""


from gomoku import Gomoku

import time, sys
from Agents.agent import Agent
from Agents.alphabeta import AlphaBeta
from Agents.minimax import MiniMax
from Agents.reflex import Reflex
from Agents.human import Human
import helper
import gui

game = Gomoku()

if __name__ == "__main__":

    incorrectUsageError = "Incorrect Usage: Expected " \
                        + "\"python %s <agent1> <agent2>\"" % sys.argv[0]

    assert len(sys.argv) == 3, incorrectUsageError

    # Agent 1
    if sys.argv[1] == "alpha-beta" or sys.argv[1] == "ab":
        Jon = AlphaBeta(game, 1)
    elif sys.argv[1] == "minimax" or sys.argv[1] == "mm":
        Jon = MiniMax(game, 1)
    elif sys.argv[1] == "reflex" or sys.argv[1] == "r":
        Jon = Reflex(game, 1)
    elif sys.argv[1] == "human" or sys.argv[1] == "h":
        Jon = Human(game, 1)
    else:
        sys.exit("AgentNotFoundError: Is the agent name spelled correctly?")

    # Agent 2
    if sys.argv[2] == "alpha-beta" or sys.argv[2] == "ab":
        Jess = AlphaBeta(game, 2)
    elif sys.argv[2] == "minimax" or sys.argv[2] == "mm":
        Jess = MiniMax(game, 2)
    elif sys.argv[2] == "reflex" or sys.argv[2] == "r":
        Jess = Reflex(game, 2)
    elif sys.argv[2] == "human" or sys.argv[2] == "h":
        Jess = Human(game, 2)
    else:
        sys.exit("AgentNotFoundError: Is the agent name spelled correctly?")


if sys.argv[1] == "human" or sys.argv[1] == "h" or sys.argv[2] == "human" or sys.argv[2] == "h":
    exec('gui.py')

else:

    # print(game)
    # win = False
    # for i in range(0, 10):
    #     if(game.reds_turn):
    #         Jon.makeMove()
    #     else:
    #         Jess.makeMove()
    #     print(game)
    # Jess.makeMove()
    print(game)
    win = None
    while win is None:
        if(game.reds_turn):
            Jon.makeMove()
        else:
            Jess.makeMove()
        print(game)
        print(game.movesTaken)
        win = game.winOrDraw()

    print(game)


# moves = [(6, 4), (6, 2), (5, 5), (5, 4), (5, 6), (5, 3), (5, 2), (5, 1), (4, 6), (6, 6), (4, 5), (6, 5), (4, 4), (5, 0), (4, 3), (4, 2), (6, 0), (4, 1), (6, 1), (3, 5), (4, 0), (3, 6), (3, 4)]


# a = []
# print("a ", a)
# a.append((1,2))
# a.append((3,1))
# a.append((5,7))
# print("a ", a)
# print("popped ", a.pop(-1))
# print("a ", a)


# raise ValueError()
"""
moves = [(3, 4), (3, 3), (1, 2), (4, 3), (5, 3), (2, 2), (2,3), (1,1),
        (3,5), (5,4),(3,2),(1,0),(6,5),(6,4),(0,6),(1,5)]
"""
"""moves = [(0,6), (0,5), (1,6), (1,5), (2,6), (2,5), (3,6), (3,5),
         (0,4), (0,3), (1,4), (1,3), (2,4), (2,3), (3,4), (3,3)]"""

# Random Moves
"""for m in moves:
    game.setPiece(m[0], m[1], game.reds_turn)"""
"""
# print(game)
# print("Moves taken: ", game.movesTaken)
# print("\n\n\tSet")
# game.setPiece(5,5, game.reds_turn)
# print(game)
# print("Moves taken: ", game.movesTaken)
# print("\n\n\tunSet")
# game.unsetPiece()
# game.unsetPiece()
# game.unsetPiece()
# print(game)
# print("Moves taken: ", game.movesTaken)
# print("\n\n\tSet")
# game.setPiece(4,4,  game.reds_turn)
game.setPiece(5,0, game.reds_turn)
game.setPiece(6,6, game.reds_turn)
game.setPiece(4,0, game.reds_turn)
game.setPiece(6,3, game.reds_turn)
game.setPiece(6,0, game.reds_turn)
# print(game.board[4][4])
# game.setPiece(4,1, game.reds_turn)
# print(game)
# print("Moves taken: ", game.movesTaken)
# print("\n\n\tunset")
# game.unsetPiece()
# print(game)
# print("Moves taken: ", game.movesTaken)
"""

"""print(game)


directions = [(1,0),(0,1),(1,-1),(1,1)]"""

# def outOfBounds(pos):
#   return pos[0] < 0 or pos[0] >= game.dim or pos[1] < 0 or pos[1] >= game.dim
#
# def nextPosition(pos, direction, reverse=False, length=1):
#   if reverse:
#       nextPos = (pos[0] - length * direction[0], pos[1] - length * direction[1])
#   else:
#       nextPos = (pos[0] + length * direction[0], pos[1] + length * direction[1])
#   return nextPos if not outOfBounds(nextPos) else None

# print(nextPosition((2,2),(1,0),reverse=True, length=2))
"""patterns = game.getPatterns()

blocks = helper.findBlocks(game)"""

"""
reflex = Reflex(game, 2)

print(reflex.player)
# print(reflex.playerNum)
print(reflex.getMove())
# print(game.movesTaken)
# reflex.makeMove()
print(game)
"""

"""print ("\n\nFIRST DICTIONARY\n\n")
for pattern in patterns[0]:
    print(pattern, patterns[0][pattern])
print ("\n\nSECOND DICTIONARY\n\n")
for pattern in patterns[1]:
    print(pattern, patterns[1][pattern])
print ("\n\nTHIRD DICTIONARY\n\n")
for pattern in patterns[2]:
    print(pattern, patterns[2][pattern])"""
# for direction in directions:
#   print(nextPosition(game,(3,4),direction))

# print(sys.path)

"""
THE FOLLOWING CODE IS A SIMPLE TEST OF THE GENERAL ALPHA-BETA PRUNING
AND MINIMAX ALGORITHMS!
"""

# import tree

"""
class Node(object):
    def __init__(self, board, curPlayerColor, depth, MIN_OR_MAX, prevMove):
        # These variables remain unchanged after initialization.
        self.board = board
        self.curPlayerColor = curPlayerColor
        self.depth = depth
        self.MIN_OR_MAX = MIN_OR_MAX
        self.prevMove = prevMove

        # These variables will be updated as the minimax tree is built.
        self.childChoice = None
        self.children = []
        self.value = 0
"""

# rootDepth = 1
# root = tree.Node(game, "RED", rootDepth, "MAX", None)
#
# for i in range(3):
# 	root.children.append(tree.Node(game, "BLUE", rootDepth+1, "MIN", (rootDepth+1, i)))
#
# 	if i == 0:
# 		root.children[i].children.append(tree.Node("game", "RED", rootDepth+2, "MAX", (rootDepth+2, 0)))
# 		root.children[i].children[0].value = float("-inf")
# 		root.children[i].children.append(tree.Node("game", "RED", rootDepth+2, "MAX", (rootDepth+2, 1)))
# 		root.children[i].children[1].value = float("-inf")
# 		root.children[i].children.append(tree.Node("game", "RED", rootDepth+2, "MAX", (rootDepth+2, 2)))
# 		root.children[i].children[2].value = float("-inf")
# 	elif i == 1:
# 		root.children[i].children.append(tree.Node("game", "RED", rootDepth+2, "MAX", (rootDepth+2, 3)))
# 		root.children[i].children[0].value = float("-inf")
# 		root.children[i].children.append(tree.Node("game", "RED", rootDepth+2, "MAX", (rootDepth+2, 4)))
# 		root.children[i].children[1].value = float("-inf")
# 		root.children[i].children.append(tree.Node("game", "RED", rootDepth+2, "MAX", (rootDepth+2, 5)))
# 		root.children[i].children[2].value = float("-inf")
# 	elif i == 2:
# 		root.children[i].children.append(tree.Node("game", "RED", rootDepth+2, "MAX", (rootDepth+2, 6)))
# 		root.children[i].children[0].value = float("-inf")
# 		root.children[i].children.append(tree.Node("game", "RED", rootDepth+2, "MAX", (rootDepth+2, 7)))
# 		root.children[i].children[1].value = float("-inf")
# 		root.children[i].children.append(tree.Node("game", "RED", rootDepth+2, "MAX", (rootDepth+2, 8)))
# 		root.children[i].children[2].value = float("-inf")
#
# tree.printTree(root)
#
# tree.loopOverChildren(root)
#
# print("")
# print("")
# print("FINISHED LOOP OVER CHILDREN!")
# print("")
#
# tree.printTree(root)


"""
RUN THE FOLLOWING CODE TO TEST THE EVALUATION FUNCTION
AFTER SETTING UP THE BOARD!
"""
#patterns = game.getPatterns()

#blocks = helper.findBlocks(game)"""

#print("")
#print("Evaluation cost: " + str(helper.evalLayout("RED", patterns, blocks)))
