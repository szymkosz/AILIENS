from gomoku import Gomoku
from position import Position
from agent import Agent

class Reflex(Agent):
    def __init__(self, game=Gomoku(), playerNum=1):
        super().__init__(game, playerNum)
        self.name = "REFLEX"

    def makeMove(self):
        raise NotImplementedError()

    def getMove(self):
        patterns = self.game.getPatterns()
        curPattern = (self.player, 4, False) ## Agent, 4-in-a-row, open
        count = patterns[0][curPattern]

        ## 1. Check whether the agent can win the game by placing one stone
        #      Break a tie by choosing a move in the following order:
        #           left > down > right > up
        if count > 0:
            # Only one move is needed to win the game, return that move.
            allPossibleMoves = patterns[2][curPattern]
            # TODO: Break a potential tie. Check how moves are sorted.
            nextCoord = allPossibleMoves[0][0]
            return nextCoord

        ## 2. Check whether the opponent has an unbroken chain of 4 stones and an
        #      empty position that could win the game. Place a stone in that position.
        curPattern = (Gomoku.players[playerNum%2], 4, False)
        count = patterns[0][curPattern]
        if count > 0:
            # Only one move is needed to win, so if there are more than one possible,
            #  the game would be lost anyway, so just get the first possible one.
            allPossibleMoves = patterns[2][curPattern]
            nextCoord = allPossibleMoves[0][0]
            return nextCoord

        ## 3. Check whether the opponent has an unbroken chain of 3 stones and an
        #      empty position on both ends. Break a tie by choosing a move in the
        #      following order:
        #           left > down > right > up
        curPattern = (Gomoku.players[playerNum%2], 3, False)
        count = patterns[0][curPattern]
        allPossibleMoves = patterns[2][curPattern]
        while count > 0:
            pass

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
