from gomoku import Gomoku
from position import Position
from agent import Agent
from sys import maxsize
from tree import Node

class MiniMax(Agent):
    def __init__(self, game=Gomoku(), playerNum=1):
        super().__init__(game, playerNum)
        self.name = "MINIMAX"
        self.tree = None

    def getMove(self):
        pass

    def makeMove(self):
        self.tree = helper.fillMinimaxTree()
        optimalMoveSequence = []
        curNode = 
