import pygame
import time
from gomoku import Gomoku
from alphabeta import AlphaBeta 
from human import Human
from minimax import MiniMax 
from reflex import Reflex

# parse the board instead of looking for x, y input

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

coordinateList = [50, 160, 270, 380, 490, 600, 710]

class GUI(object):
	boardInitialized = False
	gameDisplay = None
	keepPlaying = True
	gameExit = False
	win = False

	def __init__(self, game=Gomoku())
	# check if the board has been initalized 
	if boardInitialized == False:
		pygame.init()
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
		bigFont = pygame.font.SysFont(None, 100)
		littleFont = pygame.font.SysFont(None, 25)
		boardInitialized = True

	def gameLoop(self):
		while not gameExit:
			if keepPlaying == True:
				if Gomoku.reds_turn:
					win = Jon.makeMove()
				else:
					win = Jess.makeMove()
					
				self.refreshBoard()

			# if there is a winner, print winner to screen
			if win == 1:
				if Gomoku.reds_turn:
					text = bigFont.render("Blue wins!", True, blue)
				else:
					text = bigFont.render("Red wins!", True, red)
				gameDisplay.blit(text, [385, 385])
				pygame.display.update()
				keepPlaying = False

			if event.type == pygame.QUIT:
				gameExit = True
					
		pygame.quit()
		quit()

	def refreshBoard()
		# parse the board to get coordinates
		board = Gomoku.board
		for x in range(0, 7):
			for y in range(0, 7):
				pos = board[x][y]
				if not pos.char == '.':
					# print the piece with the corresponding colors
					screenX, screenY = self.boardToScreen(x, y)
					if pos.color == "RED":
						pygame.draw.circle(gameDisplay, red, (screenX, screenY), 40)
					if pos.color == "BLUE":
						pygame.draw.circle(gameDisplay, blue, (screenX, screenY), 40)
					# print the corresponding character on the piece
					char = pos.char
					pieceChar = littleFont.render(char, True, white)
					gameDisplay.blit(pieceChar, [screenX, screenY])
					
		# refresh the board display
		pygame.display.update()

	# returns tuple of coordinates at center of the square
	def boardToScreen(self, x, y):
		if(x<0 or y<0 or x>6 or y>6):
			return -1;

		screenX = 110*x + 105;
		screenY = 110*y + 105;
		return (screenX, screenY)

	# returns tuple of board coordinates
	def screenToBoard(self, x, y):
		if(x<50 or y<50 or x>820 or y>820):
			return -1;

		for i in range(0, 7):
			if x > coordinateList[6-i]:
				boardX = 6-i 
			if  y > coordinateList[6-i]:
				boardY = 6-i

		return (boardX, boardY)
