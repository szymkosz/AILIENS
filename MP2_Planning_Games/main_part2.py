from gomoku import Gomoku

game = Gomoku()

print(game)

moves = [(3, 4), (3, 3), (4, 5), (4, 3), (5, 3)]

# Random Moves
for m in moves:
    game.setPiece(m[0], m[1], game.reds_turn)

game.setPiece(5,5, game.reds_turn)

# game.setPiece(4,4,not game.reds_turn)

print(game)
