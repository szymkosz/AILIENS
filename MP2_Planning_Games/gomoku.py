import sys
from position import Position

## Used for formatting standard output
P1_COLOR = '\033[91m'
P2_COLOR = '\033[94m'
C_END = '\033[0m'

class Gomoku:
    ## Constructor
    def __init__(self, dim=7):
        self.curr_char = 'a'
        self.dim = dim
        self.reds_turn = True       ## Red always starts
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
                raise ValueError("Trying to set a {0}RED{2} piece when it is {1}BLUE{2}'s turn.".format(P1_COLOR, P2_COLOR, C_END))
            elif not red:
                raise ValueError("Trying to set a {1}BLUE{2} piece when it is {0}RED{2}'s turn.".format(P1_COLOR, P2_COLOR, C_END))

        # If setting a red piece and it is red's turn
        if red and self.reds_turn:

            # Set the position's char to the next red char and its color to "RED"
            # Switch the turn
            pos.char = self.curr_char
            pos.color = "RED"
            self.reds_turn = False

        # Else if setting a blue piece and it is blue's turn
        elif not red and not self.reds_turn:

            # Set the position's char to the next blue char and its color to "BLUE"
            # Switch the turn
            pos.char = self.curr_char.upper()
            pos.color = "BLUE"
            self.curr_char = chr(ord(self.curr_char) + 1)
            self.reds_turn = True
        return False

    ## Prints the state of the game to standard out
    def printBoard(self):
        board = self.board
        for i in range(len(board)):
            sys.stdout.write(' '.join(n.__repr__() for n in board[i]))
            sys.stdout.write("\n")
        sys.stdout.write("\n")

    ## Returns the state of the game as a single string
    def __str__(self):
        ret = ""
        board = self.board

        ## Numbers along top
        ret += "  " + ' '.join(str(i+1) for i in range(self.dim)) + "\n"
        for i in range(self.dim):
            ## First row is first number
            ret += str(i+1) + " " + ' '.join(n.__repr__() for n in board[i]) + "\n"

            ## First row is last number
            # ret += str(len(board) - i) + " " + ' '.join(n.__repr__() for n in board[i]) + "\n"

        ## Numbers along bottom
        # ret += "  " + ' '.join(str(i+1) for i in range(self.dim)) + "\n"
        return ret
