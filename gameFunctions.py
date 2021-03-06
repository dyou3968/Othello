#####################################################################################
# Game Functions page

# Compiles all the game functions for Othello

"""
Notes:
While is represented on the 2dlist with a value of 1
Black is represented on the 2dlist with a value of -1
"""
#####################################################################################

import sys
import pygame
import copy
import random
from stateEvaluations import *
from stateEvaluationsPrime import *
from time import time


#####################################################################################
# Attributes (Model)
#####################################################################################

class Board(object):
    def __init__(self, turn = 1, state = None):
        if state == None:
            self.state = [[0] * 8 for i in range(8)]
            self.state[3][3] = self.state[4][4] = 1
            self.state[3][4] = self.state[4][3] = -1
        else: self.state = state
        self.turn = turn         
        self.names = [0, "White", "Black"]
        self.colors = [0, (255,255,255), (0,0,0)]
        self.displayPossible = False
        self.humanControlled = 0
        self.controlledNames = ["Both", "White", "Neither", "Black"]
        self.controlledColors = [[-1,1], [1], [], [-1]]
        self.over = False
        self.whiteWins = 0
        self.blackWins = 0

    def place(self, row, col):
        possibleMoves = getValidMoves(self)
        if (row, col) in possibleMoves:
            for square in getFlipped(self, (row, col)):
                self.state[square[0]][square[1]] = self.turn
            self.state[row][col] = self.turn
            self.checkGameOver()
            return True
        else:
            return False
    
    #Checks for game overs and double moves
    def checkGameOver(self):
        self.turn *= -1
        moves = getValidMoves(self)
        if len(moves) == 0:
            self.turn *= -1
            moves = getValidMoves(self)
            if len(moves) == 0:
                self.over = True
                totals = self.getDist()
                if totals[1] > totals[-1]:
                    self.whiteWins += 1
                elif totals[1] < totals[-1]:
                    self.blackWins += 1
                return

    def reset(self):
        self.state = [[0] * 8 for i in range(8)]
        self.state[3][3] = self.state[4][4] = 1
        self.state[3][4] = self.state[4][3] = -1
        self.turn = 1
        self.over = False

    def getDist(self):
        totals = [0,0,0]
        for row in range(8):
            for col in range(8):
                totals[self.state[row][col]] += 1
        return totals

def statePlace(state, row, col, turn):
    possibleMoves = getValidMovesState(state, turn)
    if (row, col) in possibleMoves:
        for square in getFlippedState(state, (row, col), turn):
            state[square[0]][square[1]] = turn
        state[row][col] = turn
        return state
    else:
        return False

def sortTwoLists(actual, values):
    if len(actual) <= 1:
        return actual
    else:
        less = []
        lessValues = []
        greater = []
        greaterValues = []
        pivot = actual[0]
        pivotValue = values[0]
        for i in range(1, len(actual)):
            if values[i] <= pivotValue:
                less.append(actual[i])
                lessValues.append(values[i])
            else:
                greater.append(actual[i])
                greaterValues.append(values[i])
        return sortTwoLists(less, lessValues) + [pivot] + sortTwoLists(greater, greaterValues)

def sortPossibleMoves(state, moves, maximizingPlayer):
    time0 = time()
    values = []
    for i in moves:
        copyBoard = Board(state = copy.deepcopy(state), turn = (1 if maximizingPlayer else -1))
        copyBoard.place(i[0], i[1])
        values.append(evaluateStatePrime(copyBoard.state))
    time1 = time()
    result = sortTwoLists(moves, values)
    if not maximizingPlayer: result.reverse() #Could be backwards
    return result

def textSize(text, size):
    font = pygame.font.Font('freesansbold.ttf', size)
    return font.size(text)

def renderCenteredText(screen, text, size, x, y, color):
    font = pygame.font.Font('freesansbold.ttf', size)
    x -= textSize(text, size)[0]//2
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

def getFlippedInDir(board, row, col, drow, dcol):
    if not (row in range(8) and col in range(8)):
        return None
    #Make sure to flip tokens before placing new one
    if board.state[row][col] == board.turn:
        return False
    elif board.state[row][col] == 0:
        return None
    result = getFlippedInDir(board, row + drow, col + dcol, drow, dcol)
    if result == None:
        return None
    elif result == False:
        return [[row, col]]
    else:
        result.append([row, col])
        return result

def getFlippedInDirState(state, row, col, drow, dcol, turn):
    if not (row in range(8) and col in range(8)):
        return None
    #Make sure to flip tokens before placing new one
    if state[row][col] == turn:
        return False
    elif state[row][col] == 0:
        return None
    result = getFlippedInDirState(state, row + drow, col + dcol, drow, dcol, turn)
    if result == None:
        return None
    elif result == False:
        return [[row, col]]
    else:
        result.append([row, col])
        return result

