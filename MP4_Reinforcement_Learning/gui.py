import pygame
import time
import loader
# from pong import Pong
# from Agents.human import Human

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

gameDisplay = None
x_paddle = 550
x_agent2_paddle = 0
old_y_paddle = 230
old_y_agent2_paddle = 230
old_x_ball = 280
old_y_ball = 280
radius = 10

def pong_gui(game, agent1 = None, agent2 = None):
	global gameDisplay
	gui_init(agent2)
	# print(agent1, agent2)
	# game loop
	while not game.game_is_over():
		game.update_time_step(False)
		update_display(game.get_state(), agent2)
		# wait() so it is visible to human eye
		time.sleep(.03)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				pygame.quit()
				quit()

def pong_expert_gui():
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

def gui_init(agent2 = None):
	global gameDisplay
	pygame.init()
	pygame.display.init()
	gameDisplay = pygame.display.set_mode((560, 560))
	pygame.display.set_caption('Pong')

	# draw walls and display
	gameDisplay.fill(white)
	if(agent2 is None):
		pygame.draw.rect(gameDisplay, black, [0, 0, 10, 560])	# left wall
	pygame.draw.rect(gameDisplay, black, [0, 0, 560, 10])	# top wall
	pygame.draw.rect(gameDisplay, black, [0, 550, 560, 10]) # bottom wall

	# draw paddle
	move_paddle(230)
	if(agent2 is not None):
		move_agent2_paddle(230)

	# draw ball
	old_x_ball = 280
	old_y_ball = 280
	move_ball(280, 280)

def update_display(pong_state, agent2 = None):
	# map the pong_state location to screen_location (multiply by 540 then add 10?)
	ball_x = int(pong_state[0]*520 + 20)
	ball_y = int(pong_state[1]*520 + 20)
	paddle_y = int(pong_state[4]*520 + 10)
	if(agent2 is not None):
		agent2_paddle_y = int(pong_state[5]*520 + 10)

	# refresh walls
	if(agent2 is None):
		pygame.draw.rect(gameDisplay, black, [0, 0, 10, 560])	# left wall
	pygame.draw.rect(gameDisplay, black, [0, 0, 560, 10])	# top wall
	pygame.draw.rect(gameDisplay, black, [0, 550, 560, 10]) # bottom wall

	# move_paddle
	move_paddle(paddle_y)
	if(agent2 is not None):
		move_agent2_paddle(agent2_paddle_y)
	pygame.display.update()

	# move_ball
	move_ball(ball_x, ball_y)
	
def move_paddle(y_coord):
	global gameDisplay, old_y_paddle
	pygame.draw.rect(gameDisplay, white, [x_paddle, old_y_paddle, 12, 100]) # clear old paddle
	pygame.draw.rect(gameDisplay, black, [x_paddle, y_coord, 12, 100]) # draw new paddle
	old_y_paddle = y_coord
	pygame.display.update()

def move_agent2_paddle(y_coord):
	global gameDisplay, old_y_agent2_paddle
	pygame.draw.rect(gameDisplay, white, [x_agent2_paddle, old_y_agent2_paddle, 10, 100]) # clear old paddle
	pygame.draw.rect(gameDisplay, blue, [x_agent2_paddle, y_coord, 10, 100]) # draw new paddle
	old_y_agent2_paddle = y_coord
	pygame.display.update()

def move_ball(x_coord, y_coord):
	global gameDisplay, old_x_ball, old_y_ball, radius
	pygame.draw.circle(gameDisplay, white, (old_x_ball, old_y_ball), radius) # clear old ball
	pygame.draw.circle(gameDisplay, red, (x_coord, y_coord), radius) # draw new ball
	old_x_ball = x_coord
	old_y_ball = y_coord
	pygame.display.update()

# pong_expert_gui()
