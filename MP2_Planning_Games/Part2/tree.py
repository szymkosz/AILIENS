import helper

class Node(object):
    def __init__(self, board, curPlayerColor, depth, MIN_OR_MAX, prevMove):
        # These variables remain unchanged after initialization.
        self.board = board
        self.curPlayerColor = curPlayerColor
        self.depth = depth
        self.MIN_OR_MAX = MIN_OR_MAX
        self.prevMove = prevMove

        # These variables will be updated as the minimax tree is built.
        self.childChoice = None
        self.children = []
        self.value = 0


"""
## This function identifies the color of the player at the root Node given
#  an arbitrary node in the tree.  This is important for identifying if a
#  chain of 5 stones is a win or loss for the original player at the root Node.
#
#  The color of the root Node is returned as either "RED" or "BLUE".
def determineRootColor(node):
    if node.curPlayerColor == "BLUE":
        if node.depth % 2 == 0:
            return "BLUE"
        else:
            return "RED"
    elif node.curPlayerColor == "RED":
        if node.depth % 2 == 0:
            return "RED"
        else:
            return "BLUE"
    else:
        raise ValueError("curPlayerColor must be 'RED' or 'BLUE'!")
"""


def buildTree(agent, node, alpha=float("-inf"), beta=float("inf")):
    # Increment the agent's expanded Node counter
    agent.expandedNodes += 1

    # Before building the children, the current board layout is
    # checked for a win (a chain of 5 stones) for either player or a draw.
    boardState = node.board.winOrDraw()
    rootColor = agent.player

    # If the current board layout is a win or a draw, no subtree should be built.
    # Instead, the appropriate value should be assigned to the parameter Node.
    if boardState is not None:
        # If the current board layout is a draw, the parameter Node's value is 0.
        if boardState == "DRAW":
            node.value = 0
            return
        elif boardState == "BLUE" or boardState == "RED":
            # If the color of this tree's root Node matches the color of the
            # chain of 5 stones, the parameter Node's value should be set to
            # positive infinity to represent a win for the original player.
            # Otherwise, it should be set to negative infinity to represent a
            # loss for the original player.
            if rootColor == boardState:
                node.value = float("inf")
                return
            else:
                node.value = float("-inf")
                return
        else:
            raise ValueError("The winOrDraw function isn't returning a correct value.")

    # If this is level 3, call the evaluation function to set the
    # parameter Node's value and return.
    if node.depth >= 3:
        patterns = node.board.getPatterns()
        blocks = helper.findBlocks(node.board)
        node.value = helper.evalLayout(rootColor, patterns, blocks)
        return

    # Initialize variables for determining whether or not the color of the next
    # stone to be placed is red, the color of the next player, whether the
    # children of the parameter Node are MIN or MAX nodes, storing the depth of the next
    # layer in the game tree, and storing a parent pointer to the parameter Node
    isSettingRed = False
    nextPlayerColor = None
    nextDepth = node.depth + 1
    nextMIN_OR_MAX = None

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

    # Loop over all squares in the current board to consider
    # all the possibilities for the next move
    for x in range(node.board.dim):
        for y in range(node.board.dim):
            if node.board.board[x][y].char == '.':
                # Set the stone in this square to set up the board for evaluating
                # the children of the newly created node
                node.board.setPiece(x, y, isSettingRed)

                # Add the move to the list of previous moves for storing it in the new Node
                nextPrevMove = (x, y)

                # Create the child Node, add it to the parameter's list of child Nodes,
                # and recurse on it to build its subtree

                #child = Node(node.board, nextPlayerColor, nextDepth, nextMIN_OR_MAX, nextParent, nextPrevMove)
                child = Node(node.board, nextPlayerColor, nextDepth, nextMIN_OR_MAX, nextPrevMove)
                node.children.append(child)
                buildTree(agent, child, alpha, beta)

                # Remove the stone from this square to reset the board for
                # considering other empty squares to place a stone in
                node.board.unsetPiece()

                # Update the parameter Node's value and move choice if appropriate
                # (If the parameter Node is a MAX node and the child's value is greater
                # than or equal to the canddidate value or a MIN node and the child's
                # value is less than or equal to the candidate value)
                if (isMax and child.value >= candidateValue) or\
                   ((not isMax) and child.value <= candidateValue):
                    candidateValue = child.value
                    node.value = candidateValue
                    node.childChoice = child

                    # If the agent is an alpha-beta agent, prune the
                    # parameter Node if appropriate
                    if agent.name == "ALPHA_BETA":
                        if isMax:
                            # If the parameter Node is a MAX node and its new value is
                            # greater than or equal to beta, prune it.  Otherwise,
                            # update alpha if the new value is greater than alpha.
                            if node.value >= beta:
                                return
                            elif node.value > alpha:
                                alpha = node.value
                        else:
                           # If the parameter Node is a MIN node and its new value is
                           # less than or equal to alpha, prune it.  Otherwise,
                           # update beta if the new value is less than beta.
                           if node.value <= alpha:
                               return
                           elif node.value < beta:
                               beta = node.value

    """
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