def getFlipped(board, square):
    row,col = square
    flipped = []
    for drow in range(-1, 2):
        for dcol in range(-1, 2):
            if not (drow == dcol == 0):
                result = getFlippedInDir(board, row + drow, col + dcol, drow, dcol)
                if result not in [False, None]: flipped += result
    return flipped

def getFlippedState(state, square, turn):
    row,col = square
    flipped = []
    for drow in range(-1, 2):
        for dcol in range(-1, 2):
            if not (drow == dcol == 0):
                result = getFlippedInDirState(state, row + drow, col + dcol, drow, dcol, turn)
                if result not in [False, None]: flipped += result
    return flipped

def getValidMoves(board):
    possibleMoves = []
    for row in range(8):
        for col in range(8):
            if board.state[row][col] == 0:
                if len(getFlipped(board, (row, col))) > 0:
                    possibleMoves.append((row, col))
    return possibleMoves

def getValidMovesState(state, turn):
    possibleMoves = []
    for row in range(8):
        for col in range(8):
            if state[row][col] == 0:
                if len(getFlippedState(state, (row, col), turn)) > 0:
                    possibleMoves.append((row, col))
    return possibleMoves

# Adapted from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def checkInGrid(aiSettings,x,y):
    """Returns true if (x,y) is inside the grid"""
    return ((aiSettings.margin <= x <= aiSettings.screenWidth - aiSettings.margin) and
            (aiSettings.margin <= y <= aiSettings.screenHeight - aiSettings.margin))

def viewToModel(aiSettings,x,y):
    """Returns the top left row and col of the mouse press"""
    if not checkInGrid(aiSettings,x,y):
        return (-1,-1)
    row = int((y-aiSettings.margin)/aiSettings.blockSize)
    col = int((x-aiSettings.margin)/aiSettings.blockSize)
    return (row,col)

def modelToView(aiSettings,row,col):
    """Returns the (x,y) coordinates of the row and col"""
    x = int(col*aiSettings.blockSize + aiSettings.margin)
    y = int(row*aiSettings.blockSize + aiSettings.margin)
    return (x,y)

class Header(object):
    def __init__(self, node):
        self.head = node

class Move(object):
    def __init__(self, prev, move, turn, first = False):
        if first:
            self.parent = None
            self.state = [[0] * 8 for i in range(8)]
            self.state[3][3] = self.state[4][4] = 1
            self.state[3][4] = self.state[4][3] = -1
            self.move = None
            self.placed = 4
        else:
            self.parent = prev
            newState = copy.deepcopy(prev.state)
            for square in getFlippedState(newState, move, turn):
                newState[square[0]][square[1]] = turn
            newState[move[0]][move[1]] = turn
            self.state = newState
            self.move = move
            self.placed = prev.placed + 1
        self.children = []
        self.moves = []
        self.score = None
    
    def resetAlphaBeta(self):
        self.alpha = None
        self.beta = None
        for child in self.children:
            child.resetAlphaBeta()

    def addChild(self, move, turn):
        self.moves.append(move)
        self.children.append(Move(self, move, turn))

#####################################################################################
# Easy Level for the AI

"""
The AI will look at all the valid moves and choose one at random
"""
#####################################################################################

def makeAIMovesEasy(board):
    if board.turn not in board.controlledColors[board.humanControlled]:
        moves = getValidMoves(board) #List of tuples of coords of possible moves
        if len(moves) == 0:
            board.turn *= -1
        else:
            if board.turn == 1:
                nextMove = random.choice(moves)
                board.place(nextMove[0], nextMove[1])
            else:
                nextMove = random.choice(moves)
                board.place(nextMove[0], nextMove[1])

#####################################################################################
# Medium Level for the AI

"""
PUT NOTES ABOUT THE MEDIUM AI HERE
"""
#####################################################################################

def makeAIMovesMedium(board):
    pass

#####################################################################################
# Hard Level for the AI

"""
Minimax Algorithm with Alpha Beta Pruning

Inspired by https://www.youtube.com/watch?v=l-hh51ncgDI

This algorithm works by maximizing the score of one player and minimizing the score of 
the other player. In our algorithm, we will have white try to maximize the score and black 
minimize the score. Each position on the board has a certain "value" that we will assign it.
When we run through the algorithm, at each turn, the pieces will check a depth of 4, meaning 
the AI will check its move, the opposite player's move, and then repeat this process once again. 
Once the AI has checked the number of different end states needed, it will choose the one 
that gives it the best outcome. If two states give the same outcome, it will choose the 
first one of the same group.

Alpha Beta Pruning:
Alpha beta pruning works by decreasing the total computation necessary for the program. 
It removes the necessity of checking every single end state by pruning the branches we 
know will not be checked. The video gives a good example of this process.
"""
#####################################################################################

