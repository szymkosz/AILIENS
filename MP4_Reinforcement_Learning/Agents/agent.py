from pong import Pong

NAME = "AGENT"

class Agent(object):
    def __init__(self, game=Pong(self), playerNum=1):
        self.name = NAME
        self.game = game
        self.playerNum = playerNum
        # self.playerColor = ?


    """
    The getAction function should decide the action this agent should take
    given the state of self.game.  It should return 1 if the paddle should
    move up, -1 if the paddle should move down, or 0 if the paddle should do
    nothing.
    """
    def getAction(self):
        raise NotImplementedError()
