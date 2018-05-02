import sys
import helper
from Agents import *
import numpy as np
from pong import Pong

# CONSTANTS
LEFT_WALL_X = 0.0
RIGHT_WALL_X = 1.0
TOP_WALL_Y = 0.0
BOTTOM_WALL_Y = 1.0
PADDLE_HEIGHT = 0.2

# CONSTANTS FOR INITIALIZING GAME
INITIAL_BALL_X = 0.5
INITIAL_BALL_Y = 0.5
INITIAL_VELOCITY_X = 0.03
INITIAL_VELOCITY_Y = 0.01
INITIAL_PADDLE_Y = 0.5 - (PADDLE_HEIGHT/2)


class Two_Player_Pong(Pong):
    """
    This is the constructor for a 2-player Pong game.  By default, the setup of the game
    is identical to the initial state defined in the assignment.  The game's
    agents should always be passed in as the appropriate object.
    """
    def __init__(self, agent, agent2, ball_x=INITIAL_BALL_X, ball_y=INITIAL_BALL_Y, velocity_x=INITIAL_VELOCITY_X, velocity_y=INITIAL_VELOCITY_Y, paddle_y=INITIAL_PADDLE_Y, paddle2_y=INITIAL_PADDLE_Y):
        # Initialize the first agent and game state
        super().__init__(agent, ball_x, ball_y, velocity_x, velocity_y, paddle_y)

        # Initialize the second agent and the player scores
        self.agent2 = agent2
        self.paddle2_y = paddle2_y


    """
    The update_time_step function is responsible for updating the state of the game
    with every time step.  It gets the agent's action, uses it to update the paddle's
    position, updates the ball's position, and then handles the bouncing of the ball.

    Nothing is returned here, and the is_training parameter isn't used.
    """
    def update_time_step(self, is_training):
        # Get player 1's action and update player 1's paddle
        if self.agent.name.lower() == "human":
            action = self.agent.getAction()
            self.paddle_y = self.move_paddle(True, self.paddle_y, action)
        else:
            cur_state_tuple = (self.ball_x, self.ball_y, self.velocity_x, self.velocity_y, self.paddle_y)
            action = self.agent.getAction(False, cur_state_tuple)
            self.paddle_y = self.move_paddle(False, self.paddle_y, action)

        # Get player 2's action and update player 2's paddle
        if self.agent2.name.lower() == "human":
            action = self.agent2.getAction()
            self.paddle2_y = self.move_paddle(True, self.paddle2_y, action)
        else:
            cur_state_tuple = (self.ball_x, self.ball_y, self.velocity_x, self.velocity_y, self.paddle2_y)
            action = self.agent2.getAction(False, cur_state_tuple)
            self.paddle2_y = self.move_paddle(False, self.paddle2_y, action)

        # Update the ball's position
        self.ball_x += self.velocity_x
        self.ball_y += self.velocity_y

        # Handle the bouncing of the ball
        self.handle_bounce()

        return None


    def move_paddle(self, isHuman, initial_paddle_y, action):
        # Determine the paddle's new y-coordinate
        paddle_y = initial_paddle_y
        if isHuman:
            # Since this is the paddle of a human agent, set the paddle's
            # y-coordinate to the action (the y-coordinate of the mouse cursor)
            paddle_y = action
        else:
            # Since this is not the paddle of a human agent, raise or
            # lower the paddle's position based on the agent's action
            if action == 2:
                paddle_y += 0.04
            elif action == 0:
                paddle_y -= 0.04

        # Reset the paddle position if the paddle
        # tries to move off the top of the screen
        if paddle_y < 0:
            return 0
        # Reset the paddle position if the paddle tries
        # to move off the bottom of the screen
        elif (paddle_y + PADDLE_HEIGHT) > 1:
            return (1 - PADDLE_HEIGHT)
        else:
            return paddle_y


    """
    The handle_bounce function handles the bouncing of the ball off of the walls and paddle.
    """
    def handle_bounce(self):
        # Handles bouncing off the walls
        if self.ball_y < TOP_WALL_Y:
            self.ball_y *= -1
            self.velocity_y *= -1
        if self.ball_y > BOTTOM_WALL_Y:
            self.ball_y = 2 - self.ball_y
            self.velocity_y *= -1

        # Handles bouncing off the right paddle
        if self.ball_x > RIGHT_WALL_X:
            if (self.ball_y >= self.paddle_y and self.ball_y <= (self.paddle_y + PADDLE_HEIGHT)):
                self.ball_x = 2 - self.ball_x

                candidate_velocity_x = self.velocity_x - np.random.uniform(low=-0.015, high=0.015)
                self.velocity_x = -1*min(max(candidate_velocity_x, 0.03), 1)

                candidate_velocity_y = self.velocity_y + np.random.uniform(low=-0.03, high=0.03)
                sign = 1
                if candidate_velocity_y < 0:
                    sign = -1

                self.velocity_y = sign*min(abs(candidate_velocity_y), 1)

        # Handles bouncing off the left paddle
        if self.ball_x < LEFT_WALL_X:
            if (self.ball_y >= self.paddle2_y and self.ball_y <= (self.paddle2_y + PADDLE_HEIGHT)):
                self.ball_x *= -1

                candidate_velocity_x = -1*self.velocity_x + np.random.uniform(low=-0.015, high=0.015)
                self.velocity_x = min(max(candidate_velocity_x, 0.03), 1)

                candidate_velocity_y = self.velocity_y + np.random.uniform(low=-0.03, high=0.03)
                sign = 1
                if candidate_velocity_y < 0:
                    sign = -1

                self.velocity_y = sign*min(abs(candidate_velocity_y), 1)


    """
    The run_multiple_games function is responsible for running multiple games
    to play the part1 and part2 agents against each other.

    The is_training parameter isn't used here.
    """
    def run_multiple_games(self, num_games, is_training):
        agent1_wins = 0
        agent2_wins = 0

        for i in range(num_games):
            while not self.game_is_over():
                self.update_time_step(None)

            assert (self.ball_x > RIGHT_WALL_X or self.ball_x < LEFT_WALL_X), \
                   "ERROR: Game ended and the ball hasn't left the game"

            if self.ball_x > RIGHT_WALL_X:
                agent1_wins += 1
            else:
                agent2_wins += 1

            self.reset_game()

        print("Number of Player 1 Victories: " + str(agent1_wins))
        print("Number of Player 2 Victories: " + str(agent2_wins))

        return None


    """
    The game_is_over function checks if the ball has left the screen and therefore,
    the Pong game has ended.
    """
    def game_is_over(self):
        if self.ball_x > RIGHT_WALL_X and (self.ball_y < self.paddle_y or self.ball_y > (self.paddle_y + PADDLE_HEIGHT)):
            return True
        elif self.ball_x < LEFT_WALL_X and (self.ball_y < self.paddle2_y or self.ball_y > (self.paddle2_y + PADDLE_HEIGHT)):
            return True
        return False


    """
    The reset_game function resets the position and velocity of the ball and
    the positions of the paddles for starting a new game.  The parameters make it
    possible to reset these variables differently, but they will be set to the
    initial state defined in the assignment by default.  This means paddle2_y
    will also be set to the default value of paddle_y by default.
    """
    def reset_game(self, ball_x=INITIAL_BALL_X, ball_y=INITIAL_BALL_Y, velocity_x=INITIAL_VELOCITY_X, velocity_y=INITIAL_VELOCITY_Y, paddle_y=INITIAL_PADDLE_Y, paddle2_y=INITIAL_PADDLE_Y):
        super().reset_game(ball_x, ball_y, velocity_x, velocity_y, paddle_y)
        self.paddle2_y = paddle2_y


    """
    For a 2-player Pong game, the get_state function returns a 6-tuple of the
    attributes of the game's state as:

    (ball_x, ball_y, velocity_x, velocity_y, paddle_y, paddle2_y)

    where the first 5 entries are the same 5 atributes of a single-player Pong game
    and paddle2_y is the y-coordinate of the top of player 2's paddle.
    """
    def get_state(self):
        return (self.ball_x, self.ball_y, self.velocity_x, self.velocity_y, self.paddle_y, self.paddle2_y)


    """
    This returns a string representation of the 2-player game in the form:

    "Agent 1: <self.agent.name>  Agent2: <self.agent2.name>  " +
    "State: <(self.ball_x, self.ball_y, self.velocity_x, self.velocity_y, self.paddle_y, self.paddle2_y)>".
    """
    def __str__(self):
        state = self.get_state()
        ret = "Agent 1: " + self.agent.name + "  Agent2: " + self.agent2.name + "  State: " + str(state)
        return ret
