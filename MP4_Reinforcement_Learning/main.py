"""
-------------------------------------------------------------------------------
This is the driver file for parts 1 and 2

To run part 1, run the following command:

python main.py <part1> <human> <agent> <learning_rate_constant> <discount_factor> <exploration_threshold> <num_training_games>

where:
<part1>                  = "part1" (ignoring case)
<human>                  = "human" (ignoring case) if a human agent should be
                            : able to play against the AI.  Omit this argument if
                            : there should be no human agent.
<agent>                  = "q_learning" or "q-learning" (ignoring case) if the
                            : AI should be a Q-learning agent or "sarsa"
                            : (ignoring case) if the AI should be a SARSA agent
<learning_rate_constant>    = The constant C to be used in the calculation of the
                            : learning rate alpha as alpha = C/(C+N(s,a))
<discount_factor>          = The discount factor gamma to be used during training
<exploration_threshold>  = The upper bound in the exploration function.  If the
                            : first input to the exploration function is below this
                            : threshold, positive infinity is returned.
<num_training_games>        = The number of games for training the agent


To run part 2, run the following command:

python main.py <part2> <num_layers> <num_units_per_layer> <learning_rate> <weight_scale_parameter> <epochs> <mini_batch_size>

where:
<part2>                  = "part2" (ignoring case)
<num_layers>                = The number of layers the neural network should have.
<num_units_per_layer>      = The number of neurons/output features in each layer
                              (except the last layer, which is always 3 outputs)
<learning_rate>          = The learning rate to be used during gradient descent
<weight_scale_parameter>    = The scaling factor by which to scale the randomly
                              initialized weights of the neural network.  This makes
                              the weights be randomly initialized on the range
                              [0,weight_scale_parameter).
<epochs>                    = The number of epochs to run during the training phase
<mini_batch_size>          = The number of training vectors to use in each mini-batch





python main.py <gui> <agent1> <agent2>

1. Create Pong game object
2. Set up both agents
3. Create GUI
4. Start game
-------------------------------------------------------------------------------
"""


import sys
from loader import parser
import numpy as np
import helper
import gui

from pong import Pong
from Agents.q_learning import q_learning
from Agents.sarsa import sarsa
from Agents.network import network
from Agents.human import human

# CONSTANTS
NUM_TEST_GAMES = 200
NUM_TEST_RUNS = 100
SEED = 17
NUM_EPISODES_BETWEEN_POINTS = 1
EXPERT_POLICTY_DATASET_FILENAME = "Data/expert_policy.txt"

# .003906

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
##   while standard deviation increases to around 9.263404879385186.
## At the end of the 100,000 games, the mean rewards is around 11.193050505050506
##   and the standard deviation is around 9.70943954875793


