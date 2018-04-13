import pygame
import time
#from gui import screenToBoard
from pong import Pong
from Agents.agent import Agent

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

NAME = "HUMAN"

class Human(Agent):
	def __init__(self, game=Pong(), playerNum=1):
		# super(self).__init__(game, playerNum)
		super().__init__(game, playerNum)
		self.name = NAME
		# self.playerColor = ?


	def makeMove(self):
		x, y = self.getMove()
		if self.playerNum == 1:
			return self.game.setPiece(x, y, 1, isHuman=True)
		elif self.playerNum == 2:
			return self.game.setPiece(x, y, 0, isHuman=True)


	"""
    The getAction function should decide the action this agent should take
    given the state of self.game.  It should return 1 if the paddle should
    move up, -1 if the paddle should move down, or 0 if the paddle should do
    nothing.
    """
	def getAction(self):
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
