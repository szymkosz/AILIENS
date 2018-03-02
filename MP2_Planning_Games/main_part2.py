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
<<<<<<< HEAD
=======
import time
import agents

# game = Gomoku()

# print(game)

if __name__ == "__main__":

    incorrectUsageError = "Incorrect Usage: Expected " \
                        + "\"python %s <agent1> <agent2>\"" % sys.argv[0]

    assert len(sys.argv) == 3, incorrectUsageError

    # Agent 1
	if sys.argv[1] == "alpha-beta" or sys.argv[1] == "ab":
		red = 
	elif sys.argv[1] == "minimax" or sys.argv[1] == "mm":
		red = 
	elif sys.argv[1] == "reflex" or sys.argv[1] == "r":  
		red = 
	# elif sys.argv[1] == "human" or sys.argv[1] == "h":
	# 	red = 
	else:
		sys.exit("AgentNotFoundError: Is the agent name spelled correctly?")
>>>>>>> cf2500490fc7a4434e3e13ab97cf38271f223610

	# Agent 2
	if sys.argv[2] == "alpha-beta" or sys.argv[2] == "ab":
		blue = 
	elif sys.argv[2] == "minimax" or sys.argv[2] == "mm":
		blue = 
	elif sys.argv[2] == "reflex" or sys.argv[2] == "r": 	  
		blue = 
	# elif sys.argv[2] == "human" or sys.argv[2] == "h":
	# 	blue = 
	else:
		sys.exit("AgentNotFoundError: Is the agent name spelled correctly?")

	# Run the Gomoku game with the specified agents
	# How should I do this...?

moves = [(3, 4), (3, 3), (4, 5), (4, 3), (5, 3)]

# Random Moves
<<<<<<< HEAD
for m in moves:
    game.setPiece(m[0], m[1], game.reds_turn)

game.setPiece(5,5, game.reds_turn)

# game.setPiece(4,4,not game.reds_turn)
=======
# game.setPiece(3,4,1)
# game.setPiece(3,3,0)
# game.setPiece(4,5,1)
# game.setPiece(4,3,0)
# game.setPiece(5,3,1)
>>>>>>> cf2500490fc7a4434e3e13ab97cf38271f223610

# print(game)
