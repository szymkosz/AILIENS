NAME = "AGENT"

class Agent(object):
    #def __init__(self, game=Pong(self), playerNum=1):
    def __init__(self, name=NAME, playerNum=1):
        #self.name = NAME
        #self.game = game
        self.name = name
        self.playerNum = playerNum
        # self.playerColor = ?


    """
    The getAction function should decide the action this agent should take
    given the state of self.game.  It should return 1 if the paddle should
    move up, -1 if the paddle should move down, or 0 if the paddle should do
    nothing.
    """
    def getAction(self, is_training, cur_state_tuple):
        raise NotImplementedError()


    """
    The updateAction function is largely responsible for the agent's learning.
    It updates the agent's parameters given the state s, the action a taken in
    state s, the resulting state s_prime (s'), whether or not s is the terminal state,
    and whether or not s' is the terminal state.  It computes the reward r,
    the action a' to take from state s', and performs the TD update as appropriate.

    Nothing is returned.
    """
    def updateAction(self, s, a, s_prime, s_isTerminal, s_prime_isTerminal):
        raise NotImplementedError()
