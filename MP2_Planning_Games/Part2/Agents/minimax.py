from gomoku import Gomoku
from position import Position
from agent import Agent
from sys import maxsize

#from tree import Node
import tree

class MiniMax(Agent):
    def __init__(self, game=Gomoku(), playerNum=1):
        super().__init__(game, playerNum)
        self.name = "MINIMAX"
        #self.tree = None

    def getMove(self):
        assert self.game is not None, "MINIMAX ERROR: No game has been initialized!"
        assert (self.player == "RED") or (self.player == "BLUE"), \
            "MINIMAX ERROR: Player must be 'RED' or 'BLUE'!"

        # Create a root node and build the search tree to decide the next move
        #root = tree.Node(self.game, self.player, 0, "MAX", None, None)
        root = tree.Node(self.game, self.player, 0, "MAX", None)
        tree.buildTree(root)

        optimalMove = root.childChoice.prevMove

        assert optimalMove is not None, "MINIMAX ERROR: No move can be made!"

        return optimalMove


    def makeMove(self):
        return self.getMove()
