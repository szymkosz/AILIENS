import pygame
import time
from pong import Pong
from Agents.agent import Agent

NAME = "HUMAN"

class human(Agent):
	def __init__(self, playerNum=1):
		# super(self).__init__(game, playerNum)
		super().__init__(NAME, playerNum)
		self.name = NAME

	"""
    The getAction function should decide the action this agent should take
    given the state of self.game.  It should return 1 if the paddle should
    move up, -1 if the paddle should move down, or 0 if the paddle should do
    nothing.
    """
	def getAction(self, is_training = False, cur_state_tuple = None):
		garbage, y_human_paddle = pygame.mouse.get_pos()
		screen_paddle = (y_human_paddle - 10)/500
		return screen_paddle

	"""
    The updateAction function is largely responsible for the agent's learning.
    It updates the agent's parameters given the state s, the action a taken in
    state s, the reward of taking action a in state s, and the resulting state
    s_prime (s').  It computes the action a' to take from state s' and performs
    the TD update as appropriate.

    Nothing is returned.
    """
	def updateAction(self, s, a, reward, s_prime):
		pass

