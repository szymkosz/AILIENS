# Import all the necessary packages
import heapq

"""
-------------------------------------------------------------------------------
PART 1.1 HELPER FUNCTIONS START HERE!
-------------------------------------------------------------------------------
"""

# Takes in a list of 5 strings as one parameter and finds the Longest Common
# Subsequence (LCS) of those strings
def lcsOf5List(strings, printL=False):
    X, Y, Z, T, U = strings
    return lcsOf5(X, Y, Z, T, U, printL)

## Finds the length of the Longest Common Subsequence for 5 strings
def lcsOf5(X, Y, Z, T, U, printL=False):
    a, b, c, d, e = len(X), len(Y), len(Z), len(T), len(U)

    L = [[[[[0 for i in range(e+1)] for j in range(d+1)]
         for k in range(c+1)] for l in range(b+1)] for m in range(a+1)]

    for i in range(a+1):                    # X
        for j in range(b+1):                # Y
            for k in range(c+1):            # Z
                for l in range(d+1):        # T
                    for m in range(e+1):    # U
                        if (i == 0 or j == 0 or k == 0 or l == 0 or m == 0):
                            L[i][j][k][l][m] = 0

                        elif (X[i-1] == Y[j-1] and
                              X[i-1] == Z[k-1] and
                              X[i-1] == T[l-1] and
                              X[i-1] == U[m-1]):
                            L[i][j][k][l][m] = L[i-1][j-1][k-1][l-1][m-1] + 1

                        else:
                            L[i][j][k][l][m] = max(max(max(
                            max(L[i-1][j][k][l][m], L[i][j-1][k][l][m]),
                            L[i][j][k-1][l][m]), L[i][j][k][l-1][m]), L[i][j][k][l][m-1])

    # Prints the state of the L matrix before returning
    if printL:
        for i in range(len(L)):
            print("\n-------------- {0} --------------\n".format(i))
            for j in range(len(L[0])):
                for k in range(len(L[0][0])):
                    print(k, L[i][j][k])
                print("\n")

    return L[a][b][c][d][e]

def scsOf5List(strings, printL=False):
    return sum([len(string) for string in strings]) - lcsOf5List(strings, printL)


"""
-------------------------------------------------------------------------------
PART 1.3 HELPER FUNCTIONS START HERE!
-------------------------------------------------------------------------------
"""
