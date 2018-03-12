from gomoku import Gomoku
from position import Position
from Agents.agent import Agent
from sys import maxsize
import tree

class MiniMax(Agent):
    def __init__(self, game=Gomoku(), playerNum=1):
        super().__init__(game, playerNum)
        self.name = "MINIMAX"
        self.move_num = 1
        self.expandedNodes = 0

        self.treeDepth = 3


    def getMove(self):
        assert self.game is not None, "MINIMAX ERROR: No game has been initialized!"
        assert (self.player == "RED") or (self.player == "BLUE"), \
            "MINIMAX ERROR: Player must be 'RED' or 'BLUE'!"

        self.expandedNodes = 0

        # Create a root node and build the search tree to decide the next move
        #root = tree.Node(self.game, self.player, 0, "MAX", None, None)
        # root = tree.Node(self.game, self.player, 0, "MAX", None)
        root = tree.Node(self.game, self.player, self.treeDepth, "MAX", None)
        tree.buildTree(self, root)
        print(root.value)
        optimalMove = root.childChoice.prevMove
        print(optimalMove)
        assert optimalMove is not None, "MINIMAX ERROR: No move can be made!"

        return optimalMove


    def makeMove(self):
        moveToMake = self.getMove()
        print("Agent: " + self.name + "  Move: " + str(self.move_num) + "  " + \
              self.player + " Nodes Expanded: " + str(self.expandedNodes))
        self.move_num += 1

        # The agent is player1/RED
        settingRed = self.game.players[0] == self.player

        return self.game.setPiece(moveToMake[0], moveToMake[1], settingRed)