def minimax(stateNode, depth, alpha, beta, maximizingPlayer, total = None):
    if total == None:
        total = stateNode.placed
        stateNode.resetAlphaBeta()
        stateNode.alpha = -1000000
        stateNode.beta = 1000000
    
    elif total == 64:
        # If the entire grid is filled
        white = 0
        for row in range(8):
            for col in range(8):
                if stateNode.state[row][col] == 1: white += 1
        if white > 32:
            return 10000, 0
        elif white < 32:
            return -10000, 0
        else:
            return 0, 0

    if depth <= 0:
        if maximizingPlayer: #White's algorithm
            return evaluateStatePrime(stateNode.state), 0
        else: #Black's algorithm
            return evaluateStatePrime(stateNode.state), 0
    
    turn = (1 if maximizingPlayer else -1)
    Eval = -1000000 * turn
    selectedMove = None
    if stateNode.children == []:
        result = getValidMovesState(copy.deepcopy(stateNode.state), turn)
        if len(result) == 0:
            return minimax(stateNode, depth - 1, alpha, beta, (not maximizingPlayer), total = total)
        for move in result:
            stateNode.addChild(move, turn)
    #Presorts possible moves to take advantage of alpha-beta pruning
    #Currently makes the thing run slower, so comment out for now
    #if depth >= 5:
    #    result = sortPossibleMoves(state, result, maximizingPlayer)
    for newState in stateNode.children:
        val = minimax(newState, depth - 1, alpha, beta, not maximizingPlayer, total = total + 1)[0]
        if (maximizingPlayer and (val > Eval)) or ((not maximizingPlayer) and (val < Eval)):
            Eval = val
            selectedMove = newState.move
        if turn == 1: alpha = max(val, alpha)
        else: beta = min(beta, val)
        if beta <= alpha:
            break
    return (Eval, selectedMove)

def makeAIMovesHard(board, tree):
    print(123)
    if board.turn not in board.controlledColors[board.humanControlled]:
        print(234)
        moves = getValidMoves(board)
        if len(moves) == 0:
            board.turn *= -1
            print(345)
        else:
            print(456)
            print(board.turn)
            if board.turn == 1:
                nextMove = (minimax(tree.head, 3, -1000000, 1000000, True))[1]
                board.place(nextMove[0], nextMove[1])
            else:
                nextMove = (minimax(tree.head, 3, -1000000, 1000000, False))[1]
                board.place(nextMove[0], nextMove[1])
            print(nextMove)
            new = tree.head.children[tree.head.moves.index(nextMove)]
            print(new.state)
            tree.head = new

#####################################################################################
# Impossible Level for the AI

"""
PUT NOTES ABOUT THE IMPOSSIBLE AI HERE
"""
#####################################################################################

def makeAIMovesImpossible(board):
    pass



#####################################################################################
# Drawing Section (View)
#####################################################################################

def drawPiece(aiSettings,screen,color,rectX,rectY):
    """Draws each individual piece on the screen"""
    radius = int(aiSettings.blockSize/2)
    startX = rectX + radius
    startY = rectY + radius
    pygame.draw.circle(screen, color, (startX,startY), radius-2,0)

def drawGrid(aiSettings, screen, board):
    """Draws the grid for the screen"""
    gridSize = aiSettings.screenWidth - 2*aiSettings.margin
    blockSize = gridSize/8
    for row in range(9):
        pygame.draw.line(screen, (0,0,0), (aiSettings.margin, aiSettings.margin + int(blockSize * row)),  
                         (aiSettings.screenWidth - aiSettings.margin, aiSettings.margin + int(blockSize * row)))
    for col in range(9):
        pygame.draw.line(screen, (0,0,0), (aiSettings.margin + int(blockSize * col), aiSettings.margin),  
                         (aiSettings.margin + int(blockSize * col), aiSettings.screenHeight - aiSettings.margin))

def drawPieces(aiSettings, screen, board):
    for row in range(8):
        for col in range(8):
            (rectX,rectY) = modelToView(aiSettings,row,col)
            if board.state[row][col] == 1:
                drawPiece(aiSettings,screen,(255, 255, 255),rectX,rectY)
            elif board.state[row][col] == -1:
                drawPiece(aiSettings,screen,(0, 0, 0),rectX,rectY)
    if board.displayPossible:
        possibleMoves = getValidMoves(board)
        for square in possibleMoves:
            (rectX,rectY) = modelToView(aiSettings, square[0], square[1])
            drawPiece(aiSettings, screen, aiSettings.possibleColor, rectX, rectY)

