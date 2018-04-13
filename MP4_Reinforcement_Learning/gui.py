import pygame
import time
from pong import Pong
# from Agents.human import Human

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

x_paddle = 510
old_y_paddle = 210
old_x_ball = 260
old_y_ball = 260
radius = 10

def pong_gui():
	gui_init()
	# game loop
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				pygame.quit()
				quit()


def gui_init():
	game = Pong()
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
	move_ball()

def move_paddle(y_coord)
	pygame.draw.rect(gameDisplay, white, [x_paddle, old_y_coord, 10, 100]) # clear old paddle
	pygame.draw.rect(gameDisplay, black, [x_paddle, y_coord, 10, 100]) # draw new paddle
	old_y_paddle = y_coord
	pygame.display.update()

def move_ball(x_coord, y_coord)
	pygame.draw.circle(gameDisplay, white, (old_x_ball, old_y_ball), radius) # clear old ball
	pygame.draw.circle(gameDisplay, red, (x_coord, y_coord), radius) # draw new ball
	old_x_ball = x_coord
	old_y_ball = y_coord
	pygame.display.update()

pong_gui()

# -----------------------------------------------------------------------------------
# boardInitialized = False
# gameDisplay = None
# keepPlaying = True
# gameExit = False
# win = False

# # check if the board has been initalized
# if boardInitialized == False:
# 	pygame.init()
# 	pygame.display.init()
# 	gameDisplay = pygame.display.set_mode((870, 940))
# 	pygame.display.set_caption('Gomoku')
# 	# draw board
# 	gameDisplay.fill(white)
# 	for x in range(0, 8):
# 		pygame.draw.rect(gameDisplay, black, [110*x + 50, 50, 10, 780])
# 	for y in range(0, 8):
# 		pygame.draw.rect(gameDisplay, black, [50, 110*y + 50, 780, 10])
# 	pygame.display.update()
# 	bigFont = pygame.font.SysFont(None, 100)
# 	littleFont = pygame.font.SysFont(None, 35)
# 	boardInitialized = True
# 	gameDisplay = pygame.transform.scale(gameDisplay, (556, 600))


# def refreshBoard():
# 	# parse the board to get coordinates
# 	board = game.board
# 	for x in range(0, 7):
# 		for y in range(0, 7):
# 			pos = board[x][y]
# 			if not pos.char == '.':
# 				# print the piece with the corresponding colors
# 				screenX, screenY = boardToScreen(x, y)
# 				if pos.color == "RED":
# 					pygame.draw.circle(gameDisplay, red, (screenX+5, screenY+5), 40)
# 				if pos.color == "BLUE":
# 					pygame.draw.circle(gameDisplay, blue, (screenX+5, screenY+5), 40)
# 				# print the corresponding character on the piece
# 				char = pos.char
# 				pieceChar = littleFont.render(char, True, white)
# 				gameDisplay.blit(pieceChar, [screenX-2, screenY-5])

# 	# refresh the board display
# 	pygame.display.update()

# while not gameExit:
# 	if keepPlaying == True:
# 		if game.reds_turn:
# 			win = Jon.makeMove()
# 		else:
# 			win = Jess.makeMove()

# 		refreshBoard()

# 	# check for draws
# 	if game.boardIsFull():
# 		text = bigFont.render("DRAW!", True, black)

# 		text_X = 430 - (text.get_width()/2)
# 		gameDisplay.blit(text, [text_X, 860])
# 		pygame.display.update()
# 		keepPlaying = False

# 	# if there is a winner, print winner to screen
# 	if win == True:
# 		if game.reds_turn:
# 			text = bigFont.render("BLUE WINS!", True, blue)
# 		else:
# 			text = bigFont.render("RED WINS!", True, red)

# 		text_X = 430 - (text.get_width()/2)
# 		gameDisplay.blit(text, [text_X, 860])
# 		pygame.display.update()
# 		keepPlaying = False

# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			gameExit = True

# if gameExit == True:
# 	pygame.display.quit()
# 	pygame.quit()
# 	quit()

# # refreshBoard

# # boardToScreen

# # screenToBoard
