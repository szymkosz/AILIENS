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
        def randomMove():
            x = round((self.game.dim - 1) * random.random())
            y = round((self.game.dim - 1) * random.random())
            while ((x,y) in self.game.movesTaken):
                x = round((self.game.dim - 1) * random.random())
                y = round((self.game.dim - 1) * random.random())
            nextCoord = (x,y)
            return nextCoord

        if self.firstMove:
            return randomMove()


        ## 1. Check whether the agent can win the game by placing one stone
        #      Break a tie by choosing a move in the following order:
        #           left > down > right > up
        if count > 0:
            print("\tin first rule")
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
            print("\tin second rule")
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
            print("\tin third rule")
            allPossibleMoves = []
            listToUnwrap = []
            # print("patterns[2][curPattern][True]", patterns[2][curPattern][True])
            try:
                for i in patterns[2][curPattern][True]:
                    # print("\ti", i)
                    # print("\tlen(i)", len(i))
                    if len(i) > 1:
                        listToUnwrap.append(i)
                unwrapList(listToUnwrap, allPossibleMoves)
                # print("listToUnwrap ", listToUnwrap)
                # print("allPossibleMoves ", allPossibleMoves)
                allPossibleMoves = sorted(allPossibleMoves)
                nextCoord = allPossibleMoves[0]
            except:
                for i in patterns[2][curPattern][True]:
                    # print("\ti", i)
                    # print("\tlen(i)", len(i))
                    if len(i) > 0:
                        listToUnwrap.append(i)
                unwrapList(listToUnwrap, allPossibleMoves)
                # print("listToUnwrap ", listToUnwrap)
                # print("allPossibleMoves ", allPossibleMoves)
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
        print("\tin fourth rule")
        helperDicts = helper.findCoordinates(self.game)
        # for i in helperDicts[0].keys():
        #     print(i, helperDicts[0][i])
        # for i in helperDicts[1].keys():
        #     print(i, helperDicts[1][i])
        possibleMoves = []
        nextCoord = None
        for num in reversed(range(Gomoku.minStones, Gomoku.maxStones + 1)):
            possibleMoves = []
            print(helperDicts[0][(self.player, num)])
            if helperDicts[0][(self.player, num)]:
                for startingCoordKey in helperDicts[0][(self.player, num)]:
                    possibleMoves.append(helperDicts[1][startingCoordKey])
                possibleMoves.sort()
                return possibleMoves[0]

        print("next", nextCoord)
        curPattern = (None, 5, False)
        print("empty blocks: ", patterns[0][curPattern])
        if nextCoord is None and patterns[0][curPattern] > 0:
            possibleMoves = []
            for block in patterns[1][curPattern]:
                x = block[0][0]
                y = block[0][1]
                dir = block[1]
                for i in range(5):
                    possibleMoves.append((x + i * dir[0], y + i * dir[1]))
            possibleMoves.sort()
            nextCoord = possibleMoves[0]


        ## All other options have been exhausted...
        #   Loop over the board and choose a random position.
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
