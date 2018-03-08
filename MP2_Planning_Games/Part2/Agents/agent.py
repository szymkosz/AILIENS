from gomoku import Gomoku
from position import Position

class Agent:
    def __init__(self, game=Gomoku(), playerNum=1):
        self.name = "AGENT"
        self.game = game
        self.playerNum = playerNum
        self.player = Gomoku.players[(playerNum-1)%2]

    def getMoves(self):
        raise NotImplementedError()

    def makeMove(self):
        raise NotImplementedError()
