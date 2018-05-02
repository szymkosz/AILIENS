NAME = "AGENT"
import numpy as np

class Agent(object):
	def __init__(self, name=NAME, playerNum=1):
		self.name = name
		self.playerNum = playerNum
		# self.playerColor = ?
		self.q_values = None
		self.counts_Nsa = None

		self.learning_rate_constant = None
		self.discount_factor = None
		self.exploration_threshold = None

		self.num_training_games = None


	"""
	The getAction function should decide the action this agent should take
	given the current state s of the game.  It should return 0 if the paddle
	should move up, 2 if the paddle should move down, or 1 if the paddle should
	do nothing.
	"""
	def getAction(self, is_training, cur_state_tuple):
		raise NotImplementedError()


	"""
	The updateAction function is largely responsible for the agent's learning.
	It updates the agent's parameters given the state s, the action a taken in
	state s, the reward of taking action a in state s, and the resulting state
	s_prime (s').  It computes the action a' to take from state s' and performs
	the TD update as appropriate.

	Nothing is returned.
	"""
	def updateAction(self, s, a, reward, s_prime):
		raise NotImplementedError()

	"""
	Puts together a file name for the agent and the parameters in the format:
	<agent> <LRC> <Discount_Factor> <Exploration_Threshold>
	i.e. "Q_LEARNINING__LRC_10__Discount_0.8__ExplrThr_20__100000"
	"""
	def formulate_file_name(self):
		return str(self.name.upper()) + "__LRC_" + str(int(self.learning_rate_constant)) + \
		 "__Discount_" + str(float(self.discount_factor)) + "__ExplrThr_" + \
		 str(int(self.exploration_threshold)) + "__" + str(int(self.num_training_games))

	def load(self):
		fileName = "Agents/Training_Data/" + self.formulate_file_name() + ".npz"
		import os.path
		load = os.path.isfile(fileName)
		if load:
			ans = input("\nTraining data has been found for this agent. Load it? (y/n)  ")
			if ans.lower() == 'n' or ans.lower() == "no":
				load = False
		else:
			print("\nCould not find existing training data for this agent.")
		if load:
			data = np.load(fileName)
			self.q_values = data['q_values'].reshape((12,12,2,3,12,3))
			self.counts_Nsa = data['counts_Nsa'].reshape((12,12,2,3,12,3))
			self.learning_rate_constant = data['lrc']
			self.discount_factor = data['discount_factor']
			self.exploration_threshold = data['exploration_threshold']
			try:
				self.num_training_games = data['num_training_games']
			except:
				pass
		return load

	def save(self):
		save = False
		fileName = "Agents/Training_Data/" + self.formulate_file_name() + ".npz"
		import os.path
		if os.path.isfile(fileName):
			print("\nTraining data for this agent and these parameters already exists.")
			ans = input("Overwrite it? (y/n)  ")
			if ans.lower() == 'n' or ans.lower() == "no":
				print("Canceling save.")
				return
			else:
				save = True
		else:
			save = True
		if save:
			print("\nSaving training data...")
			np.savez(fileName, q_values=self.q_values.flatten(), counts_Nsa=self.counts_Nsa.flatten(), \
					lrc=self.learning_rate_constant, discount_factor=self.discount_factor,\
					exploration_threshold=self.exploration_threshold, num_training_games=self.num_training_games)
