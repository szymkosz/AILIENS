from gomoku import Gomoku
from position import Position
from Agents.agent import Agent
import random
import helper

class Reflex(Agent):
    def __init__(self, game=Gomoku(), playerNum=1):
        super().__init__(game, playerNum)
        self.name = "REFLEX"
        self.firstMove = True

    def makeMove(self):
        moveToMake = self.getMove()

        print(moveToMake)

        if self.firstMove:
            self.firstMove = False

        # The agent is player1/RED
        settingRed = self.game.players[0] == self.player

        return self.game.setPiece(moveToMake[0], moveToMake[1], settingRed)

    def getMove(self):
        patterns = self.game.getPatterns()
        curPattern = (self.player, 4, True) ## Agent, 4-in-a-row, open
        count = patterns[0][curPattern]
        nextCoord = None

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

        def randomMove():
            x = round((self.game.dim - 1) * random.random())
            y = round((self.game.dim - 1) * random.random())
            while ((x,y) in self.game.movesTaken):
                x = round((self.game.dim - 1) * random.random())
                y = round((self.game.dim - 1) * random.random())
            nextCoord = (x,y)
            return nextCoord

        ## 5. The first move can follow any of the following strategies:
        #       -   Follow rule #4 above (and choose bottom left corner)
        #   ->  -   Play at random
        #       -   Make an optimal move (in the middle)
        if self.firstMove:
            return randomMove()


        ## 1. Check whether the agent can win the game by placing one stone
        #      Break a tie by choosing a move in the following order:
        #           left > down > right > up
        if count > 0:
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

        if count > 0:
            # Only one move is needed to win, so if there are more than one possible,
            #  the game would be lost anyway, so just get the first possible one.
            allPossibleMoves = []
            unwrapList(patterns[2][curPattern][True], allPossibleMoves)
            allPossibleMoves.sort()
            nextCoord = allPossibleMoves[0]
            return nextCoord

        ## 3. Check whether the opponent has an unbroken chain of 3 stones and an
        #      empty position on both ends. Break a tie by choosing a move in the
        #      following order:
        #           left > down > right > up
        curPattern = (Gomoku.players[self.playerNum % 2], 3, True)
        count = patterns[0][curPattern]

        if count > 0:
            allPossibleMoves = []
            listToUnwrap = []

            for i in patterns[2][curPattern][True]:
                ## For there to be an empty position on both ends, this list must
                #   have a length of 2
                if len(i) > 1:
                    listToUnwrap.append(i)

            ## Consolidate all of these candidate positions into a single list and tie break
            unwrapList(listToUnwrap, allPossibleMoves)
            allPossibleMoves.sort()
            if allPossibleMoves:
                return allPossibleMoves[0]

        ## 4. Otherwise, find the winning block (a block of 5 consecutive spaces
        #      in which victory is still possible) containing the largest number of
        #      the agent's stones.
        #
        #     To break a tie, find the position which is farthest to the left;
        #      among those which are farthest to the left, find the position
        #      which is closest to the bottom.
        helperDicts = helper.findCoordinates(self.game)
        possibleMoves = []

        # Iterate over the possible number of stones in a block in reverse
        for num in reversed(range(Gomoku.minStones, Gomoku.maxStones + 1)):
            possibleMoves = []

            # If there's any possible move, that's it
            if helperDicts[0][(self.player, num)]:
                for startingCoordKey in helperDicts[0][(self.player, num)]:
                    possibleMoves.append(helperDicts[1][startingCoordKey])
                possibleMoves.sort()
                return possibleMoves[0]

        # Lastly, look at empty blocks of 5 positions
        curPattern = (None, 5, False)

        if nextCoord is None and patterns[0][curPattern] > 0:
            possibleMoves = []
            for block in patterns[1][curPattern]:
                x = block[0][0]
                y = block[0][1]
                dir = block[1]

                ## Add the starting and ending coordinates
                possibleMoves.append((x,y))
                possibleMoves.append((x + 4 * dir[0], y + 4 * dir[1]))

            # Break a tie
            possibleMoves.sort()
            nextCoord = possibleMoves[0]


        ## All other options have been exhausted...
        #   Loop over the board and choose the first open position
        if nextCoord is None:
            possibleMoves = 0
            board = self.game.board
            for x in range(self.game.dim):
                for y in range(self.game.dim):
                    curPos = board[x][y]
                    if curPos.char == '.' and nextCoord is None:
                        nextCoord = (x,y)
                        break
        return nextCoord
