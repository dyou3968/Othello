import sys
import pygame


# Adapted from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def checkInGrid(aiSettings,x,y):
    """Returns true if (x,y) is inside the grid"""
    return ((aiSettings.margin <= x <= aiSettings.screenWidth - aiSettings.margin) and
            (aiSettings.margin <= y <= aiSettings.screenHeight - aiSettings.margin))

def viewToModel(aiSettings,x,y):
    """Returns the top left row and col of the mouse press"""
    if not checkInGrid(aiSettings,x,y):
        return (-1,-1)
    row = (y-aiSettings.margin)//aiSettings.blockSize
    col = (x-aiSettings.margin)//aiSettings.blockSize
    return (row,col)

def modelToView(aiSettings,row,col):
    """Returns the (x,y) coordinates of the row and col"""
    x = col*aiSettings.blockSize + aiSettings.margin
    y = row*aiSettings.blockSize + aiSettings.margin
    return (x,y)

# From https://github.com/ehmatthes/pcc/blob/master/chapter_12/game_functions.py

def checkEvents(aiSettings,screen):
    """Respond to user events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX,mouseY = pygame.mouse.get_pos()
            (row,col) = viewToModel(aiSettings,mouseX,mouseY)
            (rectX,rectY) = modelToView(aiSettings,row,col)

            # Draws each individual piece
            black = (0,0,0)
            white = (255,255,255)
            if (row+col)%2 == 0:
                drawPiece(aiSettings,screen,black,rectX,rectY,radius = 50)
            else:
                drawPiece(aiSettings,screen,white,rectX,rectY,radius = 50)

def drawPiece(aiSettings,screen,color,rectX,rectY,radius = 50):
    """Draws each individual piece on the screen"""
    startX = rectX + radius
    startY = rectY + radius
    pygame.draw.circle(screen, color, (startX,startY), radius,0)

# class Board(object):
#     def __init__(self):
#         # Empty 2d list with all zeros
#         # If we add a white tile, it's changed to 1
#         # If we add a black tile, it's changed to -1   

def drawGrid(aiSettings, screen):
    """Draws the grid for the screen"""
    gridSize = aiSettings.screenWidth - 2*aiSettings.margin
    blockSize = gridSize//8
    for row in range(8):
        for col in range(8):
            rectX = col*blockSize+(blockSize//2)
            rectY = row*blockSize+(blockSize//2)
            rect = pygame.Rect(rectX, rectY, aiSettings.blockSize, aiSettings.blockSize)
            pygame.draw.rect(screen,(0,0,0),rect,2)

# From https://github.com/ehmatthes/pcc/blob/master/chapter_12/game_functions.py
def updateScreen(aiSettings, screen):
    """Updates screen"""
    # Redraw the screen, each pass through the loop.
    screen.fill(aiSettings.bgColor)
    
    # Draws the background grid
    drawGrid(aiSettings, screen)

    # Checks the events going on the in game
    checkEvents(aiSettings,screen)

