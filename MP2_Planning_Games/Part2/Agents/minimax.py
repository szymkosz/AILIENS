from gomoku import Gomoku
from position import Position
from agent import Agent

class MiniMax(Agent):
    def __init__(self, game=Gomoku(), playerNum=1):
        super().__init__(game, playerNum)
        self.name = "MINIMAX"

    def makeMove(self):
        raise NotImplementedError()
