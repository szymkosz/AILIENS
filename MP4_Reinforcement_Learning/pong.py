import sys
import helper

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

class Pong(object):
    """
    This is the constructor for a Pong game.  By default, the setup of the game
    is identical to the initial state defined in the assignment.  The game's
    agent should always be passed in as the appropriate object.
    """
    def __init__(self, agent, ball_x=INITIAL_BALL_X, ball_y=INITIAL_BALL_Y, velocity_x=INITIAL_VELOCITY_X, velocity_y=INITIAL_VELOCITY_Y, paddle_y=INITIAL_PADDLE_Y):
        # Check that velocity_x and velocity_y are valid
        if abs(velocity_x) < 0.03:
            raise ValueError("Absolute value of velocity_x must be greater than or equal to 0.03!")
        elif abs(velocity_x) > 1.0:
            raise ValueError("Absolute value of velocity_x must be less than or equal to 1!")
        elif abs(velocity_y) > 1.0:
            raise ValueError("Absolute value of velocity_y must be less than or equal to 1!")

        # Initialize the agent
        self.agent = agent

        # Initialize the game state
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.paddle_y = paddle_y


    """
    The update_time_step function is responsible for updating the state of the game
    with every time step.  It gets the agent's action, uses it to update the paddle's
    position, updates the ball's position, and then handles the bouncing of the ball.
    """
    def update_time_step(self, is_training):
        # Get the action of the agent
        cur_state_tuple = (self.ball_x, self.ball_y, self.velocity_x, self.velocity_y, self.paddle_y)
        action = self.agent.getAction(is_training, cur_state_tuple)

        # Update the paddle's position based on the agent's action
        if action == 1:
            self.paddle_y += 0.04

            # Reset the paddle position if the paddle
            # tries to move off the top of the screen
            if self.paddle_y < 0:
                self.paddle_y = 0
        elif action == -1:
            self.paddle_y -= 0.04

            # Reset the paddle position if the paddle tries
            # to move off the bottom of the screen
            if (self.paddle_y + PADDLE_HEIGHT) > 1:
                self.paddle_y = (1 - PADDLE_HEIGHT)

        # Update the ball's position
        self.ball_x += self.velocity_x
        self.ball_y += self.velocity_y

        # Handle the bouncing of the ball
        self.handle_bounce()

        # Update the agent's parameters if it's being trained
        if is_training:
            new_state_tuple = (self.ball_x, self.ball_y, self.velocity_x, self.velocity_y, self.paddle_y)
            self.agent.updateAction(cur_state_tuple, action, new_state_tuple)


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
        if self.ball_x < LEFT_WALL_X:
            self.ball_x *= -1
            self.velocity_x *= -1

        # Handles bouncing off the paddle
        if self.ball_x > RIGHT_WALL_X and (self.ball_y >= self.paddle_y and self.ball_y <= (self.paddle_y + PADDLE_HEIGHT)):
            self.ball_x = 2 - self.ball_x

            candidate_velocity_x = self.velocity_x - np.random.uniform(low=-0.015, high=0.015)
            self.velocity_x = -1*np.min(np.max(candidate_velocity_x, 0.03), 1)

            candidate_velocity_y = self.velocity_y + np.random.uniform(low=-0.03, high=0.03)
            sign = 1
            if candidate_velocity_y < 0:
                sign = -1

            self.velocity_y = sign*np.min(abs(candidate_velocity_y), 1)


    """
    The run_multiple_games function is responsible for running multiple games
    to either train the agent or test it.

    Set the is_training parameter to True if these games are for training the agent
    or False if these games are for testing the agent.
    """
    def run_multiple_games(self, num_games, is_training):
        for i in range(num_games):
            while not self.game_is_over():
                self.update_time_step(is_training)

            self.reset_game()


    """
    The game_is_over function checks if the ball has left the screen and therefore,
    the Pong game has ended.  This is determined by checking if the ball's x-coordinate
    is greater than 1 and the ball's y-coordinate is either less than the paddle's
    y-coordinate or greater than the paddle's y-coordinate plus the height of the paddle.
    """
    def game_is_over(self):
        if self.ball_x > RIGHT_WALL_X and (self.ball_y < self.paddle_y or self.ball_y > (self.paddle_y + PADDLE_HEIGHT)):
            return True
        else:
            return False


    """
    The reset_game function resets the position and velocity of the ball and
    the position of the paddle for starting a new game.  The parameters make it
    possible to reset these variables differently, but they will be set to the
    initial state defined in the assignment by default.
    """
    def reset_game(self, ball_x=INITIAL_BALL_X, ball_y=INITIAL_BALL_Y, velocity_x=INITIAL_VELOCITY_X, velocity_y=INITIAL_VELOCITY_Y, paddle_y=INITIAL_PADDLE_Y)):
        # Check that velocity_x and velocity_y are valid
        if abs(velocity_x) < 0.03:
            raise ValueError("Absolute value of velocity_x must be greater than or equal to 0.03!")
        elif abs(velocity_x) > 1.0:
            raise ValueError("Absolute value of velocity_x must be less than or equal to 1!")
        elif abs(velocity_y) > 1.0:
            raise ValueError("Absolute value of velocity_y must be less than or equal to 1!")

        # Reset the game state
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.paddle_y = paddle_y


    """
    This returns a string representation of the game in the form
    "Agent: <self.agent.name>  State: <(self.ball_x, self.ball_y, self.velocity_x, self.velocity_y, self.paddle_y)>".
    """
    def __str__(self):
        state = (self.ball_x, self.ball_y, self.velocity_x, self.velocity_y, self.paddle_y)
        ret = "Agent: " + self.agent.name + "  State: " + str(state)
        return ret
