import pygame
import time
from gomoku import Gomoku
from alphabeta import AlphaBeta 
from human import Human
from minimax import MiniMax 
from reflex import Reflex

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

coordinateList = [50, 160, 270, 380, 490, 600, 710, 820]

gameExit = False
win = False
gameDisplay = Human.gameDisplay
# how do I get access to the type of agent? and how do I get access to game without circular import statements?
Jon = Human(game, 1)
Jess = Reflex(game, 2)

if Human.boardInitialized == False:
	initializeBoard()

while not gameExit:
	# change gameloop to accomodate for other agents
	if Gomoku.reds_turn:
		# where do I get the coordinates to set the circle on the board?? 1) Jon.getPiece returns a position type which does not have coordinates,
		# and 2) setPiece gets its coordinates passed but I am not sure how these coordinates will be passed. I need access to these coordinates
		win = Jon.makeMove()
		pygame.draw.circle(gameDisplay, red, coordinates, 40)
	else:
		win = Jess.makeMove()
		pygame.draw.circle(gameDisplay, blue, coordinates, 40)
	pygame.display.update()

	if win == 1:
		if Gomoku.reds_turn:
			text = font.render("Red wins!", True, red)
		else:
			text = font.render("Blue wins!", True, blue)
		gameDisplay.blit(text, [385, 385])
		pygame.display.update()
		time.sleep(5)
		gameExit = True

	if event.type == pygame.QUIT:
		gameExit = True
			

pygame.quit()
quit()

def initializeBoard()
	pygame.init()
	gameDisplay = Human.gameDisplay
	gameDisplay = pygame.display.set_mode((870, 870))
	pygame.display.set_caption('Gomoku')
	# draw board
	gameDisplay.fill(white)
	for x in range(0, 8):
		pygame.draw.rect(gameDisplay, black, [110*x + 50, 50, 10, 770])
	for y in range(0, 8):
		pygame.draw.rect(gameDisplay, black, [50, 110*y + 50, 770, 10])
	pygame.display.update()
	# font
	font = pygame.font.SysFont(None, 100)
	Human.boardInitialized = True

# returns tuple of coordinates at center of the square
def boardToScreen(x, y):
	if(x<0 or y<0 or x>6 or y>6):
		return -1;

	screenX = 110*x + 105;
	screenY = 110*y + 105;
	return (screenX, screenY)

#returns tuple of board coordinates
def screenToBoard(x, y):
	if(x<50 or y<50 or x>820 or y>820):
		return -1;

	for i in range(0, 7):
		if x > coordinateList[6-i]:
			boardX = i 
		if  y > coordinateList[6-i]:
			boardY = i

	return (boardX, boardY)
