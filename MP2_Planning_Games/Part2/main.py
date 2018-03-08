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

game = Gomoku()

# a = Agent().getMoves()

print(game)

# if __name__ == "__main__":
#
#     incorrectUsageError = "Incorrect Usage: Expected " \
#                         + "\"python %s <agent1> <agent2>\"" % sys.argv[0]
#
#     assert len(sys.argv) == 3, incorrectUsageError
#
#     # Agent 1
# 	if sys.argv[1] == "alpha-beta" or sys.argv[1] == "ab":
# 		gomoku.players[0]
# 	elif sys.argv[1] == "minimax" or sys.argv[1] == "mm":
# 		red =
# 	elif sys.argv[1] == "reflex" or sys.argv[1] == "r":
# 		red =
# 	# elif sys.argv[1] == "human" or sys.argv[1] == "h":
# 	# 	red =
# 	else:
# 		sys.exit("AgentNotFoundError: Is the agent name spelled correctly?")
#
# 	# Agent 2
# 	if sys.argv[2] == "alpha-beta" or sys.argv[2] == "ab":
# 		blue =
# 	elif sys.argv[2] == "minimax" or sys.argv[2] == "mm":
# 		blue =
# 	elif sys.argv[2] == "reflex" or sys.argv[2] == "r":
# 		blue =
# 	# elif sys.argv[2] == "human" or sys.argv[2] == "h":
# 	# 	blue =
# 	else:
# 		sys.exit("AgentNotFoundError: Is the agent name spelled correctly?")

	# Run the Gomoku game with the specified agents
	# How should I do this...?

moves = [(3, 4), (3, 3), (1, 2), (4, 3), (5, 3), (2, 2), (2,3), (1,1),
		(3,5), (5,4),(3,2),(0,0),(6,5),(6,4),(0,6),(1,5)]

# Random Moves
for m in moves:
    game.setPiece(m[0], m[1], game.reds_turn)

game.setPiece(5,5, game.reds_turn)

game.setPiece(4,4, game.reds_turn)

print(game)

directions = [(1,0),(0,1),(1,-1),(1,1)]

def outOfBounds(pos):
	return pos[0] < 0 or pos[0] >= game.dim or pos[1] < 0 or pos[1] >= game.dim

def nextPosition(pos, direction, reverse=False, length=1):
	if reverse:
		nextPos = (pos[0] - length * direction[0], pos[1] - length * direction[1])
	else:
		nextPos = (pos[0] + length * direction[0], pos[1] + length * direction[1])
	return nextPos if not outOfBounds(nextPos) else None

# print(nextPosition((2,2),(1,0),reverse=True, length=2))
patterns = game.getPatterns()

print ("\n\nFIRST DICTIONARY\n\n")
for pattern in patterns[0]:
	print(pattern, patterns[0][pattern])
# print ("\n\nSECOND DICTIONARY\n\n")
# for pattern in patterns[1]:
# 	print(pattern, patterns[1][pattern])
# print ("\n\nTHIRD DICTIONARY\n\n")
# for pattern in patterns[2]:
# 	print(pattern, patterns[2][pattern])
# for direction in directions:
# 	print(nextPosition(game,(3,4),direction))

# print(sys.path)
