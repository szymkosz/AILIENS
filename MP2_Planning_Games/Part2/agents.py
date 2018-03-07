from gomoku import Gomoku
from board import Board
from position import Position

class Agent:
    def __init__(self, game, playerNum):
        self.name = "AGENT"
        self.game = game
        self.playerNum = playerNum
        self.player = Gomoku.players[(playerNum-1)%2]

    def getMoves(self):
        raise NotImplementedError()

    def makeMove(self):
        raise NotImplementedError()

class Reflex(Agent):
    def __init__(self, game, playerNum):
        self.name = "REFLEX"
        self.game = game
        self.playerNum = playerNum
        self.player = Gomoku.players[(playerNum-1)%2]

    def makeMove(self):
        raise NotImplementedError()

    def getMove(self):
        patterns = self.game.getPatterns()
        curPattern = (Gomoku.players[playerNum%2], 4, False) ## Opponent, open, 4-in-a-row
        count = patterns[0][curPattern]

        ## 1. Check whether the agent can win the game by placing one stone
        #      Break a tie by choosing a move in the following order:
        #           left > down > right > up
        if count > 0:
            curPatternVector = patterns[1][curPattern]
            prevPos

        ## 2. Check whether the opponent has an unbroken chain of 4 stones and an
        #      empty position that could win the game. Place a stone in that position.

        ## 3. Check whether the opponent has an unbroken chain of 3 stones and an
        #      empty position on both ends. Break a tie by choosing a move in the
        #      following order:
        #           left > down > right > up

        ## 4. Otherwise, find the winning block (a block of 5 consecutive spaces
        #      in which victory is still possible) containing the largest number of
        #      the agent's stones.
        #
        #     To break a tie, find the position which is farthest to the left;
        #      among those which are farthest to the left, find the position
        #      which is closest to the bottom.

        ## 5. The first move can follow any of the following strategies:
        #       -   Follow rule #4 above (and choose bottom left corner)
        #       -   Play at random
        #       -   Make an optimal move (in the middle)
        raise NotImplementedError()
