from gomoku import Gomoku
import time

game = Gomoku()

game.printBoard()

# Random Moves
game.setPiece(3,4,1)
game.setPiece(3,3,0)
game.setPiece(4,5,1)
game.setPiece(4,3,0)
game.setPiece(5,3,1)

print(game)
