import pygame
import time
#from gui import screenToBoard
from gomoku import Gomoku
from position import Position
from Agents.agent import Agent

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

coordinateList = [50, 160, 270, 380, 490, 600, 710]

class Human(Agent):
	def __init__(self, game=Gomoku(), playerNum=1):
		# super(self).__init__(game, playerNum)
		super().__init__(game, playerNum)
		self.name = "HUMAN"

	def makeMove(self):
		x, y = self.getMove()
		if self.playerNum == 1:
			self.game.setPiece(x, y, 1)
		elif self.playerNum == 2:
			self.game.setPiece(x, y, 0)



	# returns coordinates
	def getMove(self):
		# get user clicking input
		while(True):
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP:
					screenX, screenY = pygame.mouse.get_pos() # ??
					boardX, boardY = screenToBoard(screenX, screenY)
					if(boardX == -1 or boardY == -1):
						pass
					else:
						return (boardX, boardY)

				if event.type == pygame.QUIT:
					pygame.display.quit()
					pygame.quit()
					quit()
				
# returns tuple of board coordinates
def screenToBoard(x, y):
	print("screenToBoard: " + str(x) + ", " + str(y))
	if(x<50 or y<50 or x>820 or y>820):
		return (-1, -1);

	boardX = 0
	boardY = 0
	for i in range(0, 7):
		if x > coordinateList[6-i]:
			boardX = 6-i 
			break
	for j in range(0, 7):
		if  y > coordinateList[6-j]:
			boardY = 6-j
			break

	return (boardX, boardY)

