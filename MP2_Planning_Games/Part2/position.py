from colorama import Fore
from colorama import Style

## Used for formatting standard output
# P1_COLOR = '\033[91m'
# P2_COLOR = '\033[94m'
# C_END = '\033[0m'

class Position:
    colors = { "RED":    '\033[91m',
               "GREEN":  '\033[92m',
               "YELLOW": '\033[93m',
               "BLUE":   '\033[94m',
               "PURPLE": '\033[95m',
               "END":    '\033[0m'}

    ## Constructor
    def __init__(self):
        self.color = None   # Gets set to the appropriate string, "RED" or "BLUE"
        self.char = '.'

    ## Used for printing board array
    def __repr__(self):
        if self.char == '.':
            return self.char
        return Position.colors[self.color] + self.char + Position.colors["END"]

    def __str__(self):
        if self.char == '.':
            return self.char
        return Position.colors[self.color] + self.char + Position.colors["END"]
