import pygame
import time
from pong import Pong
from Agents.agent import Agent

NAME = "HUMAN"

class Human(Agent):
	def __init__(self, game=Pong(), playerNum=1):
		# super(self).__init__(game, playerNum)
		super().__init__(game, playerNum)
		self.name = NAME
		# self.playerColor = ?

	"""
    The updateAction function is largely responsible for the agent's learning.
    It updates the agent's parameters given the state s, the action a taken in
    state s, the reward of taking action a in state s, and the resulting state
    s_prime (s').  It computes the action a' to take from state s' and performs
    the TD update as appropriate.

    Nothing is returned.
    """
	def updateAction(self, s, a, reward, s_prime):
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

