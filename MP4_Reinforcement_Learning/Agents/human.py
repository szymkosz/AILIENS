# import sys, os
# sys.path.append(os.path.abspath(os.path.join('..', 'loader')))

import pygame
import time
import loader
from pong import Pong
from Agents.agent import Agent

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

gameDisplay = None
x_paddle = 510
x_human_paddle = 10
old_y_paddle = 210
old_y_human_paddle = 210

NAME = "HUMAN"

class Human(Agent):
	def __init__(self, game=Pong(), playerNum=1):
		# super(self).__init__(game, playerNum)
		super().__init__(game, playerNum)
		self.name = NAME
		# self.playerColor = ?


	def makeMove(self):
		# game loop
		for i in range(dataset.shape[0]):
			# update_display(dataset[i,:])
			# wait() so it is visible to human eye
		#while True:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP:
					garbage, y_human_paddle = pygame.mouse.get_pos()
				
				if event.type == pygame.QUIT:
					pygame.display.quit()
					pygame.quit()
					quit()

			time.sleep(.03)
			update_display(dataset[i,:])
		


	"""
    The getAction function should decide the action this agent should take
    given the state of self.game.  It should return 1 if the paddle should
    move up, -1 if the paddle should move down, or 0 if the paddle should do
    nothing.
    """
	def getAction(self):
		pass

	def pong_human_gui():
		global gameDisplay
		gui_init()
		dataset = loader.parser("Data/expert_policy.txt")[0]
		self.makeMove()


def gui_init():
	global gameDisplay
	# game = Pong()
	pygame.init()
	pygame.display.init()
	gameDisplay = pygame.display.set_mode((520, 520))
	pygame.display.set_caption('Pong')
	# draw board
	gameDisplay.fill(white)
	# pygame.draw.rect(gameDisplay, black, [0, 0, 10, 520])	# left wall
	pygame.draw.rect(gameDisplay, black, [0, 0, 520, 10])	# top wall
	pygame.draw.rect(gameDisplay, black, [0, 510, 520, 10]) # bottom wall
	# draw paddles
	move_paddle(210)
	move_human_paddle(210)
	# draw ball
	old_x_ball = 260
	old_y_ball = 260
	move_ball(260, 260)

def update_display(pong_state):
	# map the pong_state location to screen_location (multiply by 500 then add 10?)
	ball_x = int(pong_state[0]*500 + 10)
	ball_y = int(pong_state[1]*500 + 10)
	paddle_y = int(pong_state[4]*500 + 10)
	# move ball and paddles
	move_ball(ball_x, ball_y)
	move_paddle(paddle_y)
	move_human_paddle(human_paddle_y)
	# pygame.draw.rect(gameDisplay, black, [0, 0, 10, 520])	# left wall
	pygame.draw.rect(gameDisplay, black, [0, 0, 520, 10])	# top wall
	pygame.draw.rect(gameDisplay, black, [0, 510, 520, 10]) # bottom wall
	pygame.display.update()

def move_paddle(y_coord):
	pygame.draw.rect(gameDisplay, white, [x_paddle, old_y_paddle, 10, 100]) # clear old paddle
	pygame.draw.rect(gameDisplay, black, [x_paddle, y_coord, 10, 100]) # draw new paddle
	old_y_paddle = y_coord
	pygame.display.update()

def move_human_paddle(y_coord):
	pygame.draw.rect(gameDisplay, white, [x_human_paddle, old_y_human_paddle, 10, 100]) # clear old paddle
	pygame.draw.rect(gameDisplay, blue, [x_human_paddle, y_coord, 10, 100]) # draw new paddle
	old_y_human_paddle = y_coord
	pygame.display.update()
