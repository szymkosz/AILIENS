from pong import Pong
from Agents.agent import Agent

NAME = "Q-LEARNING"

class q_learning(Agent):
	def __init__(self, game=Pong(), playerNum=1):
		# super(self).__init__(game, playerNum)
		super().__init__(game, playerNum)
		self.name = NAME
		# self.playerColor = ?


	"""
    The getAction function should decide the action this agent should take
    given the state of self.game.  It should return 1 if the paddle should
    move up, -1 if the paddle should move down, or 0 if the paddle should do
    nothing.
    """
	def getAction(self):
		# TODO: Implement Q-Learning algorithm
        pass
