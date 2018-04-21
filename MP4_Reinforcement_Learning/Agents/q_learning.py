from Agents.agent import Agent
import numpy as np
import helper

NAME = "Q-LEARNING"

class q_learning(Agent):
	#def __init__(self, game=Pong(), playerNum=1, learning_rate_constant=1.0, discount_factor=.70):
	def __init__(self, learning_rate_constant=1.0, discount_factor=.70, exploration_threshold=3, playerNum=1):
		# super(self).__init__(game, playerNum)
		super().__init__(NAME, playerNum)
		# self.name = NAME
		# self.playerColor = ?
		# Initialize the rewards, q-values, and N(s,a) counts
		self.rewards = np.zeros((12,12,2,3,12))
		for i in range(12):
			self.rewards[11][i][1][:][i] = 1.0

		self.q_values = np.zeros((12,12,2,3,12,3))
		self.counts_Nsa = np.zeros((12,12,2,3,12,3), dtype=np.int32)

		# These three variables describe the characteristics of the terminal state,
		# where the ball has left the screen because the paddle missed it.
		self.terminal_reward = -1
		self.terminal_count = 0
		self.terminal_q_value = 0

		self.learning_rate_constant = learning_rate_constant
		self.discount_factor = discount_factor
		self.exploration_threshold = exploration_threshold


	"""
    The getAction function should decide the action this agent should take
    given the state of self.game.  It should return 1 if the paddle should
    move up, -1 if the paddle should move down, or 0 if the paddle should do
    nothing.
    """
	def getAction(self, is_training, cur_state_tuple):
		discrete_state = helper.get_discrete_state(cur_state_tuple)

		action = None
		q_values = self.q_values[discrete_state[0]][discrete_state[1]][discrete_state[2]][discrete_state[3]][discrete_state[4]][:]
		if is_training:
			# If the Q-learning agent is being trained, then its next action
			# a = argmax{over all actions a'}( f(Q(s,a'), N(s,a')) ).
			counts_Nsa = self.counts_Nsa[discrete_state[0]][discrete_state[1]][discrete_state[2]][discrete_state[3]][discrete_state[4]][:]
			action = np.argmax(helper.exploration_function(q_values, counts_Nsa, self.exploration_threshold)) - 1
		else:
			# This is how actions are determined outside of training.  The action
			# is computed as argmax(Q(s,a')) over all actions a'.
			action = np.argmax(q_values) - 1

		return action


	"""
    The updateAction function is largely responsible for the agent's learning.
    It updates the agent's parameters given the state s, the action a taken in
    state s, and the resulting state s_prime (s').  It computes the reward r,
    the action a' to take from state s', and performs the TD update.

    Nothing is returned.
    """
	def updateAction(self, s, a, s_prime):
		# TODO: Implement Q-Learning algorithm
		"""
		1. s, a, and s' are already given as parameters.  s and s' are 5-tuples
		   containing all 5 attributes of the game state, and a is a number (-1,0, or 1).
		2. Acquire the reward R(s)
		3. Perform the TD update (See lecture slides)
		"""
		pass
