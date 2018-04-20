from pong import Pong
from Agents.agent import Agent

NAME = "SARSA"

class sarsa(Agent):
	def __init__(self, game=Pong(), playerNum=1):
		# super(self).__init__(game, playerNum)
		super().__init__(game, playerNum)
		self.name = NAME
		# self.playerColor = ?
		self.rewards = np.zeros((12,12,2,3,12))
		self.q_values = np.zeros((12,12,2,3,12,3))
		self.counts_Nsa = np.zeros((12,12,2,3,12,3))

		self.terminal_reward = -1
		self.terminal_count = 0
		self.terminal_q_value = 0


	"""
    The getAction function should decide the action this agent should take
    given the state of self.game.  It should return 1 if the paddle should
    move up, -1 if the paddle should move down, or 0 if the paddle should do
    nothing.
    """
	def getAction(self):
		# TODO: Implement SARSA algorithm
		pass
