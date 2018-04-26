NAME = "AGENT"

class Agent(object):
    def __init__(self, name=NAME, playerNum=1):
        self.name = name
        self.playerNum = playerNum
        # self.playerColor = ?


    """
    The getAction function should decide the action this agent should take
    given the current state s of the game.  It should return 0 if the paddle
    should move up, 2 if the paddle should move down, or 1 if the paddle should
    do nothing.
    """
    def getAction(self, is_training, cur_state_tuple):
        raise NotImplementedError()


    """
    The updateAction function is largely responsible for the agent's learning.
    It updates the agent's parameters given the state s, the action a taken in
    state s, the reward of taking action a in state s, and the resulting state
    s_prime (s').  It computes the action a' to take from state s' and performs
    the TD update as appropriate.

    Nothing is returned.
    """
    def updateAction(self, s, a, reward, s_prime):
        raise NotImplementedError()
