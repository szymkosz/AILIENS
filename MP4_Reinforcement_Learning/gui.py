import pygame
import time
import loader
# from pong import Pong
# from Agents.human import Human

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

gameDisplay = None
x_paddle = 510
old_y_paddle = 210
old_x_ball = 260
old_y_ball = 260
radius = 10

def pong_gui():
	global gameDisplay
	gui_init()
	dataset = loader.parser("Data/expert_policy.txt")[0]
	# game loop
	for i in range(dataset.shape[0]):
		update_display(dataset[i,:])
		# wait() so it is visible to human eye
		time.sleep(.03)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				pygame.quit()
				quit()

def gui_init():
	global gameDisplay
	# game = Pong()
	pygame.init()
	pygame.display.init()
	gameDisplay = pygame.display.set_mode((520, 520))
	pygame.display.set_caption('Pong')
	# draw board
	gameDisplay.fill(white)
	pygame.draw.rect(gameDisplay, black, [0, 0, 10, 520])	# left wall
	pygame.draw.rect(gameDisplay, black, [0, 0, 520, 10])	# top wall
	pygame.draw.rect(gameDisplay, black, [0, 510, 520, 10]) # bottom wall
	# draw paddle
	move_paddle(210)
	# draw ball
	old_x_ball = 260
	old_y_ball = 260
	move_ball(260, 260)

def update_display(pong_state):
	# map the pong_state location to screen_location (multiply by 500 then add 10?)
	ball_x = int(pong_state[0]*500 + 10)
	ball_y = int(pong_state[1]*500 + 10)
	paddle_y = int(pong_state[4]*500 + 10)
	# move_ball
	move_ball(ball_x, ball_y)
	# move_paddle
	move_paddle(paddle_y)
	pygame.draw.rect(gameDisplay, black, [0, 0, 10, 520])	# left wall
	pygame.draw.rect(gameDisplay, black, [0, 0, 520, 10])	# top wall
	pygame.draw.rect(gameDisplay, black, [0, 510, 520, 10]) # bottom wall
	pygame.display.update()

def move_paddle(y_coord):
	global gameDisplay, old_y_paddle
	pygame.draw.rect(gameDisplay, white, [x_paddle, old_y_paddle, 10, 100]) # clear old paddle
	pygame.draw.rect(gameDisplay, black, [x_paddle, y_coord, 10, 100]) # draw new paddle
	old_y_paddle = y_coord
	pygame.display.update()

def move_ball(x_coord, y_coord):
	global gameDisplay, old_x_ball, old_y_ball, radius
	pygame.draw.circle(gameDisplay, white, (old_x_ball, old_y_ball), radius) # clear old ball
	pygame.draw.circle(gameDisplay, red, (x_coord, y_coord), radius) # draw new ball
	old_x_ball = x_coord
	old_y_ball = y_coord
	pygame.display.update()

pong_gui()
