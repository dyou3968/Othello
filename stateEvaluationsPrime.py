#####################################################################################
# Evaluation states more efficiently using this paper: 
# http://web.eecs.utk.edu/~zzhang61/docs/reports/2014.04%20-%20Searching%20Algorithms%20in%20Playing%20Othello.pdf

# This uses the same base algorithm as evaluateState but changes the reward of different squares 
#####################################################################################

import random

def evaluateStatePrime(state):
    # State is the board of the game (2d List)
    # Pieces Played is the number of pieces that have been played on the board
        # This is not currently used in our program, but it was part of the other algorithm
        # So we wanted to keep it just in case.


    # This grid is based off of the reward system in the paper cited above
    # We believe this implementation is best for the minimax algorithm
    squareRewards =[[120, -20, 20,  5,  5, 20, -20, 120],
                    [-20, -40, -5, -5, -5, 20, -40, -20],
                    [ 20,  -5, 15,  3,  3, 15,  -5,  20],
                    [  5,  -5,  3,  3,  3,  3,  -5,   5],
                    [  5,  -5,  3,  3,  3,  3,  -5,   5],
                    [ 20,  -5, 15,  3,  3, 15,  -5,  20],
                    [-20, -40, -5, -5, -5, 20, -40, -20],
                    [120, -20, 20,  5,  5, 20, -20, 120]]

    whiteTotal = 0
    blackTotal = 0

    for row in range(8):
        for col in range(8):
            if state[row][col] == 1: #If the piece on that specific space is white 
                whiteTotal += squareRewards[row][col]
            elif state[row][col] == -1: #If the piece on that specific space is black
                blackTotal += squareRewards[row][col]

    value = whiteTotal - blackTotal
    value += random.random() 
    return value