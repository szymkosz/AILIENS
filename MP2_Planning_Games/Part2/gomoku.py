import sys
from position import Position
from operator import itemgetter

## Used for formatting standard output
P1_COLOR = '\033[91m'
P2_COLOR = '\033[94m'
C_END = '\033[0m'

class Gomoku:
    players = ["RED", "BLUE"]   ## ONLY TWO PLAYERS

    ## Constructor
    def __init__(self, dim=7):
        self.curr_char = 'a'
        self.dim = dim
        self.reds_turn = True       # Red always starts
        self.board = [ [ Position() for i in range(dim) ] for j in range(dim) ]
        self.movesTaken = []
        # self.emptySquares = [ (x,y) for x in range(dim) for y in range(dim) ]

    ## Sets the next piece at the desired coordinates (x,y).
    #   @param settingRed - flag indicating the color of the piece to set
    #                True (1) for RED; False (0) for BLUE
    def setPiece(self, x, y, settingRed):
        pos = self.board[x][y]

        # If the piece at (x,y) is not empty
        if pos.char != '.':
            raise ValueError("Trying to set a piece in a non-empty position, char: " + str(pos.char))

        # Check to see if it is the turn of the player setting the piece
        if settingRed != self.reds_turn:
            if settingRed:
                raise ValueError("Trying to set a {0}{3[0]}{2} piece when it is {1}{3[1]}{2}'s turn.".format(P1_COLOR, P2_COLOR, C_END, Gomoku.players))
            elif not settingRed:
                raise ValueError("Trying to set a {1}{3[1]}{2} piece when it is {0}{3[0]}{2}'s turn.".format(P1_COLOR, P2_COLOR, C_END, Gomoku.players))

        # If setting a red piece and it is red's turn
        if settingRed and self.reds_turn:

            # Set the position's char to the next red char and its color to "RED"
            # Add the coordinates to the movesTaken list
            # Switch the turn
            pos.char = self.curr_char
            pos.color = Gomoku.players[0]
            self.movesTaken.append((x,y))
            self.reds_turn = False

        # Else if setting a blue piece and it is blue's turn
        elif not settingRed and not self.reds_turn:

            # Set the position's char to the next blue char and its color to "BLUE"
            # Add the coordinates to the movesTaken list
            # Switch the turn
            pos.char = self.curr_char.upper()
            pos.color = Gomoku.players[1]
            self.curr_char = chr(ord(self.curr_char) + 1)
            self.movesTaken.append((x,y))
            self.reds_turn = True

        # self.emptySquares.remove((x,y))
        ## CHECK IF MOVE WON THE GAME
        patterns = self.getPatterns()

        return patterns[0][(pos.color, 5, True)] > 0 or patterns[0][(pos.color, 5, False)] > 0

    def unsetPiece(self):
        # If no moves have been taken yet, there are no pieces to unset.
        #  Just do nothing and return False.
        if not self.movesTaken:
            return False

        # Obtain the last move taken and remove if from the movesTaken list
        coordToUnset = self.movesTaken.pop(-1)
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

    ## Parses the board and populates a dictionary specifying how many of each
    #   type of pattern is present on the current board.
    def getPatterns(self):
        ## Can only check if patterns of >2 are open or closed
        minStones = 1
        maxStones = 5

        possibleWin = [True, False]

        # Initializes the dictionary { (player, numberOfStonesInARow, Open/Closed) : 0 }
        patternCount = { (p,num,canWin):0 for p in [Gomoku.players[0],Gomoku.players[1]] \
                                for num in range(minStones,maxStones+1) for canWin in possibleWin }
        patternStartingPos = { (p,num,canWin):[] for p in [Gomoku.players[0],Gomoku.players[1]] \
                                for num in range(minStones,maxStones+1) for canWin in possibleWin }
        patternMovesToComplete = { (p,num,canWin):[] for p in [Gomoku.players[0],Gomoku.players[1]] \
                                for num in range(minStones,maxStones+1) for canWin in possibleWin }

        # Add dictionary key to include winning block search
        for canWin in possibleWin:
            patternCount[ (None, 5, canWin) ] = 0
            patternStartingPos[ (None, 5, canWin) ] = []

        # Right, down, diag-right-up, diag-right-down
        directions = [(1,0),(0,1),(1,-1),(1,1)]

        def outOfBounds(pos):
            return pos[0] < 0 or pos[0] >= self.dim or pos[1] < 0 or pos[1] >= self.dim

        def nextPosition(pos, direction, reverse=False, length=1):
            if reverse:
                nextPos = (pos[0] - length * direction[0], pos[1] - length * direction[1])
            else:
                nextPos = (pos[0] + length * direction[0], pos[1] + length * direction[1])
            return nextPos if not outOfBounds(nextPos) else None

        def findPattern(pattern, pos, direction):
            player, num, canWin = pattern
            curPos = pos

            # If player == None, we are looking for winning blocks
            winningBlockSearch = player == None

            # Check if this position begins the pattern (player's piece is not
            #  the piece before it)
            prevPos = nextPosition(pos, direction, reverse=True)
            startsPattern = (prevPos == None) or (self.board[prevPos[0]][prevPos[1]].color != player)

            # Check if the number of stones required is within bounds
            endPos = nextPosition(pos, direction, reverse=False, length=num-1)
            endPosOOB = endPos == None

            # If it is not the pattern-starting stone or the ending stone would
            #  be out of bounds, return False
            if (not startsPattern and not winningBlockSearch) or endPosOOB:
                return False

            onePosPast = nextPosition(endPos, direction)
            if (onePosPast != None and self.board[onePosPast[0]][onePosPast[1]].color == player) and not (winningBlockSearch):
                return False

            # Check if pattern is present (with potential overlap)
            for i in range(num):
                # nextPos = nextPosition(curPos, direction)
                if self.board[curPos[0]][curPos[1]].color != player:
                    return False
                curPos = nextPosition(curPos, direction)

            # If looking for a winning block, return False. This will get
            #  populated by another function
            if canWin:
                return False

            return True

        # Takes in each pattern and checks if a win is still possible in that block
        def patternIsOpen(pattern, pos, direction):
            player, num, canWin = pattern
            curCoord = nextPosition(pos, direction, length=num)
            prevCoord = nextPosition(pos, direction, reverse=True)
            if curCoord != None:
                curPos = self.board[curCoord[0]][curCoord[1]]
            if prevCoord != None:
                prevPos = self.board[prevCoord[0]][prevCoord[1]]

            spotsNecessary = 5 - num
            count = 0
            isOpen = False

            # Check forward direction
            while (count < spotsNecessary):
                if curCoord != None and (curPos.color == player or curPos.color == None):
                    curPos = self.board[curCoord[0]][curCoord[1]]
                    count += 1
                    curCoord = nextPosition(curCoord, direction)
                else:
                    break

            # Check reverse direction
            while (count < spotsNecessary):
                if prevCoord != None and (prevPos.color == player or prevPos.color == None):
                    prevPos = self.board[prevCoord[0]][prevCoord[1]]
                    count += 1
                    prevCoord = nextPosition(prevCoord, direction, reverse=True)
                else:
                    break

            if count >= spotsNecessary:
                isOpen = True
            return isOpen

        def getMovesToComplete(pattern, pos, direction):
            player, num, canWin = pattern
            curCoord = nextPosition(pos, direction, length=num)
            prevCoord = nextPosition(pos, direction, reverse=True)
            if curCoord != None:
                curPos = self.board[curCoord[0]][curCoord[1]]
            if prevCoord != None:
                prevPos = self.board[prevCoord[0]][prevCoord[1]]

            possibleMoves = []
            spotsNecessary = 5 - num
            count = 0

            # Check forward direction
            while (count < spotsNecessary):
                if curCoord != None and (curPos.color == player or curPos.color == None):
                    curPos = self.board[curCoord[0]][curCoord[1]]
                    if curPos.color == None:
                        possibleMoves.append(curCoord)
                    count += 1
                    curCoord = nextPosition(curCoord, direction)
                else:
                    break

            spotsNecessary = 5 - num
            count = 0

            # Check reverse direction
            while (count < spotsNecessary):
                if prevCoord != None and (prevPos.color == player or prevPos.color == None):
                    prevPos = self.board[prevCoord[0]][prevCoord[1]]
                    if prevPos.color == None:
                        possibleMoves.append(prevCoord)
                    count += 1
                    prevCoord = nextPosition(prevCoord, direction, reverse=True)
                else:
                    break

            possibleMoves = sorted(possibleMoves, key=itemgetter(1))

            return sorted(possibleMoves, key=itemgetter(0))

        ## Go through each position on the board and look for each kind of pattern
        #   Check if the
        for x in range(self.dim):
            for y in range(self.dim):
                curPos = (x,y)
                for direction in directions:
                    for canWin in possibleWin:
                        for player in Gomoku.players:
                            for num in range(minStones, maxStones+1):
                                curPattern = (player, num, canWin)
                                if findPattern(curPattern, curPos, direction):
                                    patternCount[(player, num, canWin)] += 1
                                    if (curPos, direction) not in (patternStartingPos[curPattern]):
                                        endPos = nextPosition(curPos, direction, length=num-1)
                                        patternStartingPos[curPattern].append((curPos, endPos, direction))
                                    if patternIsOpen(curPattern, curPos, direction):
                                        patternCount[(player, num, True)] += 1
                                        patternCount[curPattern] -= 1
                                        if (curPos, direction) not in (patternStartingPos[(player, num, True)]):
                                            patternStartingPos[(player, num, True)].append((curPos, endPos, direction))
                                            patternMovesToComplete[(player,num, True)].append(getMovesToComplete((player, num, canWin), curPos, direction))
                                            patternStartingPos[(player, num, False)].remove((curPos, endPos, direction))
                        if findPattern((None, 5, canWin), curPos, direction):
                            patternCount[(None, 5, canWin)] += 1
                            if (curPos, direction) not in (patternStartingPos[(None, 5, canWin)]):
                                patternStartingPos[(None, 5, canWin)].append((curPos, direction))

        return (patternCount, patternStartingPos, patternMovesToComplete)


    ## Prints the state of the game to standard out
    def printBoard(self):
        board = self.board
        for i in range(len(board)):
            sys.stdout.write(' '.join(n[i].__repr__() for n in board))
            sys.stdout.write("\n")
        sys.stdout.write("\n")

    ## Returns the state of the game as a single string
    def __str__(self):
        zeroIndexed = True
        ret = ""
        board = self.board

        ## Numbers along top
        # ret += "  " + ' '.join(str(i+int(not zeroIndexed)) for i in range(self.dim)) + "\n"
        for i in range(self.dim):
            # First row is top row
            # ret += str(i+int(not zeroIndexed)) + " " + ' '.join(n[i].__repr__() for n in board) + "\n"

            # First row is bottom row
            ret += str(len(board) - i - int(zeroIndexed)) + " " + ' '.join(n[self.dim - i - 1].__repr__() for n in board) + "\n"

        ## Numbers along bottom
        ret += "  " + ' '.join(str(i+int(not zeroIndexed)) for i in range(self.dim)) + "\n"
        return ret