def drawInfo(aiSettings, screen, board):
    renderCenteredText(screen, "Currently playing as " + board.controlledNames[board.humanControlled], 20, 150, 10, (0,0,0))
    renderCenteredText(screen, board.names[board.turn] + "'s Turn", 20, aiSettings.screenWidth-150, 10, board.colors[board.turn])
    totals = board.getDist()
    renderCenteredText(screen, "Balance: " + str(int(evaluateState(board.state, totals[1] + totals[-1], 3))), 20, aiSettings.screenWidth//2, aiSettings.screenHeight - 40, board.colors[1])
    colors = [0,0,0]
    for row in board.state:
        for square in row:
            colors[square] += 1
    renderCenteredText(screen, board.names[1] + f": {colors[1]} tiles", 20, 100, aiSettings.screenHeight - 40, board.colors[1])
    renderCenteredText(screen, board.names[-1] + f": {colors[-1]} tiles", 20, aiSettings.screenWidth - 100, aiSettings.screenHeight - 40, board.colors[-1])
    renderCenteredText(screen, str(board.whiteWins), 20, aiSettings.margin//2, aiSettings.screenHeight//2, (255,255,255))
    renderCenteredText(screen, str(board.blackWins), 20, aiSettings.screenWidth - aiSettings.margin//2, aiSettings.screenHeight//2, (0,0,0))


# From https://github.com/ehmatthes/pcc/blob/master/chapter_12/game_functions.py
def updateScreen(aiSettings, screen, board):
    """Updates screen"""
    # Redraw the screen, each pass through the loop.
    screen.fill(aiSettings.bgColor)
    
    # Draws the background grid
    drawGrid(aiSettings, screen, board)

    # Draws placed pieces and possible moves
    drawPieces(aiSettings, screen, board)

    # Draws surrounding info
    drawInfo(aiSettings, screen, board)


def getTime(state, sort):
     time0 = time()
     a = minimax(state, 4, -1000000, 1000000, True, sort = sort)
     return time() - time0

def renderText(screen, text, size, x, y, color):
    font = pygame.font.Font('freesansbold.ttf', size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

def listText(screen, text, size, x, y, margin, color = None, w = None, h = None, scroll = 0, sameLineMargin = 3, indent = 0, formatting = None):
    colors = [(255,255,255), (100,100,200), (50,180,50), (180,50,180)]
    if h != None:
        final = screen
        intermediate = pygame.surface.Surface((w, h))
        screen = pygame.surface.Surface((w, 10000))
        finalY, y = y, 0
    if color == None: color = (255,255,255)
    if len(text) > 0:
        vertical = textSize(text[0], size)[1]
    else:
        vertical = 0
    w -= 2*x
    line = 0
    sameLines = 0
    if w == None:
        for i in range(len(text)):
            renderText(screen, text[i], size, x, y + line*(vertical + margin), color)
            line += 1
    else:
        height = margin
        for i in range(len(text)):
            words = text[i].split(" ")
            first = True
            cur = ""
            for word in words:
                if textSize(cur+" "+word,size)[0] > w:
                    if formatting != None:
                        if formatting[i][0] == 0:
                            renderText(screen, cur, formatting[i][1], x, y + height, colors[formatting[i][2]])
                        else:
                            renderCenteredText(screen, cur, formatting[i][1], x + w//2, height, colors[formatting[i][2]])
                        height += (sameLineMargin + textSize(cur, formatting[i][1])[1])
                    else:
                        renderText(screen, cur, size, x, y + height, color)
                        height += (sameLineMargin + textSize(cur, size)[1])
                    cur = word
                else:
                    cur = (" "*indent + word if first else cur + " " + word)
                    first = False
            if formatting != None:
                if formatting[i][0] == 0:
                    renderText(screen, cur, formatting[i][1], x, y + height, colors[formatting[i][2]])
                else:
                    renderCenteredText(screen, cur, formatting[i][1], x + w//2, y + height, colors[formatting[i][2]])
                height += (margin + textSize(cur, formatting[i][1])[1])
            else:
                renderText(screen, cur, size, x, y + height, color)
                height += (margin + textSize(cur, size)[1])
    if h != None:
        intermediate.blit(screen, (0, scroll))
        final.blit(intermediate, (x, finalY))
    nextText = (0 if len(text) == 0 else (margin + textSize(cur, size)[1]))
    return height + nextText