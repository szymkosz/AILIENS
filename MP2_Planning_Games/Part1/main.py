"""
-------------------------------------------------------------------------------
This file is for running the search algorithms.
To run a particular algorithm, run the following command:

python main.py <sequence> <algorithm> <N> <numTrials>
where:
<sequence>  = "stops" or "distance"
<algorithm> = "A*" or "Astar" or "AStar" when running A* search
            : "ucs" or "UCS" when running uniform-cost search
<N>         = the length of each widget (3 <= N <= 8); should be provided
            : only if the random widget generator is being run
<numTrials> = the number of trials to run with the random widget generator
-------------------------------------------------------------------------------
"""

import sys
import search
import helper

# Initialize the given recipes and the letters that can be used to form recipes
recipes = ["AEDCA", "BEACD", "BABCE", "DADBD", "BECBD"]
#recipes = ["AD", "AD", "AD", "BD", "BD"]
letters = ["A", "B", "C", "D", "E"]

# Initialize a dictionary of dictionaries to retrieve pairwise distances
# between locations
distances = { "A": {"B": 1064,
                    "C": 673,
                    "D": 1401,
                    "E": 277},
              "B": {"A": 1064,
                    "C": 958,
                    "D": 1934,
                    "E": 337},
              "C": {"A": 673,
                    "B": 958,
                    "D": 1001,
                    "E": 399},
              "D": {"A": 1401,
                    "B": 1934,
                    "C": 1001,
                    "E": 387},
              "E": {"A": 277,
                    "B": 337,
                    "C": 399,
                    "D": 387}}

shortestPaths = helper.computeShortestPaths(distances, letters)

isRandom = False


if __name__ == "__main__":
    incorrectUsageError = "Incorrect Usage: Expected " \
                        + "\"python %s <sequence> <algorithm> " % sys.argv[0] \
                        + "<N> \"\nOmit <N> and <numTrials> if not running the random widget generator."

    assert len(sys.argv) == 3 or len(sys.argv) == 5, incorrectUsageError

    if len(sys.argv) == 5:
        N = int(sys.argv[3])
        results = []

        for i in range(int(sys.argv[4])):
            recipes = helper.generateWidgets(N, letters)

            if sys.argv[1] == "stops":
                if sys.argv[2] == "A*" or sys.argv[2] == "Astar" or sys.argv[2] == "AStar":
                    print("Widgets: " + str(recipes))
                    results.append(search.AStar_MinStops(recipes, letters))
                elif sys.argv[2] == "ucs" or sys.argv[2] == "UCS":
                    print("Widgets: " + str(recipes))
                    results.append(search.UCS_MinStops(recipes, letters))
                else:
                    sys.exit("AlgorithmNotRecognizedError: Is the algorithm spelled correctly?")

            elif sys.argv[1] == "distance":
                if sys.argv[2] == "A*" or sys.argv[2] == "Astar" or sys.argv[2] == "AStar":
                    print("Widgets: " + str(recipes))
                    results.append(search.AStar_MinDistance(recipes, distances, shortestPaths, letters))
                elif sys.argv[2] == "ucs" or sys.argv[2] == "UCS":
                    print("Widgets: " + str(recipes))
                    results.append(search.UCS_MinDistance(recipes, distances, shortestPaths, letters))
                else:
                    sys.exit("AlgorithmNotRecognizedError: Is the algorithm spelled correctly?")
            else:
                sys.exit("SequenceNotRecognizedError: Is the sequence spelled correctly?")

            print("")

        average = sum(results)/len(results)
        print("Average Expanded Nodes: " + str(average))

    else:
        if sys.argv[1] == "stops":
            if sys.argv[2] == "A*" or sys.argv[2] == "Astar" or sys.argv[2] == "AStar":
                print("Widgets: " + str(recipes))
                search.AStar_MinStops(recipes, letters)
            elif sys.argv[2] == "ucs" or sys.argv[2] == "UCS":
                print("Widgets: " + str(recipes))
                search.UCS_MinStops(recipes, letters)
            else:
                sys.exit("AlgorithmNotRecognizedError: Is the algorithm spelled correctly?")

        elif sys.argv[1] == "distance":
            if sys.argv[2] == "A*" or sys.argv[2] == "Astar" or sys.argv[2] == "AStar":
                print("Widgets: " + str(recipes))
                search.AStar_MinDistance(recipes, distances, shortestPaths, letters)
            elif sys.argv[2] == "ucs" or sys.argv[2] == "UCS":
                print("Widgets: " + str(recipes))
                search.UCS_MinDistance(recipes, distances, shortestPaths, letters)
            else:
                sys.exit("AlgorithmNotRecognizedError: Is the algorithm spelled correctly?")
        else:
            sys.exit("SequenceNotRecognizedError: Is the sequence spelled correctly?")
