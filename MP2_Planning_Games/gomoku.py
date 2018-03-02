import sys
from position import Position

## Used for formatting standard output
P1_COLOR = '\033[91m'
P2_COLOR = '\033[94m'
C_END = '\033[0m'

players = ["RED", "BLUE"]

class Gomoku:
    ## Constructor
    def __init__(self, dim=7):
        self.curr_char = 'a'
        self.dim = dim
        self.reds_turn = True       # Red always starts
        self.board = [ [ Position() for i in range(dim) ] for i in range(dim) ]

    ## Sets the next piece at the desired coordinates (x,y).
    #   @param red - flag indicating the color of the piece to set
    #                True (1) for RED; False (0) for BLUE
    def setPiece(self, x, y, red):
        pos = self.board[x][y]

        # If the piece at (x,y) is empty
        if pos.char != '.':
            raise ValueError("Trying to set a piece in a non-empty position, char: " + str(pos.char))

        # Check to see if it is the turn of the player setting the piece
        if red != self.reds_turn:
            if red:
                raise ValueError("Trying to set a {0}{3[0]}{2} piece when it is {1}{3[1]}{2}'s turn.".format(P1_COLOR, P2_COLOR, C_END, players))
            elif not red:
                raise ValueError("Trying to set a {1}{3[1]}{2} piece when it is {0}{3[0]}{2}'s turn.".format(P1_COLOR, P2_COLOR, C_END, players))

        # If setting a red piece and it is red's turn
        if red and self.reds_turn:

            # Set the position's char to the next red char and its color to "RED"
            # Switch the turn
            pos.char = self.curr_char
            pos.color = players[0]
            self.reds_turn = False

        # Else if setting a blue piece and it is blue's turn
        elif not red and not self.reds_turn:

            # Set the position's char to the next blue char and its color to "BLUE"
            # Switch the turn
            pos.char = self.curr_char.upper()
            pos.color = players[1]
            self.curr_char = chr(ord(self.curr_char) + 1)
            self.reds_turn = True
        return False

    ## Parses the board and populates a dictionary specifying how many of each
    #   type of pattern is present on the current board.
    def getPatterns(self):
        # Initializes the dictionary { (player, numberOfStonesInARow, Open/Closed) : 0 }
        patterns = { (p,num,closed):0 for p in [players[0],players[1]] \
                                for num in range(3,6) for closed1 in [True,False] }
        patternStartingPos = patterns.copy()

        # Right, down, diag-right-up, diag-right-down
        directions = [(1,0),(0,1),(1,-1),(1,1)]

        def outOfBounds(self, pos):
            return pos[0] < 0 or pos[0] >= self.dim or pos[1] < 0 or pos[1] >= self.dim

        def nextPosition(self, pos, direction):
            nextPos = (pos[0] + direction[0], pos[1] + direction[1])
            return nextPos if not outOfBounds(nextPos) else None

        def findPattern(self, pattern, pos, direction):
            player, num, closed = pattern
            nextPos = pos
            exists = False
            count = 0
            # self.board[pos[0]][pos[1]].color == player
            for i in range(num):
                if self.board[nextPos[0]][nextPos[1]].color != player:
                    return False



        for player in players:
            for direction in directions:
                for num in range(2,6):


    ## Prints the state of the game to standard out
    def printBoard(self):
        board = self.board
        for i in range(len(board)):
            sys.stdout.write(' '.join(n[i].__repr__() for n in board))
            sys.stdout.write("\n")
        sys.stdout.write("\n")

    ## Returns the state of the game as a single string
    def __str__(self):
        ret = ""
        board = self.board

        ## Numbers along top
        ret += "  " + ' '.join(str(i+1) for i in range(self.dim)) + "\n"
        for i in range(self.dim):
            ## First row is top row
            ret += str(i+1) + " " + ' '.join(n[i].__repr__() for n in board) + "\n"

            ## First row is bottom row
            # ret += str(len(board) - i) + " " + ' '.join(n[i].__repr__() for n in board) + "\n"

        ## Numbers along bottom
        # ret += "  " + ' '.join(str(i+1) for i in range(self.dim)) + "\n"
        return ret
