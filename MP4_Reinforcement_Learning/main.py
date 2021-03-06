"""
-------------------------------------------------------------------------------
This is the driver file for parts 1 and 2

To run part 1, run the following command:

python main.py <part1> <agent> <learning_rate_constant> <discount_factor> <exploration_threshold> <num_training_games>

where:
<part1>                     = "part1" (ignoring case)
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
                            : (except the last layer, which is always 3 outputs)
<learning_rate>             = The learning rate to be used during gradient descent
<weight_scale_parameter>    = The scaling factor by which to scale the randomly
                            : initialized weights of the neural network.  This makes
                            : the weights be randomly initialized on the range
                            : [0,weight_scale_parameter).
<epochs>                    = The number of epochs to run during the training phase
<mini_batch_size>           = The number of training vectors to use in each mini-batch


To run the GUI with 1 or 2 agents, run the following command:

python main.py <gui> <agent1> <agent2>

where:
<gui>       = "gui" (ignoring case)
<agent1>    = The type of agent player 1 is
<agent2>    = The type of agent player 2 is.  Omit this
            : argument to run the GUI with only one agent

<agent1> and <agent2> can be any of the following (ignoring case):
"human"                         = Human agent (only for agent2)
"q_learning" or "q-learning"    = Q-learning agent
"sarsa"                         = SARSA agent
"network"                       = Neural network agent


To play the part 1 and part 2 agents against each other, run the following command:

python main.py <versus> <agent1>

where:
<versus>       = "versus" (ignoring case)
<agent1>       = The type of agent from part 1 (Q-learning and SARSA)
-------------------------------------------------------------------------------
"""


import sys
from loader import parser
import numpy as np
import helper
import gui

from pong import Pong
from two_player_pong import Two_Player_Pong
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

if __name__ == "__main__":
    # Run part 1 code
    if sys.argv[1].lower() == "part1":
        params = (sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])

        # Train and test Q-learning agent
        if sys.argv[2].lower() == "q_learning" or sys.argv[2].lower() == "q-learning":
            game = Pong(q_learning(float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), num_training_games=int(sys.argv[6])))
            game.agent.formulate_file_name()
            loaded = game.agent.load()
            if not loaded:
                training_game_rewards = game.run_multiple_games(int(sys.argv[6]), True)
                helper.plot_mean_episode_rewards_vs_episodes(training_game_rewards, NUM_EPISODES_BETWEEN_POINTS, game.agent)
                game.agent.save()

            avg_test_bounces = np.zeros((NUM_TEST_RUNS, NUM_TEST_GAMES))
            avg_test_rewards = np.zeros((NUM_TEST_RUNS, NUM_TEST_GAMES))
            np.random.seed(SEED)
            for i in range(NUM_TEST_RUNS):
                print("Running {0} of {1} sets of {2} test games...".format(i+1, NUM_TEST_RUNS, NUM_TEST_GAMES))
                test_game_rewards = game.run_multiple_games(NUM_TEST_GAMES, False)
                avg_test_rewards[i,:] += test_game_rewards

                num_test_bounces = test_game_rewards + np.ones(len(test_game_rewards))
                avg_test_bounces[i,:] += num_test_bounces

            max_game_rewards = np.amax(avg_test_rewards,axis=1)
            print("Maximum Rewards Count on test games: " + str(np.sum(max_game_rewards)/len(max_game_rewards)))
            avg_test_bounces = np.sum(np.sum(avg_test_bounces,axis=1)/avg_test_bounces.shape[1])/avg_test_bounces.shape[0]
            print("Average number of bounces on test games: " + str(avg_test_bounces))

        # Train and test SARSA agent
        elif sys.argv[2].lower() == "sarsa":
            game = Pong(sarsa(float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), num_training_games=int(sys.argv[6])))
            loaded = game.agent.load()
            if not loaded:
                training_game_rewards = game.run_multiple_games(int(sys.argv[6]), True)
                helper.plot_mean_episode_rewards_vs_episodes(training_game_rewards, NUM_EPISODES_BETWEEN_POINTS, game.agent)
                game.agent.save()

            avg_test_bounces = np.zeros((NUM_TEST_RUNS, NUM_TEST_GAMES))
            avg_test_rewards = np.zeros((NUM_TEST_RUNS, NUM_TEST_GAMES))
            np.random.seed(SEED)
            for i in range(NUM_TEST_RUNS):
                print("Running {0} of {1} sets of {2} test games...".format(i+1, NUM_TEST_RUNS, NUM_TEST_GAMES))
                test_game_rewards = game.run_multiple_games(NUM_TEST_GAMES, False)
                avg_test_rewards[i,:] += test_game_rewards

                num_test_bounces = test_game_rewards + np.ones(len(test_game_rewards))
                avg_test_bounces[i,:] += num_test_bounces

            max_game_rewards = np.amax(avg_test_rewards,axis=1)
            print("Maximum Rewards Count on test games: " + str(np.sum(max_game_rewards)/len(max_game_rewards)))
            avg_test_bounces = np.sum(np.sum(avg_test_bounces,axis=1)/avg_test_bounces.shape[1])/avg_test_bounces.shape[0]
            print("Average number of bounces on test games: " + str(avg_test_bounces))

        else:
            sys.exit("INVALID ARGUMENT ERROR: The second argument must be \"q_learning\", \"q-learning\", \"sarsa\", or \"human\" (ignoring case)!")

    # Train and test neural network agent
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

    # Run the GUI
    elif sys.argv[1].lower() == "gui":
        agent1 = None
        agent2 = None
        game = None

        if sys.argv[2].lower() == "q_learning" or sys.argv[2].lower() == "q-learning":
            agent1 = q_learning()
            agent1.load()
        elif sys.argv[2].lower() == "sarsa":
            agent1 = sarsa()
            agent1.load()
        elif sys.argv[2].lower() == "network":
            agent1 = network()
            agent1.load_network()

        if sys.argv[3].lower() == "q_learning" or sys.argv[3].lower() == "q-learning":
           agent2 = q_learning()
           agent2.load()
        elif sys.argv[3].lower() == "sarsa":
           agent2 = sarsa()
           agent2.load()
        elif sys.argv[3].lower() == "network":
            agent2 = network()
            agent2.load_network()
        elif sys.argv[3].lower() == "human":
           agent2 = human()

        if(agent2 == None):
            game = Pong(agent1)
        else:
            game = Two_Player_Pong(agent1, agent2)

        gui.pong_gui(game, agent1, agent2)
    elif sys.argv[1].lower() == "versus":
        agent1 = None

        if sys.argv[2].lower() == "q_learning" or sys.argv[2].lower() == "q-learning":
            agent1 = q_learning()
            agent1.load()
        elif sys.argv[2].lower() == "sarsa":
            agent1 = sarsa()
            agent1.load()
        else:
            sys.exit("INVALID ARGUMENT ERROR: The second argument must be \"q_learning\", \"q-learning\", or \"sarsa\" (ignoring case)!")

        agent2 = network()
        agent2.load_network()

        game = Two_Player_Pong(agent1, agent2)
        
        game.run_multiple_games(200, False)
    else:
        sys.exit("INVALID ARGUMENT ERROR: The first argument must be \"part1\" or \"part2\" (ignoring case)!")
