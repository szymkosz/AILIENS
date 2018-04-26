from Agents.agent import Agent
import numpy as np

import sys
sys.path.append('..')
import helper

NAME = "SARSA"

class sarsa(Agent):
	#def __init__(self, game=Pong(), playerNum=1, learning_rate_constant=1.0, discount_factor=.70):
	def __init__(self, learning_rate_constant=1.0, discount_factor=.70, exploration_threshold=3, playerNum=1):
		np.random.seed(6386)
		# super(self).__init__(game, playerNum)
		super().__init__(NAME, playerNum)
		# self.name = NAME
		# self.playerColor = ?
		# Initialize the rewards, q-values, and N(s,a) counts
		"""
		self.rewards = np.zeros((12,12,2,3,12))
		for i in range(12):
			self.rewards[11,i,1,:,i] = 1.0
		"""

		self.q_values = np.zeros((12,12,2,3,12,3))
		self.counts_Nsa = np.zeros((12,12,2,3,12,3), dtype=np.int32)

		# These three variables describe the characteristics of the terminal state,
		# where the ball has left the screen because the paddle missed it.
		"""
		self.terminal_reward = -1
		self.terminal_count = 0
		"""
		self.terminal_q_value = -1

		self.cur_action = np.random.randint(3)

		self.learning_rate_constant = learning_rate_constant
		self.discount_factor = discount_factor
		self.exploration_threshold = exploration_threshold


	"""
    The updateAction function should decide the action this agent should take
    given the state of self.game.  It should return 1 if the paddle should
    move up, -1 if the paddle should move down, or 0 if the paddle should do
    nothing.
    """
	def getAction(self, is_training, cur_state_tuple):
		discrete_state = helper.get_discrete_state(cur_state_tuple)
		assert discrete_state is not -1, "ERROR: discrete_state should not be a terminal state!"

		action = None
		if is_training:
			# If the SARSA agent is being trained, then its next action
			# a = self.cur_action.
			action = self.cur_action
		else:
			# This is how actions are determined outside of training.  The action
			# is computed as argmax(Q(s,a')) over all actions a'.
			q_values = self.q_values[list(discrete_state)]
			action = np.argmax(q_values)

		return action


	"""
    The updateAction function is largely responsible for the agent's learning.
    It updates the agent's parameters given the state s, the action a taken in
    state s, the resulting state s_prime (s'), whether or not s is the terminal state,
    and whether or not s' is the terminal state.  It computes the reward r,
    the action a' to take from state s', and performs the TD update as appropriate.

    Nothing is returned.
    """
	def updateAction(self, s, a, reward, s_prime):
		# TODO: Implement SARSA algorithm
		"""
		1. s, a, and s' are already given as parameters.  s and s' are 5-tuples
		   containing all 5 attributes of the game state, and a is a number (0, 1, or 2).
		2. Acquire the reward R(s)
		3. Select the action a' to take in state s' as
		   a' = argmax{over actions a' from s'}(f(Q(s',a'), N(s',a')) )
		4. Perform the TD update (See lecture slides)
		5. Store a' as a for the next time step:
		   a <- a'
		"""

		# Convert the state tuples from continuous to discrete
		d_s = helper.get_discrete_state(s)
		assert d_s is not -1, "ERROR: d_s should not be a terminal state!"
		d_s_prime = helper.get_discrete_state(s_prime)

		# Determine Q(s',a') for the TD update
		a_prime = None
		Q_s_prime_a_prime = None
		if d_s_prime == -1:
			# If s' is the terminal state, then Q(s',a') = self.terminal_q_value = -1
			Q_s_prime_a_prime = self.terminal_q_value
		else:
			# Since s' isn't the terminal state, determine the next action a' to take in state
			# s' as argmax{over a'}( helper.exploration_function(Q(s',a'), N(s',a')) )
			q_vals = self.q_values[list(d_s_prime)]
			counts = self.counts_Nsa[list(d_s_prime)]

			a_prime = np.argmax(helper.exploration_function(q_vals, counts, self.exploration_threshold))
			Q_s_prime_a_prime = self.q_values[list(d_s_prime)][a_prime]

		# Perform the TD update
		alpha = self.learning_rate_constant/(self.learning_rate_constant + self.counts_Nsa[list(d_s)][a])
		Q_sa = self.q_values[list(d_s)][a]
		self.q_values[list(d_s)][a] = Q_sa + alpha * (reward + self.discount_factor*Q_s_prime_a_prime - Q_sa)

		# If s' is the terminal state, pick a random action to start off the next game.
		# Otherwise, store the computed a' as a for the next time step.
		if a_prime is None:
			self.cur_action = np.random.randint(3)
		else:
			self.cur_action = a_prime

		"""
		# Acquire the reward R(s)
		Rs = self.rewards[list(s)]
		"""
		"""
		# Select the next action to take in state s'
		q_vals = self.q_values[list(d_s_prime)]
		counts = self.counts_Nsa[list(d_s_prime)]
		a_prime = np.argmax(helper.exploration_function(q_vals, counts, self.exploration_threshold))

		# Perform the TD update
		alpha = self.learning_rate_constant/(self.learning_rate_constant + self.counts_Nsa[list(d_s)][a])
		Qsa = self.q_values[list(d_s)][a]
		self.q_values[list(d_s)][a] = Qsa + alpha * (Rs + self.discount_factor*self.q_values[list(d_s_prime)][a_prime] - Qsa)

		# Store a' as a
		self.cur_action = a_prime
		"""
