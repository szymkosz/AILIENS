from Agents.agent import Agent
import numpy as np

import sys
sys.path.append('..')
import helper

NAME = "SARSA"

class sarsa(Agent):
	def __init__(self, learning_rate_constant=1.0, discount_factor=.70, exploration_threshold=3, playerNum=1, num_training_games=100000):
		#np.random.seed(6386)
		# super(self).__init__(game, playerNum)
		super().__init__(NAME, playerNum)

		"""
		# Initialize the rewards, q-values, and N(s,a) counts

		self.rewards = np.zeros((12,12,2,3,12))
		for i in range(12):
			self.rewards[11,i,1,:,i] = 1.0
		"""
		# Initialize the q-values and N(s,a) counts

		self.q_values = np.zeros((12,12,2,3,12,3))
		self.counts_Nsa = np.zeros((12,12,2,3,12,3), dtype=np.int32)

		"""
		# These three variables describe the characteristics of the terminal state,
		# where the ball has left the screen because the paddle missed it.
		self.terminal_reward = -1
		self.terminal_count = 0
		self.terminal_q_value = 0
		"""

		# This is the q-value of the terminal state (when the ball leaves the screen
		# because the paddle misses it).  It is fixed at -1 to help the training converge.
		self.terminal_q_value = -1

		# This is the predetermined action a to use at each time step during training.
		self.cur_action = 2 # np.random.randint(3)

		# These are the 3 training parameters that are varied for experimentation purposes.
		self.learning_rate_constant = learning_rate_constant
		self.discount_factor = discount_factor
		self.exploration_threshold = exploration_threshold

		self.num_training_games = num_training_games

	# def save(self, fileName):
	# 	save = False
	# 	fileName += ".npz"
	# 	import os.path
	# 	if os.path.isfile(fileName):
	# 		print("\nTraining data for this agent and these parameters already exists.")
	# 		ans = input("Overwrite it? (y/n)  ")
	# 		if ans.lower() == 'n' or ans.lower() == "no":
	# 			print("Canceling save.")
	# 			return
	# 		else:
	# 			save = True
	# 	else:
	# 		save = True
	# 	if save:
	# 		print("\nSaving training data...")
	# 		np.savez(fileName, q_values=self.q_values.flatten(), counts_Nsa=self.counts_Nsa.flatten(), \
	# 				lrc=self.learning_rate_constant, discount_factor=self.discount_factor,\
	# 				exploration_threshold=self.exploration_threshold)
	#
	# def load(self, fileName):
	# 	fileName += ".npz"
	# 	import os.path
	# 	if os.path.isfile(fileName):
	# 		data = np.load(fileName)
	# 		self.q_values = data['q_values'].reshape((12,12,2,3,12,3))
	# 		self.counts_Nsa = data['counts_Nsa'].reshape((12,12,2,3,12,3))
	# 		self.learning_rate_constant = data['lrc']
	# 		self.discount_factor = data['discount_factor']
	# 		self.exploration_threshold = data['exploration_threshold']
	# 		return True
	# 	print("\nCould not find existing training data for this agent.")
	# 	return False


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
		if is_training:
			# If the SARSA agent is being trained, then its next action
			# a = self.cur_action.
			action = self.cur_action
			self.counts_Nsa[discrete_state[0]][discrete_state[1]][discrete_state[2]][discrete_state[3]][discrete_state[4]][action] += 1
		else:
			# This is how actions are determined outside of training.  The action
			# is computed as argmax(Q(s,a')) over all actions a'.
			q_values = self.q_values[discrete_state[0]][discrete_state[1]][discrete_state[2]][discrete_state[3]][discrete_state[4]]
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
		# TODO: Implement SARSA algorithm
		"""
		1. s, a, reward (r), and s' are already given as parameters.  s and s' are 5-tuples
		   containing all 5 attributes of the game state, a is a number (0, 1, or 2),
		   and reward is the reward of taking action a in state s (-1, 0, or 1).
		2. If s' is the terminal state, Q(s',a') = self.terminal_q_value = -1.

		   Otherwise, select the action a' to take in state s' as
		   a' = argmax{over actions a' from s'}(f(Q(s',a'), N(s',a')) )
		   then lookup Q(s',a') in the self.q_values table.
		3. Perform the TD update (See lecture slides)
		4. If s' is the terminal state, set self.cur_action = 2 to always move down initially
		   at the beginning of every game.
		   ##If s' is the terminal state, randomly set self.cur_action on the interval [0,2].

		   Otherwise, store a' as a for the next time step:
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
			q_vals = self.q_values[d_s_prime[0]][d_s_prime[1]][d_s_prime[2]][d_s_prime[3]][d_s_prime[4]]
			counts = self.counts_Nsa[d_s_prime[0]][d_s_prime[1]][d_s_prime[2]][d_s_prime[3]][d_s_prime[4]]

			a_prime = np.argmax(helper.exploration_function(q_vals, counts, self.exploration_threshold))
			Q_s_prime_a_prime = self.q_values[d_s_prime[0]][d_s_prime[1]][d_s_prime[2]][d_s_prime[3]][d_s_prime[4]][a_prime]

		# Perform the TD update
		alpha = self.learning_rate_constant/(self.learning_rate_constant + self.counts_Nsa[d_s[0]][d_s[1]][d_s[2]][d_s[3]][d_s[4]][a])
		Q_sa = self.q_values[d_s[0]][d_s[1]][d_s[2]][d_s[3]][d_s[4]][a]
		self.q_values[d_s[0]][d_s[1]][d_s[2]][d_s[3]][d_s[4]][a] = Q_sa + alpha * (reward + self.discount_factor*Q_s_prime_a_prime - Q_sa)

		# If s' is the terminal state, set self.cur_action = 2 to always move down initially
		# at the beginning of every game.
		### If s' is the terminal state, pick a random action to start off the next game.
		# Otherwise, store the computed a' as a for the next time step.
		if d_s_prime == -1:
			self.cur_action = 2 # np.random.randint(3)
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
