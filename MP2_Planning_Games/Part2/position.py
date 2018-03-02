from colorama import Fore
from colorama import Style

## Used for formatting standard output
P1_COLOR = '\033[91m'
P2_COLOR = '\033[94m'
C_END = '\033[0m'

class Position:
    ## Constructor
    def __init__(self):
        self.color = None   # Gets set to the appropriate string, "RED" or "BLUE"
        self.char = '.'

    ## Used for printing board array
    def __repr__(self):
        if self.color == "RED":
            return P1_COLOR + self.char + C_END
        elif self.color == "BLUE":
            return P2_COLOR + self.char + C_END
        return self.char

    def __str__(self):
        if self.color == "RED":
            return P1_COLOR + self.char + C_END
        elif self.color == "BLUE":
            return P2_COLOR + self.char + C_END
        return self.char
