# Import the necessary libraries
import numpy as np

"""
-------------------------------------------------------------------------------
HELPER FUNCTIONS GO IN THIS FILE!
-------------------------------------------------------------------------------
"""

"""
This function takes in a 5-tuple representing the state of the game and converts
it into the discrete state representation where the entire board is treated as
a 12 x 12 grid, and two states are considered the same if the ball lies within
the same grid cell.

Returns a 5-tuple of the proper discrete values or -1 if the ball's x-coordinate
is greater than or equal to 1.  If returned, the entries of the tuple are as
follows:

discrete_ball_x:        The x-coordinate of the grid cell containing the ball
(0th entry)             on the interval [0,11].  Higher values correspond to higher
                        original x-coordinates.

discrete_ball_y:        The y-coordinate of the grid cell containing the ball
(1th entry)             on the interval [0,11].  Higher values correspond to higher
                        original y-coordinates.

discrete_velocity_x:    1 if the ball's horizontal velocity is positive, -1 if the
(2th entry)             ball's horizontal velocity is negative.  The absolute value
                        of the ball's horizontal velocity is assumed to be greater
                        than 0.03, so it is considered impossible for it to be
                        equivalent to 0.

discrete_velocity_y:    1 if the ball's vertical velocity is positive, -1 if the
(3th entry)             ball's vertical velocity is negative, or 0 if the absolute
                        value of the ball's vertical velocity is less than 0.015.

discrete_paddle_y:      The y-coordinate of the grid cell containing the top of
(4th entry)             the paddle on the interval [0,11].  Higher values correspond
                        to higher original y-coordinates.

                        This is set to 11 if paddle_y = 1 - paddle_height.
                        Otherwise, paddle_y is assumed to be less than (1 - paddle_height)
                        and the y-coordinate is computed as
                        floor(12 * paddle_y / (1 - paddle_height)).
"""
def get_discrete_state(state_tuple):
    # Extract the elements of the state
    continuous_ball_x = state_tuple[0]
    if continuous_ball_x >= 1.0:
        return -1

    continuous_ball_y = state_tuple[1]
    continuous_velocity_x = state_tuple[2]
    continuous_velocity_y = state_tuple[3]
    continuous_paddle_y = state_tuple[4]

    # Convert to ball_x, ball_y, and velocity_x to discrete values
    discrete_ball_x = int(12 * continuous_ball_x)
    discrete_ball_y = int(12 * continuous_ball_y)
    discrete_velocity_x = int(np.sign(continuous_velocity_x))

    # Convert velocity_y to the proper discrete value
    discrete_velocity_y = None
    if abs(continuous_velocity_y) < 0.015:
        discrete_velocity_y = 0
    else:
        discrete_velocity_y = int(np.sign(continuous_velocity_y))

    # Convert paddle_y to the proper discrete value
    discrete_paddle_y = int(np.min(12 * continuous_paddle_y / (1 - paddle_height), 11))

    return (discrete_ball_x, discrete_ball_y, discrete_velocity_x, discrete_velocity_y, discrete_paddle_y)


"""
This is the exploration function used by the q-learning and SARSA agents.  For a
particular state s, it takes in a vector of Q(s,a') values and a vector of N(s,a')
values over all actions a'.  It also takes in an exploration threshold N_e.

Returns a vector such that the ith entry is positive infinity if N(s,a'_i) < N_e
for the ith action a'_i, and Q(s,a'_i) otherwise.
"""
def exploration_function(q_values, counts_Nsa, exploration_threshold):
    indices_with_infinity = counts_Nsa < exploration_threshold
    indices_with_q_values = counts_Nsa >= exploration_threshold

    results = np.zeros((len(q_values),))
    results[indices_with_infinity] = float("inf")
    results[indices_with_q_values] = q_values[indices_with_q_values]

    return results


"""
This function creates the Mean Episodes Rewards Vs. Episodes plot.  It takes in
a numpy vector of the rewards for each episode and the number of episodes between each
computed data point.  The plotted data points are computed as:

[(num_episodes_between_points * (i+1), average over rewards[0:(num_episodes_between_points * (i+1))])
 for i in range(len(rewards)/num_episodes_between_points)]

For example, suppose rewards = [2,3,4,5,6,7].  If
num_episodes_between_points = 2, then the plotted data points are
(2, average over rewards[0:2]), (4, average over rewards[0:4]), and
(6, average over rewards[0:6]).

num_episodes_between_points is assumed to evenly divide len(rewards).
"""
def plot_mean_episode_rewards_vs_episodes(rewards, num_episodes_between_points):
    num_points = len(rewards)/num_episodes_between_points

    x_coordinates = [num_episodes_between_points * (i+1) for i in range(num_points)]
    y_coordinates = [np.sum(rewards[0:(num_episodes_between_points * (i+1))])/(num_episodes_between_points * (i+1))
                     for i in range(num_points)]

    #TODO: Plot the points


"""
Computes the confusion matrix given the true labels of the test images and
their assigned labels.
"""
def compute_confusion_matrix(true_labels, assigned_labels, numClasses=10):
    assert len(true_labels) == len(assigned_labels), "LENGTH NOT SAME ERROR: true labels " + \
                                                     "and assigned labels don't have same length!"

    # Initializes the confusion matrix as a 10 x 10 matrix of zeros and for every
    # entry (i,j), counts up the number of images with true label i that were assigned
    # label j
    confusion = np.zeros((numClasses, numClasses))
    for i in range(len(true_labels)):
        confusion[ true_labels[i] , assigned_labels[i] ] += 1

    # Normalizes every row to sum to 1, making every entry (i,j) represent the
    # percentage of images with true label i that were assigned label j
    for i in range(len(confusion)):
        confusion[i,:] /= np.sum(confusion[i,:])

    return confusion


"""
Computes the overall accuracy on a test dataset given a numpy vector of the true
labels of the test images and a numpy vector of their assigned labels
"""
def compute_overall_accuracy(true_labels, assigned_labels):
    assert len(true_labels) == len(assigned_labels), "LENGTH NOT SAME ERROR: true labels " + \
                                                     "and assigned labels don't have same length!"
    return (np.sum(np.equal(true_labels, assigned_labels)) / len(true_labels))
