"""
-------------------------------------------------------------------------------
This is the driver file for parts 1 and 2

To run part 1, run the following command:

python main.py <part1> <human> <agent> <learning_rate_constant> <discount_factor> <exploration_threshold> <num_training_games>

where:
<part1>                     = "part1" (ignoring case)
<human>                     = "human" (ignoring case) if a human agent should be
                            : able to play against the AI.  Omit this argument if
                            : there should be no human agent.
<agent>                     = "q_learning" or "q-learning" (ignoring case) if the
                            : AI should be a Q-learning agent or "sarsa"
                            : (ignoring case) if the AI should be a SARSA agent
<learning_rate_constant>    = The constant C to be used in the calculation of the
                            : learning rate alpha as alpha = C/(C+N(s,a))
<discount_factor>           = The discount factor gamma to be used during training
<exploration_threshold>     = The upper bound in the exploration function.  If the
                            : first input to the exploration function is below this
                            : threshold, positive infinity is returned.
<num_training_games>        = The number of games for training the agent


To run part 2, run the following command:

python main.py <part2> <num_layers> <num_units_per_layer> <learning_rate> <weight_scale_parameter> <epochs> <mini_batch_size>

where:
<part2>                     = "part2" (ignoring case)
<num_layers>                = The number of layers the neural network should have.
<num_units_per_layer>       = The number of neurons/output features in each layer
                              (except the last layer, which is always 3 outputs)
<learning_rate>             = The learning rate to be used during gradient descent
<weight_scale_parameter>    = The scaling factor by which to scale the randomly
                              initialized weights of the neural network.  This makes
                              the weights be randomly initialized on the range
                              [0,weight_scale_parameter).
<epochs>                    = The number of epochs to run during the training phase
<mini_batch_size>           = The number of training vectors to use in each mini-batch
-------------------------------------------------------------------------------
"""


import sys
from loader import parser
import numpy as np
import helper

from pong import Pong
from Agents.q_learning import q_learning
from Agents.sarsa import sarsa
from Agents.network import network

# CONSTANTS
NUM_TEST_GAMES = 200
NUM_EPISODES_BETWEEN_POINTS = 1
EXPERT_POLICTY_DATASET_FILENAME = "Data/expert_policy.txt"

"""
Q-LEARNING
"""

# Learning-rate-constant: 1.0
# Discount factor: .80
# exploration_threshold: 3
# Training games: 100,000

# Average number of bounces on test games: 5.25


# Learning-rate-constant: 1.0
# Discount factor: .80
# exploration_threshold: 5
# Training games: 100,000

# Average number of bounces on test games: 5.505


# Learning-rate-constant: 10
# Discount factor: .80
# exploration_threshold: 10
# Training games: 100,000

# Average number of bounces on test games: 12.98
## Mean rewards increases to around 9.008483870967742 after approximately 31,000 games
##     while standard deviation increases to around 9.263404879385186.
## At the end of the 100,000 games, the mean rewards is around 11.193050505050506
##     and the standard deviation is around 9.70943954875793


"""
SARSA

NOTE: The initial action is hard-coded to always move down. (action = 2)
"""

"""
INITIAL ACTION HARD-CODED TO ALWAYS MOVE DOWN (action = 0)
"""

# Learning-rate-constant: 10
# Discount factor: .80
# exploration_threshold: 10
# Training games: 100,000

# MAXIMUM REWARD COUNT OVER TRAINING GAMES: 57.0
# MAXIMUM REWARD COUNT OVER TEST GAMES: 28.0
# Average number of bounces on test games: 8.24

## Mean rewards increases to around 6.102525252525252 by the end of the 100,000
##     games while standard deviation increases to around 5.454864725972152.


"""
INITIAL ACTION HARD-CODED TO ALWAYS MOVE DOWN (action = 2)
"""

# Learning-rate-constant: 1.0
# Discount factor: .80
# exploration_threshold: 5
# Training games: 100,000

# MAXIMUM REWARD COUNT: 70.0
# MAXIMUM REWARD COUNT: 31.0
# Average number of bounces on test games: 8.47

## Mean rewards increases to around 6.24189898989899 by the end of the 100,000
##     games while standard deviation increases to around 5.800399675353187.


# Learning-rate-constant: 10
# Discount factor: .80
# exploration_threshold: 10
# Training games: 100,000

