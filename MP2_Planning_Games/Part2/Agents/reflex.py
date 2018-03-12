from gomoku import Gomoku
from position import Position
from Agents.agent import Agent
import random
import helper

class Reflex(Agent):
    def __init__(self, game=Gomoku(), playerNum=1):
        super().__init__(game, playerNum)
        self.name = "REFLEX"

    def makeMove(self):
        moveToMake = self.getMove()

        if self.firstMove:
            self.firstMove = False

        # The agent is player1/RED
        settingRed = self.game.players[0] == self.player

        return self.game.setPiece(moveToMake[0], moveToMake[1], settingRed)

    def getMove(self):
        patterns = self.game.getPatterns()
        curPattern = (self.player, 4, True) ## Agent, 4-in-a-row, open
        count = patterns[0][curPattern]

        def unwrapList(toUnwrap, unwrapped):
            if type(toUnwrap) == type([]):
                for value in toUnwrap:
                    unwrapList(value, unwrapped)
            else:
                unwrapped.append(toUnwrap)

        def breakTie(moves):
            unwrappedMoves = []
            unwrapList(moves, unwrappedMoves)
            unwrappedMoves = sorted(unwrappedMoves)
            return unwrappedMoves[0]


        # print("curPattern: ", curPattern)
        # print("Count: ", count)

        ## 5. The first move can follow any of the following strategies:
        #       -   Follow rule #4 above (and choose bottom left corner)
        #   ->  -   Play at random
        #       -   Make an optimal move (in the middle)
        if self.firstMove:
            x = round((self.game.dim - 1) * random.random())
            y = round((self.game.dim - 1) * random.random())
            while ((x,y) in self.game.movesTaken):
                x = round((self.game.dim - 1) * random.random())
                y = round((self.game.dim - 1) * random.random())
            nextCoord = (x,y)
            return nextCoord


        ## 1. Check whether the agent can win the game by placing one stone
        #      Break a tie by choosing a move in the following order:
        #           left > down > right > up
        if count > 0:
            # print("\tin first rule")
            # Only one move is needed to win the game, return that move.
            allPossibleMoves = []
            unwrapList(patterns[2][curPattern][True], allPossibleMoves)
            allPossibleMoves = sorted(allPossibleMoves)
            nextCoord = allPossibleMoves[0]
            return nextCoord

        ## 2. Check whether the opponent has an unbroken chain of 4 stones and an
        #      empty position that could win the game. Place a stone in that position.
        curPattern = (Gomoku.players[self.playerNum % 2], 4, True)
        count = patterns[0][curPattern]
        # print("curPattern: ", curPattern)
        # print("Count: ", count)
        if count > 0:
            # print("\tin second rule")
            # Only one move is needed to win, so if there are more than one possible,
            #  the game would be lost anyway, so just get the first possible one.
            allPossibleMoves = []
            unwrapList(patterns[2][curPattern][True], allPossibleMoves)
            allPossibleMoves = sorted(allPossibleMoves)
            nextCoord = allPossibleMoves[0]
            return nextCoord

        ## 3. Check whether the opponent has an unbroken chain of 3 stones and an
        #      empty position on both ends. Break a tie by choosing a move in the
        #      following order:
        #           left > down > right > up
        curPattern = (Gomoku.players[self.playerNum % 2], 3, True)
        count = patterns[0][curPattern]
        # print("curPattern: ", curPattern)
        # print("Count: ", count)
        if count > 0:
            # print("\tin third rule")
            allPossibleMoves = []
            listToUnwrap = []
            for i in patterns[2][curPattern][True]:
                if len(i) > 1:
                    listToUnwrap.append(i)
            unwrapList(listToUnwrap, allPossibleMoves)
            allPossibleMoves = sorted(allPossibleMoves)
            nextCoord = allPossibleMoves[0]
            return nextCoord

        ## 4. Otherwise, find the winning block (a block of 5 consecutive spaces
        #      in which victory is still possible) containing the largest number of
        #      the agent's stones.
        #
        #     To break a tie, find the position which is farthest to the left;
        #      among those which are farthest to the left, find the position
        #      which is closest to the bottom.
        # patternsToCheck = [(self.player, 3, True), (self.player, 2, True),
        #                    (self.player, 1, True), (None, 5, True)]
        # for pattern in patternsToCheck:
        #     curPattern = (self.player, 3, True)
        #     count = patterns[0][curPattern]
        # print("\tin fourth rule")
        helperDicts = helper.findCoordinates(self.game)
        possibleMoves = []
        for num in reversed(range(Gomoku.minStones, Gomoku.maxStones + 1)):
            if helperDicts[0][(self.player, num)]:
                for startingCoordKey in helperDicts[0][(self.player, num)]:
                    possibleMoves.append(helperDicts[1][startingCoordKey])
                possibleMoves = sorted(possibleMoves)
                print(possibleMoves)
                return possibleMoves[0]
