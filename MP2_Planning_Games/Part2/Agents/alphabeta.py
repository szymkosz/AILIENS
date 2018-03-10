from gomoku import Gomoku
from position import Position
from agent import Agent
from sys import maxsize
from tree import Node

class AlphaBeta(Agent):
    def __init__(self, game=Gomoku(), playerNum=1):
        super().__init__(game, playerNum)
        self.name = "ALPHA_BETA"

    def getMove(self):
        pass
        
    def makeMove(self):
        raise NotImplementedError()
