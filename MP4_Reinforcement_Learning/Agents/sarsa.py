from pong import Pong
from Agents.agent import Agent

NAME = "SARSA"

class sarsa(Agent):
	def __init__(self, game=Pong(), playerNum=1, learning_rate_constant=1.0, discount_factor=.70):
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

		self.learning_rate_constant = learning_rate_constant
		self.discount_factor = discount_factor


	"""
    The getAction function should decide the action this agent should take
    given the state of self.game.  It should return 1 if the paddle should
    move up, -1 if the paddle should move down, or 0 if the paddle should do
    nothing.
    """
	def getAction(self):
		# TODO: Implement SARSA algorithm
		"""
		1. If this is the first time step of the game, identify the current state
		   and pick an action at random.  Otherwise, reuse the computed next state s'
		   and next action a' from the last time step as s and a respectively.
		2. Observe the reward R(s) and the next state s' that follows from s and a
		3. Select the action a' to take in state s' as
		   a' = argmax{over actions a' from s'}(f(Q(s',a'), N(s',a')) )
		4. Perform the TD update (See lecture slides)
		5. Store s' and a' as s and a respectively for the next time step:
		   s <- s'
		   a <- a'
		"""
		pass
