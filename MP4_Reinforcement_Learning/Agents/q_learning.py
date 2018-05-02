from Agents.agent import Agent
import numpy as np

import sys
sys.path.append('..')
import helper

NAME = "Q_LEARNING"

class q_learning(Agent):
	def __init__(self, learning_rate_constant=20, discount_factor=.90, exploration_threshold=10, playerNum=1, num_training_games=100000):
		super().__init__(NAME, playerNum)

		self.q_values = np.zeros((12,12,2,3,12,3))
		self.counts_Nsa = np.zeros((12,12,2,3,12,3), dtype=np.int32)

		# This is the q-value of the terminal state (when the ball leaves the screen
		# because the paddle misses it).  It is fixed at -1 to help the training converge.
		self.terminal_q_value = -1

		# These are the 3 training parameters that are varied for experimentation purposes.
		self.learning_rate_constant = learning_rate_constant
		self.discount_factor = discount_factor
		self.exploration_threshold = exploration_threshold

		self.num_training_games = num_training_games

	"""
	The getAction function should decide the action this agent should take
	given the current state s of the game.  It should return 0 if the paddle
	should move up, 2 if the paddle should move down, or 1 if the paddle should
	do nothing.
	"""
	def getAction(self, is_training, cur_state_tuple):
		discrete_state = helper.get_discrete_state(cur_state_tuple)
		assert discrete_state is not -1, "ERROR: discrete_state should not be a terminal state!"

		action = None
		q_values = self.q_values[discrete_state[0]][discrete_state[1]][discrete_state[2]][discrete_state[3]][discrete_state[4]]
		if is_training:
			# If the Q-learning agent is being trained, then its next action
			# a = argmax{over all actions a'}( f(Q(s,a'), N(s,a')) ).
			counts_Nsa = self.counts_Nsa[discrete_state[0]][discrete_state[1]][discrete_state[2]][discrete_state[3]][discrete_state[4]]

			action = np.argmax(helper.exploration_function(q_values, counts_Nsa, self.exploration_threshold))
			self.counts_Nsa[discrete_state[0]][discrete_state[1]][discrete_state[2]][discrete_state[3]][discrete_state[4]][action] += 1
		else:
			# This is how actions are determined outside of training.  The action
			# is computed as argmax(Q(s,a')) over all actions a'.
			action = np.argmax(q_values)

		return action


	"""
	The updateAction function is largely responsible for the agent's learning.
	It updates the agent's parameters given the state s, the action a taken in
	state s, the reward of taking action a in state s, and the resulting state
	s_prime (s').  It computes the action a' to take from state s' and performs
	the TD update as appropriate.

	Nothing is returned.
	"""
	def updateAction(self, s, a, reward, s_prime):
		"""
		1. s, a, reward (r), and s' are already given as parameters.  s and s' are 5-tuples
		   containing all 5 attributes of the game state, a is a number (0, 1, or 2),
		   and reward is the reward of taking action a in state s (-1, 0, or 1).
		2. If s' is the terminal state, max(Q(s',a')) for any action a' = self.terminal_q_value = -1.

		   Otherwise, compute max(Q(s',a')) over all actions a'.
		3. Perform the TD update (See lecture slides)
		"""
		# Convert the state tuples from continuous to discrete
		d_s = helper.get_discrete_state(s)
		assert d_s is not -1, "ERROR: d_s should not be a terminal state!"
		d_s_prime = helper.get_discrete_state(s_prime)

		# Determine max(Q(s',a')) over all actions a' for the TD update
		maxQ_s_prime_a_prime = None
		if d_s_prime == -1:
			# If s' is the terminal state, then max(Q(s',a')) for any action a' = self.terminal_q_value = -1
			maxQ_s_prime_a_prime = self.terminal_q_value
		else:
			# Since s' isn't the terminal state, compute max(Q(s',a')) over all actions a'
			q_values = self.q_values[d_s_prime[0]][d_s_prime[1]][d_s_prime[2]][d_s_prime[3]][d_s_prime[4]]
			maxQ_s_prime_a_prime = np.amax(q_values)

		# Perform the TD update
		alpha = self.learning_rate_constant/(self.learning_rate_constant + self.counts_Nsa[d_s[0]][d_s[1]][d_s[2]][d_s[3]][d_s[4]][a])
		Q_sa = self.q_values[d_s[0]][d_s[1]][d_s[2]][d_s[3]][d_s[4]][a]
		self.q_values[d_s[0]][d_s[1]][d_s[2]][d_s[3]][d_s[4]][a] = Q_sa + alpha * (reward + self.discount_factor*maxQ_s_prime_a_prime - Q_sa)
