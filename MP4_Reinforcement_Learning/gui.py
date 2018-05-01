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
x_paddle = 510
x_agent2_paddle = 10
old_y_paddle = 210
old_y_agent2_paddle = 210
old_x_ball = 260
old_y_ball = 260
radius = 10

def pong_gui(game, agent1 = None, agent2 = None):
	global gameDisplay
	gui_init(agent2)
	# game loop
	while not game.game_is_over():
		game.update_time_step(False)
		update_display(game.get_state())
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
	gameDisplay = pygame.display.set_mode((520, 520))
	pygame.display.set_caption('Pong')

	# draw walls and display
	gameDisplay.fill(white)
	if(agent2 == None):
		pygame.draw.rect(gameDisplay, black, [0, 0, 10, 520])	# left wall
	pygame.draw.rect(gameDisplay, black, [0, 0, 520, 10])	# top wall
	pygame.draw.rect(gameDisplay, black, [0, 510, 520, 10]) # bottom wall

	# draw paddle
	move_paddle(210)
	if(agent2 != None):
		move_agent2_paddle(210)

	# draw ball
	old_x_ball = 260
	old_y_ball = 260
	move_ball(260, 260)

def update_display(pong_state, agent2 = None):
	# map the pong_state location to screen_location (multiply by 500 then add 10?)
	ball_x = int(pong_state[0]*500 + 10)
	ball_y = int(pong_state[1]*500 + 10)
	paddle_y = int(pong_state[4]*500 + 10)
	if(agent2 != None):
		agent2_paddle_y = int(pong_state[5]*500 + 10)

	# refresh walls
	if(agent2 == None):
		pygame.draw.rect(gameDisplay, black, [0, 0, 10, 520])	# left wall
	pygame.draw.rect(gameDisplay, black, [0, 0, 520, 10])	# top wall
	pygame.draw.rect(gameDisplay, black, [0, 510, 520, 10]) # bottom wall

	# move_paddle
	move_paddle(paddle_y)
	if(agent2 != None):
		move_agent2_paddle(agent2_paddle_y)
	pygame.display.update()

	# move_ball
	move_ball(ball_x, ball_y)
	
def move_paddle(y_coord):
	global gameDisplay, old_y_paddle
	pygame.draw.rect(gameDisplay, white, [x_paddle, old_y_paddle, 10, 100]) # clear old paddle
	pygame.draw.rect(gameDisplay, black, [x_paddle, y_coord, 10, 100]) # draw new paddle
	old_y_paddle = y_coord
	pygame.display.update()

def move_agent2_paddle(y_coord):
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

pong_gui(game, agent1, agent2)
