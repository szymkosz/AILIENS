from pong import Pong
from Agents.agent import Agent

NAME = "Q-LEARNING"

class q_learning(Agent):
	def __init__(self, game=Pong(), playerNum=1):
		# super(self).__init__(game, playerNum)
		super().__init__(game, playerNum)
		self.name = NAME
		# self.playerColor = ?
		self.rewards = np.zeros((12,12,2,3,12))

		for i in range(12):
			self.rewards[11][i][1][:][i] = 1.0

		self.q_values = np.zeros((12,12,2,3,12,3))
		self.counts_Nsa = np.zeros((12,12,2,3,12,3))

		self.terminal_reward = -1
		self.terminal_count = 0
		self.terminal_q_value = 0

		self.cur_state = (self.game.ball_x, self.game.ball_y, self.game.velocity_x,
		                  self.game.velocity_y, self.game.paddle_y)
		self.cur_action = 1


	"""
    The getAction function should decide the action this agent should take
    given the state of self.game.  It should return 1 if the paddle should
    move up, -1 if the paddle should move down, or 0 if the paddle should do
    nothing.
    """
	def getAction(self):
		# TODO: Implement Q-Learning algorithm
		pass
