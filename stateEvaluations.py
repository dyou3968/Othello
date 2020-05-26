#####################################################################################
# Evaluation states

# Sean, can you write a brief description and add comments to this page? I'm not sure what algRef is 
#####################################################################################

import random

def evaluateState(state, total, alg):
    # State is the 2d list representing the board
    # Total is the number of pieces currently placed on the board
    # Alg refers to the line of the algRef we will use for scoring


    # algRef refers to the "score" given for each position
    # The first column is the value of the sides of the board
    # The second column is the value of the corners of the board
    # The third and fourth column is the value of the inner pieces
    algRef = [[0,  0, 0, 1],
              [5, 30, 0, 1],
              [5, 30, 0, 1],
              [4, 15, 0, 1],
              [4, 15, 1, 1],
              [4, 15, 1, 2],
              [4, 15, 1, 0.5]]
    # Note: why do we need so many difference references? Can't we just have one?
    
    stats = algRef[alg] # Gets the row of data we want to use
    
    tileValue = 1
    sideValue = stats[0]
    cornerValue = stats[1]


    # The three columns of each value represent unfilled, white, and black, respectively
    squares = [0,0,0]
    sides = [0,0,0]
    corners = [0,0,0]


    for row in range(8):
        for col in range(8):
            # Adds the value to squares if the tile is filled
            squares[state[row][col]] += 1
            # Adds a value to sides if the tile is a side
            if (row in [0,7] or col in [0,7]):
                sides[state[row][col]] += 1
            # Adds a value to corners if the tile is a corner
            if (row in [0,7] and col in [0,7]):
                corners[state[row][col]] += 1

    positionalValue = 1 - stats[2] * (total/64)**stats[3]
    value = 0
    value += (squares[1]*tileValue + positionalValue * (sides[1]*sideValue + corners[1]*cornerValue))
    value -= (squares[-1]*tileValue + positionalValue * (sides[-1]*sideValue + corners[-1]*cornerValue))
    value += random.random() #I don't understand why we are introducing randomness here
    return value