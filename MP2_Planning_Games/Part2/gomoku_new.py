import sys
from position import Position
from gomoku import Gomoku
from operator import itemgetter
import helper


class NewGomoku(Gomoku):
    # Right, down, diag-right-up, diag-right-down
    directions = [(1,0),(0,1),(1,-1),(1,1)]

    def __init__(self):
        super().__init__()
        self.blocks = {}
        self.coordinateToBlocks = {(x,y): [] for x in range(self.dim) for y in range(self.dim) }
        self.initDicts()
        self.scores = { key: 0 for key in self.blocks.keys()}

    def initDicts(self):
        for x in range(self.dim):
            for y in range(self.dim):
                curCoord = (x, y)
                for direction in NewGomoku.directions:
                    curBlock = []
                    append = True
                    for i in range(5):
                        nextPos = self.nextPosition(curCoord, direction, length=i)
                        if nextPos is not None:
                            curBlock.append(nextPos)
                        else:
                            append = False
                            break
                    if append:
                        curBlockShort = (curCoord, direction)
                        self.blocks[curBlockShort] = curBlock
                        for coord in curBlock:
                            if curBlockShort not in self.coordinateToBlocks[coord]:
                                self.coordinateToBlocks[coord].append(curBlockShort)


    # Determines if the coordinates are out of bounds of the board
    def outOfBounds(self, pos):
        return pos[0] < 0 or pos[0] >= self.dim or pos[1] < 0 or pos[1] >= self.dim

    # Determines the coordinates of the next position
    # @param pos - tuple containing the starting coordinates
    #        direction - tuple containing the direction in which to go
    #   Opt: reverse - boolean whether to go in the reverse direction instead
    #                  of the forward direction
    #        length - integer of the number of steps to go away from the
    #                 starting coordinates
    # Can also return the position in the reverse direction by setting the
    #  reverse flag to True
    def nextPosition(self, pos, direction, reverse=False, length=1):
        if reverse:
            nextPos = (pos[0] - length * direction[0], pos[1] - length * direction[1])
        else:
            nextPos = (pos[0] + length * direction[0], pos[1] + length * direction[1])
        return nextPos if not self.outOfBounds(nextPos) else None

    ## Sets the next piece at the desired coordinates (x,y).
    #   @param x - x-coordinate of the desired move to make
    #   @param y - y-coordinate of the desired move to make
    #   @param settingRed - flag indicating the color of the piece to set
    #                True (1) for RED; False (0) for BLUE
    #   @param isHuman - flag indicating if the agent is human
    def setPiece(self, x, y, settingRed, isHuman=False):
        pos = self.board[x][y]
        curCoord = (x,y)

        # If the piece at (x,y) is not empty
        if pos.char != '.':
            if isHuman:
                patterns = self.getPatterns()
                return patterns[0][(pos.color, 5, True)] > 0 or patterns[0][(pos.color, 5, False)] > 0
            else:
                raise ValueError("Trying to set a piece in a non-empty position, char: " + str(pos.char))

        # Check to see if it is the turn of the player setting the piece
        if settingRed != self.reds_turn:
            if settingRed:
                raise ValueError("Trying to set a {0}{3[0]}{2} piece when it is {1}{3[1]}{2}'s turn.".format(Position.colors[Gomoku.players[0]], Position.colors[Gomoku.players[1]], Position.colors["END"], Gomoku.players))
            elif not settingRed:
                raise ValueError("Trying to set a {1}{3[1]}{2} piece when it is {0}{3[0]}{2}'s turn.".format(Position.colors[Gomoku.players[0]], Position.colors[Gomoku.players[1]], Position.colors["END"], Gomoku.players))

        # If setting a red piece and it is red's turn
        if settingRed and self.reds_turn:

            # Set the position's char to the next red char and its color to "RED"
            # Add the coordinates to the movesTaken list
            # Switch the turn
            pos.char = self.curr_char
            pos.color = Gomoku.players[0]
            self.movesTaken.append(curCoord)
            self.reds_turn = False

        # Else if setting a blue piece and it is blue's turn
        elif not settingRed and not self.reds_turn:

            # Set the position's char to the next blue char and its color to "BLUE"
            # Add the coordinates to the movesTaken list
            # Switch the turn
            pos.char = self.curr_char.upper()
            pos.color = Gomoku.players[1]
            self.curr_char = chr(ord(self.curr_char) + 1)
            self.movesTaken.append(curCoord)
            self.reds_turn = True

        for block in self.coordinateToBlocks[curCoord]:
            newScore = self.evaluateBlockScore(self.blocks[block])
            self.scores[block] = newScore
            # print("set-current block: ", block)
            # print("Set-newScore: ", newScore)

        ## CHECK IF MOVE WON THE GAME
        patterns = self.getPatterns()
        # print("Set-full board score: ", helper.fullBoardScore(self))
        return patterns[0][(pos.color, 5, True)] > 0 or patterns[0][(pos.color, 5, False)] > 0

    def evaluateBlockScore(self, block):
        playerColor = None
        count = 0
        for coord in block:
            curPos = self.board[coord[0]][coord[1]]
            if curPos.color is not None and playerColor is None:
                playerColor = curPos.color
            if playerColor == curPos.color and playerColor is not None:
                count += 1
            elif playerColor != curPos.color and curPos.color != None:
                count = 0
                break
        return count

    ## Function to undo setting a piece on the board. Used by Agent algorithms
    #   to efficiently explore and evaluate potential moves by allowing them to
    #   set a piece, examine the board, and unset that piece to evaluate another.
    def unsetPiece(self):
        # If no moves have been taken yet, there are no pieces to unset.
        #  Just do nothing and return False.
        if not self.movesTaken:
            return False

        # Obtain the last move taken and remove if from the movesTaken list
        coordToUnset = self.movesTaken.pop(-1)
        curCoord = coordToUnset
        posToUnset = self.board[coordToUnset[0]][coordToUnset[1]]

        # Set the position's char back to '.' and the color back to None
        posToUnset.char = '.'
        posToUnset.color = None

        ## If it is now RED's turn, BLUE was the last to set a piece, so that
        #   should be the piece to unset
        if self.reds_turn:

            # Because BLUE was the last to set a piece, he also incremented the
            #  game's current char, curr_char, so it must be reversed
            self.curr_char = chr(ord(self.curr_char) - 1)
        # Otherwise, nothing needs to be done

        # Switch the turn back to the player whose piece was unset
        self.reds_turn = not self.reds_turn

        for block in self.coordinateToBlocks[curCoord]:
            newScore = self.evaluateBlockScore(self.blocks[block])
            self.scores[block] = newScore
            # print("Unset-newScore: ", newScore)

        # A piece was removed from the board, so return True
        # print("Set-full board score: ", helper.fullBoardScore(self))
        return True
