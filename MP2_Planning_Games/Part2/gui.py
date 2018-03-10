import pygame
import time
from gomoku import Gomoku
# from alphabeta import AlphaBeta 
from Agents.human import Human
# from minimax import MiniMax 
# from reflex import Reflex

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

coordinateList = [50, 160, 270, 380, 490, 600, 710]

boardInitialized = False
gameDisplay = None
keepPlaying = True
gameExit = False
win = False

game = Gomoku()
Jon = Human(game, 1)
Jess = Human(game, 2)
# check if the board has been initalized 
if boardInitialized == False:
	pygame.init()
	pygame.display.init()
	gameDisplay = pygame.display.set_mode((870, 940))
	pygame.display.set_caption('Gomoku')
	# draw board
	gameDisplay.fill(white)
	# pygame.display.update() #
	#time.sleep(10) #
	for x in range(0, 8):
		pygame.draw.rect(gameDisplay, black, [110*x + 50, 50, 10, 780])
	for y in range(0, 8):
		pygame.draw.rect(gameDisplay, black, [50, 110*y + 50, 780, 10])
	pygame.display.update()
	# time.sleep(10) #
	# font
	bigFont = pygame.font.SysFont(None, 100)
	littleFont = pygame.font.SysFont(None, 35)
	boardInitialized = True
	# gameLoop(self)

# returns tuple of coordinates at center of the square
def boardToScreen(x, y):
	if(x<0 or y<0 or x>6 or y>6):
		return -1;

	screenX = 110*x + 105;
	screenY = 110*y + 105;
	return (screenX, screenY)

def refreshBoard():
	# parse the board to get coordinates
	board = game.board
	for x in range(0, 7):
		for y in range(0, 7):
			pos = board[x][y]
			if not pos.char == '.':
				# print the piece with the corresponding colors
				screenX, screenY = boardToScreen(x, y)
				if pos.color == "RED":
					pygame.draw.circle(gameDisplay, red, (screenX+5, screenY+5), 40)
				if pos.color == "BLUE":
					pygame.draw.circle(gameDisplay, blue, (screenX+5, screenY+5), 40)
				# print the corresponding character on the piece
				char = pos.char
				pieceChar = littleFont.render(char, True, white)
				gameDisplay.blit(pieceChar, [screenX-2, screenY-5])
					
	# refresh the board display
	pygame.display.update()

while not gameExit:
	if keepPlaying == True:
		if game.reds_turn:
			win = Jon.makeMove()
		else:
			win = Jess.makeMove()
					
		refreshBoard()

	# check for draws
	if game.boardIsFull():
		text = bigFont.render("DRAW!", True, black)

		text_X = 430 - (text.get_width()/2)
		gameDisplay.blit(text, [text_X, 860])
		pygame.display.update()
		keepPlaying = False

	# if there is a winner, print winner to screen
	if win == True:
		if game.reds_turn:
			text = bigFont.render("BLUE WINS!", True, blue)
		else:
			text = bigFont.render("RED WINS!", True, red)

		text_X = 430 - (text.get_width()/2)
		gameDisplay.blit(text, [text_X, 860])
		pygame.display.update()
		keepPlaying = False

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True
				
if gameExit == True:	
	pygame.display.quit()
	pygame.quit()
	quit()

# refreshBoard

# boardToScreen

# screenToBoard
