"""
-------------------------------------------------------------------------------
This is the driver file for parts 1 and 2

To run part 1, run the following command:

python main.py <part1> <human> <agent>

where:
<part1>     = "part1" (ignoring case)
<human>     = "human" (ignoring case) if a human agent should be able to play
            : against the AI.  Omit this argument if there should be no human
            : agent.
<agent>     = "q_learning" or "q-learning" (ignoring case) if the AI should be
            : a Q-learning agent or "sarsa" (ignoring case) if the AI should be
            : a SARSA agent.


To run part 2, run the following command:

python main.py <part2> ?

where:
<part2>     = "part2" (ignoring case)
?
-------------------------------------------------------------------------------
"""

#import numpy as np
import sys

if __name__ == "__main__":
    """
    incorrectUsageError = "Incorrect Usage: Expected " \
                        + "\"python %s <bayes> <laplace>\" or " % sys.argv[0] \
                        + "\"python %s <perceptron> <hasBias> <weightsAreRandom> <hasRandomTrainingOrder> <epochs>\"" % sys.argv[0]
    """
    incorrectUsageError = "Incorrect Usage: Expected " \
                        + "\"python %s <bayes> <laplace>\" or " % sys.argv[0] \
                        + "\"python %s <perceptron> <learning_rate_power> <epochs>\"" % sys.argv[0]

    assert len(sys.argv) >= 3, incorrectUsageError

    if sys.argv[1].lower() == "part1":
        # Run part 1
        

        # Check the validity of the command-line arguments
        assert len(sys.argv) in [3,4], incorrectUsageError

    elif sys.argv[1].lower() == "part2":
        # Run part 2
        if sys.argv[2].lower() == "best":
            # Run code for reproducing the best empirical results
            # discovered for the non-differentiable perceptron
            perceptron.reproduce_best_results(training_data_tuple, test_data_tuple, False)
        else:
            # Check that the number of command-line arguments is correct
            assert len(sys.argv) == 4, incorrectUsageError

            # Run code for training and classifying with perceptron
            perceptron.run_perceptron(training_data_tuple, test_data_tuple, False, int(sys.argv[2]), int(sys.argv[3]))

    else:
        sys.exit("INVALID ARGUMENT ERROR: The third argument must be \"bayes\", \"naivebayes\", \"perceptron\", or \"face\" (ignoring case)!")