# MAXIMUM REWARD COUNT OVER TRAINING GAMES: 77.0
# MAXIMUM REWARD COUNT OVER TEST GAMES: 51.0
# Average number of bounces on test games: 9.875

## Mean rewards increases to around 7.524818181818182 by the end of the 100,000
##     games while standard deviation increases to around 6.492778445060258.

if __name__ == "__main__":
    if sys.argv[1].lower() == "part1":
        if sys.argv[2].lower() == "q_learning" or sys.argv[2].lower() == "q-learning":
            game = Pong(q_learning(float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])))
            training_game_rewards = game.run_multiple_games(int(sys.argv[6]), True)
            helper.plot_mean_episode_rewards_vs_episodes(training_game_rewards, NUM_EPISODES_BETWEEN_POINTS)

            test_game_rewards = game.run_multiple_games(NUM_TEST_GAMES, False)
            num_test_bounces = test_game_rewards + np.ones(len(test_game_rewards))
            print("Average number of bounces on test games: " + str(np.sum(num_test_bounces)/len(num_test_bounces)))
        elif sys.argv[2].lower() == "sarsa":
            game = Pong(sarsa(float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])))
            training_game_rewards = game.run_multiple_games(int(sys.argv[6]), True)
            helper.plot_mean_episode_rewards_vs_episodes(training_game_rewards, NUM_EPISODES_BETWEEN_POINTS)

            test_game_rewards = game.run_multiple_games(NUM_TEST_GAMES, False)
            num_test_bounces = test_game_rewards + np.ones(len(test_game_rewards))
            print("Average number of bounces on test games: " + str(np.sum(num_test_bounces)/len(num_test_bounces)))
        elif sys.argv[2].lower() == "human":
            pass
        else:
            sys.exit("INVALID ARGUMENT ERROR: The second argument must be \"q_learning\", \"q-learning\", \"sarsa\", or \"human\" (ignoring case)!")
    elif sys.argv[1].lower() == "part2":
        assert len(sys.argv) == 8

        agent = network(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]))

        dataset_tuple = parser(EXPERT_POLICTY_DATASET_FILENAME)
        agent.MinibatchGD(dataset_tuple, int(sys.argv[6]), int(sys.argv[7]))

        game = Pong(agent)
        test_game_rewards = game.run_multiple_games(NUM_TEST_GAMES, False)
        num_test_bounces = test_game_rewards + np.ones(len(test_game_rewards))
        print("Average number of bounces on test games: " + str(np.sum(num_test_bounces)/len(num_test_bounces)))
    else:
        sys.exit("INVALID ARGUMENT ERROR: The first argument must be \"part1\" or \"part2\" (ignoring case)!")
# if __name__ == "__main__":
#     """
#     incorrectUsageError = "Incorrect Usage: Expected " \
#                         + "\"python %s <bayes> <laplace>\" or " % sys.argv[0] \
#                         + "\"python %s <perceptron> <hasBias> <weightsAreRandom> <hasRandomTrainingOrder> <epochs>\"" % sys.argv[0]
#     """
#     incorrectUsageError = "Incorrect Usage: Expected " \
#                         + "\"python %s <bayes> <laplace>\" or " % sys.argv[0] \
#                         + "\"python %s <perceptron> <learning_rate_power> <epochs>\"" % sys.argv[0]
#
#     assert len(sys.argv) >= 3, incorrectUsageError
#
#     if sys.argv[1].lower() == "part1":
#         # Run part 1
#
#
#         # Check the validity of the command-line arguments
#         assert len(sys.argv) in [3,4], incorrectUsageError
#
#     elif sys.argv[1].lower() == "part2":
#         # Run part 2
#         if sys.argv[2].lower() == "best":
#             # Run code for reproducing the best empirical results
#             # discovered for the non-differentiable perceptron
#             perceptron.reproduce_best_results(training_data_tuple, test_data_tuple, False)
#         else:
#             # Check that the number of command-line arguments is correct
#             assert len(sys.argv) == 4, incorrectUsageError
#
#             # Run code for training and classifying with perceptron
#             perceptron.run_perceptron(training_data_tuple, test_data_tuple, False, int(sys.argv[2]), int(sys.argv[3]))
#
#     else:
#         sys.exit("INVALID ARGUMENT ERROR: The third argument must be \"bayes\", \"naivebayes\", \"perceptron\", or \"face\" (ignoring case)!")