"""
SARSA
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
##   games while standard deviation increases to around 5.454864725972152.


"""
INITIAL ACTION HARD-CODED TO ALWAYS MOVE DOWN (action = 2)
"""

# Learning-rate-constant: 10
# Discount factor: .80
# exploration_threshold: 10
# Training games: 100,000

# MAXIMUM REWARD COUNT OVER TRAINING GAMES: 77.0
# MAXIMUM REWARD COUNT OVER TEST GAMES: 51.0
# Average number of bounces on test games: 9.875

## Mean rewards increases to around 7.524818181818182 by the end of the 100,000
##   games while standard deviation increases to around 6.492778445060258.

if __name__ == "__main__":
    """
    test = network()
    test.load_network()
    """
    if sys.argv[1].lower() == "part1":
        params = (sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
        if sys.argv[2].lower() == "q_learning" or sys.argv[2].lower() == "q-learning":
            game = Pong(q_learning(float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), num_training_games=int(sys.argv[6])))
            game.agent.formulate_file_name()
            loaded = game.agent.load()
            if not loaded:
                training_game_rewards = game.run_multiple_games(int(sys.argv[6]), True)
                helper.plot_mean_episode_rewards_vs_episodes(training_game_rewards, NUM_EPISODES_BETWEEN_POINTS, game.agent)
                game.agent.save()

            # test_game_rewards = game.run_multiple_games(NUM_TEST_GAMES, False)
            # num_test_bounces = test_game_rewards + np.ones(len(test_game_rewards))
            # print("Average number of bounces on test games: " + str(np.sum(num_test_bounces)/len(num_test_bounces)))

            avg_test_bounces = np.zeros((NUM_TEST_RUNS, NUM_TEST_GAMES))
            avg_test_rewards = np.zeros((NUM_TEST_RUNS, NUM_TEST_GAMES))
            np.random.seed(SEED)
            for i in range(NUM_TEST_RUNS):
                print("Running {0} of {1} sets of {2} test games...".format(i+1, NUM_TEST_RUNS, NUM_TEST_GAMES))
                test_game_rewards = game.run_multiple_games(NUM_TEST_GAMES, False)
                avg_test_rewards[i,:] += test_game_rewards

                num_test_bounces = test_game_rewards + np.ones(len(test_game_rewards))
                avg_test_bounces[i,:] += num_test_bounces
                # print("Average number of bounces on test games: " + str(np.sum(num_test_bounces)/len(num_test_bounces)))

            max_game_rewards = np.amax(avg_test_rewards,axis=1)
            print("Maximum Rewards Count on test games: " + str(np.sum(max_game_rewards)/len(max_game_rewards)))
            avg_test_bounces = np.sum(np.sum(avg_test_bounces,axis=1)/avg_test_bounces.shape[1])/avg_test_bounces.shape[0]
            print("Average number of bounces on test games: " + str(avg_test_bounces))

            # gui.pong_gui(game, 'q_learning')

        elif sys.argv[2].lower() == "sarsa":
            game = Pong(sarsa(float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])))
            loaded = game.agent.load()
            if not loaded:
                training_game_rewards = game.run_multiple_games(int(sys.argv[6]), True)
                helper.plot_mean_episode_rewards_vs_episodes(training_game_rewards, NUM_EPISODES_BETWEEN_POINTS, game.agent)
                game.agent.save()

            # test_game_rewards = game.run_multiple_games(NUM_TEST_GAMES, False)
            # num_test_bounces = test_game_rewards + np.ones(len(test_game_rewards))
            # print("Average number of bounces on test games: " + str(np.sum(num_test_bounces)/len(num_test_bounces)))

            avg_test_bounces = np.zeros((NUM_TEST_RUNS, NUM_TEST_GAMES))
            avg_test_rewards = np.zeros((NUM_TEST_RUNS, NUM_TEST_GAMES))
            np.random.seed(SEED)
            for i in range(NUM_TEST_RUNS):
                print("Running {0} of {1} sets of {2} test games...".format(i+1, NUM_TEST_RUNS, NUM_TEST_GAMES))
                test_game_rewards = game.run_multiple_games(NUM_TEST_GAMES, False)
                avg_test_rewards[i,:] += test_game_rewards

                num_test_bounces = test_game_rewards + np.ones(len(test_game_rewards))
                avg_test_bounces[i,:] += num_test_bounces
                # print("Average number of bounces on test games: " + str(np.sum(num_test_bounces)/len(num_test_bounces)))

            max_game_rewards = np.amax(avg_test_rewards,axis=1)
            print("Maximum Rewards Count on test games: " + str(np.sum(max_game_rewards)/len(max_game_rewards)))
            avg_test_bounces = np.sum(np.sum(avg_test_bounces,axis=1)/avg_test_bounces.shape[1])/avg_test_bounces.shape[0]
            print("Average number of bounces on test games: " + str(avg_test_bounces))

            # gui.pong_gui(game, 'sarsa')

        elif sys.argv[2].lower() == "human":
            game = Pong(human())
            gui.pong_gui(game)

        else:
            sys.exit("INVALID ARGUMENT ERROR: The second argument must be \"q_learning\", \"q-learning\", \"sarsa\", or \"human\" (ignoring case)!")

    elif sys.argv[1].lower() == "part2":
        assert len(sys.argv) == 8

        agent = network(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]))

        dataset_tuple = parser(EXPERT_POLICTY_DATASET_FILENAME)
        agent.MinibatchGD(dataset_tuple, int(sys.argv[6]), int(sys.argv[7]))
        agent.save_network()

        game = Pong(agent)
        test_game_rewards = game.run_multiple_games(NUM_TEST_GAMES, False)
        num_test_bounces = test_game_rewards + np.ones(len(test_game_rewards))
        print("Average number of bounces on test games: " + str(np.sum(num_test_bounces)/len(num_test_bounces)))

        agent.load_network()
        gui.pong_gui(game, 'neural_net')

    elif sys.argv[1].lower() == "gui":
        agent1 = None 
        agent2 = None 

        if sys.argv[2].lower() == "q_learning" or sys.argv[2].lower() == "q-learning":
            agent1 = q_learning();
            agent1.load();
        elif sys.argv[2].lower() == "sarsa":
            agent1 = sarsa();
            agent1.load();
        elif sys.argv[2].lower() == "network":
            agent1 = network();
            agent1.load_network();

        # if sys.argv[3].lower() == "q_learning" or sys.argv[2].lower() == "q-learning":
        #    agent2 = q_learning();
        # elif sys.argv[3].lower() == "sarsa":
        #    agent2 = sarsa();
        # elif sys.argv[3].lower() == "human":
        #    agent2 = human();

        game = Pong(agent1)
        gui.pong_gui(game, agent1, agent2)
    else:
        sys.exit("INVALID ARGUMENT ERROR: The first argument must be \"part1\" or \"part2\" (ignoring case)!")
# if __name__ == "__main__":
#    """
#    incorrectUsageError = "Incorrect Usage: Expected " \
#                        + "\"python %s <bayes> <laplace>\" or " % sys.argv[0] \
#                        + "\"python %s <perceptron> <hasBias> <weightsAreRandom> <hasRandomTrainingOrder> <epochs>\"" % sys.argv[0]
#    """
#    incorrectUsageError = "Incorrect Usage: Expected " \
#                        + "\"python %s <bayes> <laplace>\" or " % sys.argv[0] \
#                        + "\"python %s <perceptron> <learning_rate_power> <epochs>\"" % sys.argv[0]
#
#    assert len(sys.argv) >= 3, incorrectUsageError
#
#    if sys.argv[1].lower() == "part1":
#        # Run part 1
#
#
#        # Check the validity of the command-line arguments
#        assert len(sys.argv) in [3,4], incorrectUsageError
#
#    elif sys.argv[1].lower() == "part2":
#        # Run part 2
#        if sys.argv[2].lower() == "best":
#            # Run code for reproducing the best empirical results
#            # discovered for the non-differentiable perceptron
#            perceptron.reproduce_best_results(training_data_tuple, test_data_tuple, False)
#        else:
#            # Check that the number of command-line arguments is correct
#            assert len(sys.argv) == 4, incorrectUsageError
#
#            # Run code for training and classifying with perceptron
#            perceptron.run_perceptron(training_data_tuple, test_data_tuple, False, int(sys.argv[2]), int(sys.argv[3]))
#
#    else:
#        sys.exit("INVALID ARGUMENT ERROR: The third argument must be \"bayes\", \"naivebayes\", \"perceptron\", or \"face\" (ignoring case)!")
