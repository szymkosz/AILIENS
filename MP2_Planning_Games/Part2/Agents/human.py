import pygame
import time
from gomoku import Gomoku
from position import Position
from agent import Agent

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

class Human(Agent):
	boardInitialized = False
	gameDisplay = None

	def __init__(self, game=Gomoku(), playerNum=1):
		super().__init__(game, playerNum)
		self.name = "HUMAN"
		if not Human.boardInitialized:
			initializeBoard()

	def initializeBoard(self):
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

	def makeMove(self):
		raise NotImplementedError()

	def getMove(self):
		# get user clicking input

	# game loop
		gameExit = False
		win = False
		gameDisplay = Human.gameDisplay

		while not gameExit:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP:
					mouse_pos = pygame.mouse.get_pos()
					# which square did the user click? How do I coordinate this with the board already made, and how can I do a check for if the space is already occupied?
					# square should be a tuple of the center of the square

					# draw the corresponding circle in the corresponding square
					if Gomoku.reds_turn:
						pygame.draw.circle(gameDisplay, red, square, 40)
					else:
						pygame.draw.circle(gameDisplay, blue, square, 40)
					pygame.display.update()

					# make move and check for a human win... 1) do I call setPiece? - NO 2) how to print text if opponent wins??
					win = Gomoku.setPiece(square[0], square[1], Gomoku.reds_turn)
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

# add button to end game or play again if time

