class Node(object):
	def __init__(self, board, curPlayerColor, depth, MIN_OR_MAX, parent, prevMove):
		# These variables remain unchanged after initialization.
		self.board = board
		self.curPlayerColor = curPlayerColor
		self.depth = depth
		self.MIN_OR_MAX = MIN_OR_MAX
		self.parent = parent
		self.prevMove = prevMove

		# These variables will be updated as the minimax tree is built.
		self.childChoice = None
		self.children = []
		self.value = 0
		
		#buildTree(self)

def buildTree(node):
	if node.depth >= 3:
		patterns = node.board.getPatterns()
		node.value = helper.evalLayout(node.curPlayerColor, patterns)
		return

	# Initialize variables for determining whether or not the color of the next
	# stone to be placed is red, the color of the next player, whether the
	# children of the parameter Node are MIN or MAX nodes, storing the depth of the next
	# layer in the game tree, and storing a parent pointer to the parameter Node
	isSettingRed = False
	nextPlayerColor = None
	nextDepth = node.depth + 1
	nextMIN_OR_MAX = None
	nextParent = node

	# Determine whether or not the next stone to be placed is red
	# and what the color of the next player is
	if node.curPlayerColor == "RED":
		isSettingRed = True
		nextPlayerColor = "BLUE"
	elif node.curPlayerColor == "BLUE":
		isSettingRed = False
		nextPlayerColor = "RED"
	else:
		raise ValueError("curPlayerColor must be 'RED' or 'BLUE'!")

	# Determine whether the new Node is a MIN or MAX node
	if node.MIN_OR_MAX == "MIN":
		nextMIN_OR_MAX = "MAX"
	elif node.MIN_OR_MAX == "MAX":
		nextMIN_OR_MAX = "MIN"
	else:
		raise ValueError("MIN_OR_MAX must be 'MIN' or 'MAX'!")

	# Loop over all squares in the current board to consider
	# all the possibilities for the next move
	for i in range(len(node.board.board)):
		for j in range(node.board.board[0]):
			if node.board.board[i][j].color is None:
				# Set the stone in this square to set up the board for evaluating
				# the children of the newly created node
				node.board.setPiece(j, i, isSettingRed)

				# Add the move to the list of previous moves for storing it in the new Node
				nextPrevMove = (j, i)

				# Create the child Node, add it to the parameter's list of child Nodes,
				# and recurse on it to build its subtree
				child = Node(node.board, nextPlayerColor, nextDepth, nextMIN_OR_MAX, nextParent, nextPrevMove)
				node.children.append(child)
				BuildTree(child)

				# Remove the stone from this square to reset the board for
				# considering other empty squares to place a stone in
				node.board.unsetPiece()

	# Initialize a variable that identifies whether the value of the parameter Node
	# should be the minimum or maximum value among its children and a variable to
	# store that value
	candidateValue = None
	isMax = False
	if node.MIN_OR_MAX == "MIN":
		candidateValue = float("inf")
		isMax = False
	elif node.MIN_OR_MAX == "MAX":
		candidateValue = float("-inf")
		isMax = True
	else:
		raise ValueError("MIN_OR_MAX must be 'MIN' or 'MAX'!")

	# Loop over all the children Nodes and identify the child with either
	# the minimum or maximum value accordingly and store that value in the
	# parameter Node
	for child in node.children:
		if isMax and child.value >= candidateValue:
			candidateValue = child.value
			node.value = candidateValue
			node.childChoice = child
		elif (not isMax) and child.value <= candidateValue:
			candidateValue = child.value
			node.value = candidateValue
			node.childChoice = child

"""
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

"""
