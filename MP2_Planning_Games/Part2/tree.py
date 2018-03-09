from sys import maxsize

class Node(object):
	def __init__(self, depth, playerNum, numStones, value = 0):
		self.depth = depth
		self.playerNum = playerNum
		self.value = value
		self.numStones = numStones # ?????
		self.children = []
		self.createChildren()

	def createChildren(self):
		if self.depth >= 0:
			for i in range(1, 3):
				??
			self.children.append(Node(self.depth-1, -playerNum, ???, calcValue(Node)))


	def calcValue(self, value):
		# use linearly weighted algorithm to calculate the weight of each node

