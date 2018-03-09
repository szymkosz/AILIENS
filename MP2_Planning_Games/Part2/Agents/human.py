import pygame
import time
from gui import initializeBoard, boardToScreen, screenToBoard
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

	def makeMove(self):
		raise NotImplementedError()

	# returns an instance of type position
	def getMove(self):
		# get user clicking input
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONUP:
				screenX, screenY = pygame.mouse.get_pos()
				boardX, boardY = screenToBoard(screenX, screenY)
				pos = game.board[boardX][boardY]
				return pos
				


