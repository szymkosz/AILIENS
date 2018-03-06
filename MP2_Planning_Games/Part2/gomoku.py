import sys
from position import Position

## Used for formatting standard output
P1_COLOR = '\033[91m'
P2_COLOR = '\033[94m'
C_END = '\033[0m'

players = ["RED", "BLUE"]   ## ONLY TWO PLAYERS

class Gomoku:
    ## Constructor
    def __init__(self, dim=7):
        self.curr_char = 'a'
        self.dim = dim
        self.reds_turn = True       # Red always starts
        self.board = [ [ Position() for i in range(dim) ] for j in range(dim) ]

    ## Sets the next piece at the desired coordinates (x,y).
    #   @param red - flag indicating the color of the piece to set
    #                True (1) for RED; False (0) for BLUE
    def setPiece(self, x, y, settingRed):
        pos = self.board[x][y]

        # If the piece at (x,y) is empty
        if pos.char != '.':
            raise ValueError("Trying to set a piece in a non-empty position, char: " + str(pos.char))

        # Check to see if it is the turn of the player setting the piece
        if settingRed != self.reds_turn:
            if settingRed:
                raise ValueError("Trying to set a {0}{3[0]}{2} piece when it is {1}{3[1]}{2}'s turn.".format(P1_COLOR, P2_COLOR, C_END, players))
            elif not settingRed:
                raise ValueError("Trying to set a {1}{3[1]}{2} piece when it is {0}{3[0]}{2}'s turn.".format(P1_COLOR, P2_COLOR, C_END, players))

        # If setting a red piece and it is red's turn
        if settingRed and self.reds_turn:

            # Set the position's char to the next red char and its color to "RED"
            # Switch the turn
            pos.char = self.curr_char
            pos.color = players[0]
            self.reds_turn = False

        # Else if setting a blue piece and it is blue's turn
        elif not settingRed and not self.reds_turn:

            # Set the position's char to the next blue char and its color to "BLUE"
            # Switch the turn
            pos.char = self.curr_char.upper()
            pos.color = players[1]
            self.curr_char = chr(ord(self.curr_char) + 1)
            self.reds_turn = True

        ## CHECK IF MOVE WON THE GAME
        patterns = self.getPatterns()

        return patterns[0][(pos.color, 5, True)] > 0 or patterns[0][(pos.color, 5, False)] > 0

    ## Parses the board and populates a dictionary specifying how many of each
    #   type of pattern is present on the current board.
    def getPatterns(self):
        ## Can only check if patterns of >2 are open or closed
        minStones = 1
        maxStones = 5

        possibleClosed = [True, False]

        # Initializes the dictionary { (player, numberOfStonesInARow, Open/Closed) : 0 }
        patterns = { (p,num,closed):0 for p in [players[0],players[1]] \
                                for num in range(minStones,maxStones+1) for closed in possibleClosed }
        patternStartingPos = { (p,num,closed):[] for p in [players[0],players[1]] \
                                for num in range(minStones,maxStones+1) for closed in possibleClosed }

        # Add dictionary key to include winning block search
        for closed in possibleClosed:
            patterns[ (None, 5, closed) ] = 0
            patternStartingPos[ (None, 5, closed) ] = []

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
            player, num, closed = pattern
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

            # if not winningBlockSearch:
            #     if startsPattern and prevPos is not None:
            #         print("\nPlayer: ", player)
            #         print("Num: ", num)
            #         print("Direction: ", direction)
            #         print("Current Position: ", pos)
            #         print("Prev Pos: ", prevPos)
            #         print("End Pos: ", endPos )
            #         print("End+1 Pos: ", onePosPast)
            #         print("\tcurPos color: ", self.board[pos[0]][pos[0]].color)
            #         print("\tprevPos color: ", self.board[prevPos[0]][prevPos[1]].color)
            #         print("\tendPos color: ", self.board[endPos[0]][endPos[1]].color)
            #         print("\tonePosPast color: ", self.board[onePosPast[0]][onePosPast[1]].color)
            #         if closed:
            #             if (prevPos is not None and self.board[prevPos[0]][prevPos[1]].color == None) \
            #                 or (curPos is not None and self.board[curPos[0]][curPos[1]].color == None):
            #                 print("\t\tSupposed to be closed and not added")
            #         print()

            # Check if the position is open or closed
            # if closed:
            #     if (prevPos is not None and self.board[prevPos[0]][prevPos[1]].color == None) \
            #         or (curPos is not None and self.board[curPos[0]][curPos[1]].color == None):
            #         return False
            # elif not closed:
            #     if (prevPos is not None and self.board[prevPos[0]][prevPos[1]].color != None) \
            #         and (curPos is not None and self.board[curPos[0]][curPos[1]].color != None):
            #         return False

            # If looking for an open pattern, return False. This will get
            #  populated by another function
            if not closed:
                return False

            return True

        # Takes in each pattern and checks if a win is still possible in that
        def patternIsOpen(pattern, pos, direction):
            player, num, closed = pattern
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

        ## Go through each position on the board and look for each kind of pattern
        #   Check if the
        for x in range(self.dim):
            for y in range(self.dim):
                curPos = (x,y)
                for direction in directions:
                    for closed in possibleClosed:
                    # for closed in [True]:
                        for player in players:
                            for num in range(minStones, maxStones+1):
                                if findPattern((player, num, closed), curPos, direction):
                                    patterns[(player, num, closed)] += 1
                                    if (curPos, direction) not in (patternStartingPos[(player, num, closed)]):
                                        patternStartingPos[(player, num, closed)].append((curPos, direction))
                                    if patternIsOpen((player, num, closed), curPos, direction):
                                        patterns[(player, num, False)] += 1
                                        patterns[(player, num, closed)] -= 1
                                        if (curPos, direction) not in (patternStartingPos[(player, num, False)]):
                                            patternStartingPos[(player, num, False)].append((curPos, direction))
                                            patternStartingPos[(player, num, True)].remove((curPos, direction))
                        if findPattern((None, 5, closed), curPos, direction):
                            patterns[(None, 5, closed)] += 1
                            if (curPos, direction) not in (patternStartingPos[(None, 5, closed)]):
                                patternStartingPos[(None, 5, closed)].append((curPos, direction))

        return (patterns, patternStartingPos)


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
        ret += "  " + ' '.join(str(i+int(not zeroIndexed)) for i in range(self.dim)) + "\n"
        for i in range(self.dim):
            # First row is top row
            ret += str(i+int(not zeroIndexed)) + " " + ' '.join(n[i].__repr__() for n in board) + "\n"

            # First row is bottom row
            # ret += str(len(board) - i - int(zeroIndexed)) + " " + ' '.join(n[i].__repr__() for n in board) + "\n"

        ## Numbers along bottom
        # ret += "  " + ' '.join(str(i+int(not zeroIndexed)) for i in range(self.dim)) + "\n"
        return ret
