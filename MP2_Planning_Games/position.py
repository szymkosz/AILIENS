from colorama import Fore
from colorama import Style

class Position:
    ## Constructor
    def __init__(self):
        self.color = None   # Gets set to the appropriate string, "RED" or "BLUE"
        self.char = '.'

    ## Used for printing board array
    def __repr__(self):
        if self.color == "RED":
            return '\033[91m' + self.char + '\033[0m'
        elif self.color == "BLUE":
            return '\033[94m' + self.char + '\033[0m'
        return self.char

    def __str__(self):
        if self.color == "RED":
            return '\033[91m' + self.char + '\033[0m'
        elif self.color == "BLUE":
            return '\033[94m' + self.char + '\033[0m'
        return self.char
