#####################################################################################
# Creates the background board for the game
#####################################################################################

class Board(object):
    def __init__(self, turn = 1, state = None):
        if state == None:
            self.state = [[0] * 8 for i in range(8)]
            self.state[3][3] = self.state[4][4] = 1
            self.state[3][4] = self.state[4][3] = -1
        self.turn = turn
        self.names = [0, "White", "Black"]
        self.colors = [0, (255,255,255), (0,0,0)]
        self.displayPossible = False
        flip = getFlipped(self, (0,0))
    def place(self, row, col):
        possibleMoves = getValidMoves(self)
        if (row, col) in possibleMoves:
            for square in getFlipped(self, (row, col)):
                self.state[square[0]][square[1]] = self.turn
            self.state[row][col] = self.turn
            self.turn *= -1