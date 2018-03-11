import sys
from position import Position
from operator import itemgetter

class Gomoku:
    players = ["RED", "BLUE"]   ## ONLY TWO PLAYERS

    ## Constructor
    def __init__(self, dim=7):
        self.curr_char = 'a'
        self.dim = dim
        self.reds_turn = True       # Red always starts
        self.board = [ [ Position() for i in range(dim) ] for j in range(dim) ]
        self.movesTaken = []

    ## Sets the next piece at the desired coordinates (x,y).
    #   @param x - x-coordinate of the desired move to make
    #   @param y - y-coordinate of the desired move to make
    #   @param settingRed - flag indicating the color of the piece to set
    #                True (1) for RED; False (0) for BLUE
    #   @param isHuman - flag indicating if the agent is human
    def setPiece(self, x, y, settingRed, isHuman=False):
        pos = self.board[x][y]

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

        ## CHECK IF MOVE WON THE GAME
        patterns = self.getPatterns()
        return patterns[0][(pos.color, 5, True)] > 0 or patterns[0][(pos.color, 5, False)] > 0

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
        # A piece was removed from the board, so return True
        return True

    ## Parses the board and populates dictionaries with data on the current state
    #   of the game board for each possible pattern. A pattern is a specific
    #   combination (encapsulated in a tuple) of the player's color, number of
    #   stones in a row, and a boolean denoting if a win is possible in this block.
    #       i.e. (playerColor, numberOfStones, canWin) -> ("RED", 5, True)
    #
    #  Returns a tuple of three dictionaries. In each dictionary, a pattern tuple,
    #   as described above, serves as the key and it maps to the following for each
    #   index of the tuple:
    #    [0] - count of each pattern present on the board
    #               i.e. patternCount[ ("RED", 4, True) ] = 1
    #    [1] - tuple containing the starting coordinates of the pattern, the
    #          direction in which the pattern goes, and the end coordinates
    #               i.e. patternStartingPos[ ("RED", 4, True) ] = [(2,3),(1,0),(6,3)]
    #    [2] - list of lists of possible moves that would complete a block in
    #          which that pattern is present
    #               i.e. patternMovesToComplete[ ("RED", 4, True) ]: [ [(1,3)] ]
    def getPatterns(self):
        # Range for the number of stones in a row to look for
        minStones = 1
        maxStones = 5

        possibleWin = [True, False]

        # Initialization of the return dictionaries
        patternCount = { (p,num,canWin):0 for p in [Gomoku.players[0],Gomoku.players[1]] \
                                for num in range(minStones,maxStones+1) for canWin in possibleWin }
        patternStartingPos = { (p,num,canWin):[] for p in [Gomoku.players[0],Gomoku.players[1]] \
                                for num in range(minStones,maxStones+1) for canWin in possibleWin }
        patternMovesToComplete = { (p,num,canWin): { adjacent: [] for adjacent in possibleWin }  \
                                for p in [Gomoku.players[0],Gomoku.players[1]] \
                                for num in range(minStones,maxStones+1) for canWin in possibleWin }

        # Add dictionary key to include fully empty block in search
        for canWin in possibleWin:
            patternCount[ (None, 5, canWin) ] = 0
            patternStartingPos[ (None, 5, canWin) ] = []

        # Right, down, diag-right-up, diag-right-down
        directions = [(1,0),(0,1),(1,-1),(1,1)]

        # Determines if the coordinates are out of bounds of the board
        def outOfBounds(pos):
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
        def nextPosition(pos, direction, reverse=False, length=1):
            if reverse:
                nextPos = (pos[0] - length * direction[0], pos[1] - length * direction[1])
            else:
                nextPos = (pos[0] + length * direction[0], pos[1] + length * direction[1])
            return nextPos if not outOfBounds(nextPos) else None

        # Determines whether the current pattern is present at the current
        #  coordinate position and in the current direction
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

            # If it is not the pattern-starting stone or if the pattern-ending
            #  stone would be out of bounds, return False
            if (not startsPattern and not winningBlockSearch) or endPosOOB:
                return False

            # If the stone one position past the number of stones in the current
            #  pattern belongs to the current player, the pattern is a subset of
            #  another longer pattern, so return False
            onePosPast = nextPosition(endPos, direction)
            if (onePosPast != None and self.board[onePosPast[0]][onePosPast[1]].color == player) and not (winningBlockSearch):
                return False

            # Check if pattern is present (with potential overlap)
            for i in range(num):
                # nextPos = nextPosition(curPos, direction)
                if self.board[curPos[0]][curPos[1]].color != player:
                    return False
                curPos = nextPosition(curPos, direction)

            # If looking for block in which a win is possible, return False.
            #  This will get populated by patternIsOpen().
            if canWin:
                return False
            return True

        # Takes in each pattern and checks if a win is still possible in that block
        def patternIsOpen(pattern, pos, direction):
            player, num, canWin = pattern

            # Go to the stones one position past each end point
            curCoord = nextPosition(pos, direction, length=num)
            prevCoord = nextPosition(pos, direction, reverse=True)
            if curCoord != None:
                curPos = self.board[curCoord[0]][curCoord[1]]
            if prevCoord != None:
                prevPos = self.board[prevCoord[0]][prevCoord[1]]

            spotsNecessary = 5 - num
            count = 0
            canWin = False

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

            # If the number of open positions in the possible blocks surrounding
            #  the pattern exceeds the number of stones necessary to complete the
            #  pattern, a win is possible with that pattern
            if count >= spotsNecessary:
                canWin = True
            return canWin

        # Returns a list of possible moves that will complete the current pattern
        def getMovesToComplete(pattern, pos, direction):
            player, num, canWin = pattern

            adjacentMoves = []
            nonadjacentMoves = []

            ## Check the adjacent positions first
            curCoord = nextPosition(pos, direction, length=num)
            prevCoord = nextPosition(pos, direction, reverse=True)

            # If the adjacent positions are not occupied, add them to the adjacent moves list
            if prevCoord != None:
                prevPos = self.board[prevCoord[0]][prevCoord[1]]
                if prevPos.color == None:
                    adjacentMoves.append(prevCoord)
                prevCoord = nextPosition(prevCoord, direction, reverse=True)

            if curCoord != None:
                curPos = self.board[curCoord[0]][curCoord[1]]
                if curPos.color == None:
                    adjacentMoves.append(curCoord)
                curCoord = nextPosition(curCoord, direction)


            # Set up the counter to find other possible moves
            spotsNecessaryForward = 5 - num - int(curCoord != None)
            spotsNecessaryReverse = 5 - num - int(prevCoord != None)
            count = 0

            # Set up the loop with the next positions in the forward and reverse directions
            if prevCoord != None:
                prevPos = self.board[prevCoord[0]][prevCoord[1]]
            if curCoord != None:
                curPos = self.board[curCoord[0]][curCoord[1]]

            forwardDone = False
            reverseDone = False

            while (count < spotsNecessaryForward + spotsNecessaryReverse):
                # First check the reverse direction
                if not reverseDone:
                    if prevCoord != None and (prevPos.color == player or prevPos.color == None):
                        prevPos = self.board[prevCoord[0]][prevCoord[1]]
                        if prevPos.color == None:
                            nonadjacentMoves.append(prevCoord)
                        count += 1
                        prevCoord = nextPosition(prevCoord, direction, reverse=True)
                    else:
                        reverseDone = True

                # Then check the forward direction
                if not forwardDone:
                    if curCoord != None and (curPos.color == player or curPos.color == None):
                        curPos = self.board[curCoord[0]][curCoord[1]]
                        if curPos.color == None:
                            nonadjacentMoves.append(curCoord)
                        count += 1
                        curCoord = nextPosition(curCoord, direction)
                    else:
                        forwardDone = True
                if forwardDone and reverseDone: break

            # possibleMoves = sorted(possibleMoves, key=itemgetter(1))

            # return sorted(possibleMoves, key=itemgetter(0))
            adjacents = (pos, direction, adjacentMoves)
            nonadjacents = (pos, direction, nonadjacentMoves)
            # adjacentMoves = sorted(adjacentMoves)
            # nonadjacentMoves = sorted(nonadjacentMoves)
            # return (adjacents, nonadjacents)
            return (adjacentMoves, nonadjacentMoves)


        """ --------------- DRIVER FOR getPatterns() --------------- """
        ## Go through each position on the board and look for each kind of pattern
        for x in range(self.dim):
            for y in range(self.dim):
                curPos = (x,y)
                # Go through every possible direction in which a pattern can point
                for direction in directions:
                    # Go through the two categories of patterns, winning and not winning ones
                    for canWin in possibleWin:
                        ## Find the empty 5 block patterns
                        if findPattern((None, 5, canWin), curPos, direction):
                            patternCount[(None, 5, canWin)] += 1
                            if (curPos, direction) not in (patternStartingPos[(None, 5, canWin)]):
                                patternStartingPos[(None, 5, canWin)].append((curPos, direction))
                            continue
                        # For every player (so just 2)
                        for player in Gomoku.players:
                            # For every number in the specified search range
                            for num in range(minStones, maxStones+1):
                                curPattern = (player, num, canWin)  # Finally can abbreviate pattern into a variable

                                # If the pattern exists at the current position and direction, continue
                                if findPattern(curPattern, curPos, direction):
                                    # Increment the pattern count
                                    patternCount[(player, num, canWin)] += 1
                                    # If this pattern is not yet in the dictionary containing the starting positions, add it
                                    if (curPos, direction) not in (patternStartingPos[curPattern]):
                                        endPos = nextPosition(curPos, direction, length=num-1)
                                        patternStartingPos[curPattern].append((curPos, endPos, direction))
                                    # If you can still win with this pattern, add it as a canWin pattern
                                    if patternIsOpen(curPattern, curPos, direction):
                                        patternCount[(player, num, True)] += 1
                                        patternCount[curPattern] -= 1
                                        # Remove this pattern as a non-winning key in each dictionary and add it as a winning key
                                        if (curPos, direction) not in (patternStartingPos[(player, num, True)]):
                                            patternStartingPos[(player, num, True)].append((curPos, endPos, direction))
                                            patternStartingPos[(player, num, False)].remove((curPos, endPos, direction))
                                            # Since a win is possible with this pattern, find the moves needed to complete it
                                            possibleMovesTuple = getMovesToComplete((player, num, canWin), curPos, direction)
                                            if possibleMovesTuple[0]: patternMovesToComplete[(player,num, True)][True].append(possibleMovesTuple[0])
                                            if possibleMovesTuple[1]: patternMovesToComplete[(player,num, True)][False].append(possibleMovesTuple[1])

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

    ## Checks if there are any empty squares in the board.
    #  This function was added to help the gui know when a draw
    #  has been reached and the minimax and alpha-beta agents know
    #  when to cut their search short.
    def boardIsFull(self):
        board = self.board
        for x in range(self.dim):
            for y in range(self.dim):
                if board[x][y].char == '.':
                    return False
        return True


    ## This function identifies if there is a win for either player, a draw,
    #  or neither.
    #
    #  If the red player has won, "RED" is returned.
    #  If the blue player has won, "BLUE" is returned.
    #  If there is a draw, "DRAW" is returned.
    #  If there is no victory or draw, a Nonetype is returned.
    def winOrDraw(self):
        patterns = self.getPatterns()
        patternCount = patterns[0]

        numBlueChainsOf5 = patternCount[("BLUE", 5, True)]
        numRedChainsOf5 = patternCount[("RED", 5, True)]

        if numBlueChainsOf5 > 0:
            return "BLUE"
        elif numRedChainsOf5 > 0:
            return "RED"
        elif self.boardIsFull():
            return "DRAW"
        else:
            return None
