import sys
import helper

class Pong(object):
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

    """
    This is the constructor for a Pong game.  By default, the setup of the game
    is identical to the initial state defined in the assignment.  The game's
    agent should always be passed in as the appropriate object.
    """
    def __init__(self, agent, ball_x=INITIAL_BALL_X, ball_y=INITIAL_BALL_Y, velocity_x=INITIAL_VELOCITY_X, velocity_y=INITIAL_VELOCITY_Y, paddle_y=INITIAL_PADDLE_Y):
        # Check that velocity_x is valid
        if abs(velocity_x) < 0.03:
            raise ValueError("Absolute value of velocity_x must be greater than or equal to 0.03!")

        # Initialize the agent
        self.agent = agent

        # Initialize the game state
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.paddle_y = paddle_y


    """
    This function is responsible for updating the state of the game with every
    time step.  It gets the agent's action, uses it to update the paddle's
    position, updates the ball's position, and then handles the bouncing of the
    ball.
    """
    def update_time_step(self):
        # Get the action of the agent
        action = self.agent.getAction()

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

    """
    This function handles the bouncing of the ball off of the walls and paddle.
    """
    def handle_bounce(self):
        if self.ball_y < 0:
            self.ball_y *= -1
            self.velocity_y *= -1
        if self.ball_y > 1:
            self.ball_y = 2 - self.ball_y
            self.velocity_y *= -1
        if self.ball_x < 0:
            self.ball_x *= -1
            self.velocity_x *= -1

        # TODO: Implement bouncing off of paddle
        pass


    ## Prints the state of the game to standard out
    def printBoard(self):
        board = self.board
        for i in range(len(board)):
            sys.stdout.write(' '.join(n[i].__repr__() for n in board))
            sys.stdout.write("\n")
        sys.stdout.write("\n")

    ## Returns the state of the game as a single string
    def __str__(self):
        zeroIndexed = True
        ret = ""
        board = self.board

        ## Numbers along top
        # ret += "  " + ' '.join(str(i+int(not zeroIndexed)) for i in range(self.dim)) + "\n"
        for i in range(self.dim):
            # First row is top row
            # ret += str(i+int(not zeroIndexed)) + " " + ' '.join(n[i].__repr__() for n in board) + "\n"

            # First row is bottom row
            ret += str(len(board) - i - int(zeroIndexed)) + " " + ' '.join(n[self.dim - i - 1].__repr__() for n in board) + "\n"

        ## Numbers along bottom
        ret += "  " + ' '.join(str(i+int(not zeroIndexed)) for i in range(self.dim)) + "\n"
        return ret


    """
    The game_is_over function checks if the Pong game has ended (the ball has
    left the screen).
    """
    def game_is_over(self):
        pass


    """
    The reset_game function resets the position and velocity of the ball and
    the position of the paddle for starting a new game.  The parameters make it
    possible to reset these variables differently, but they will be set to the
    initial state defined in the assignment by default.
    """
    def reset_game(self, ball_x=INITIAL_BALL_X, ball_y=INITIAL_BALL_Y, velocity_x=INITIAL_VELOCITY_X, velocity_y=INITIAL_VELOCITY_Y, paddle_y=INITIAL_PADDLE_Y)):
        # Check that velocity_x is valid
        if abs(velocity_x) < 0.03:
            raise ValueError("Absolute value of velocity_x must be greater than or equal to 0.03!")

        # Reset the game state
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.paddle_y = paddle_y
