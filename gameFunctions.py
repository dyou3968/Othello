import sys
import pygame

# From https://github.com/ehmatthes/pcc/blob/master/chapter_12/game_functions.py

def getRowAndCol(aiSettings,x,y):
    """Returns the top left row and col of the mouse press."""
    row = (y-aiSettings.margin)//aiSettings.blockSize
    col = (x-aiSettings.margin)//aiSettings.blockSize
    return (row,col)

def checkEvents(aiSettings,screen):
    """Respond to user events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX,mouseY = pygame.mouse.get_pos()
            (row,col) = getRowAndCol(aiSettings,mouseX,mouseY)
            print(mouseX,mouseY)
            print(row,col)

def drawPiece(aiSettings,screen,color,startX,startY,radius):
    """Draws each individual piece on the screen."""
    pygame.draw.circle(screen, color, (startX,startY), radius,0)

def drawGrid(aiSettings, screen):
    """Draws the grid for the screen."""
    gridSize = aiSettings.screenWidth - 2*aiSettings.margin
    blockSize = gridSize//8
    for row in range(8):
        for col in range(8):
            rectX = col*blockSize+(blockSize//2)
            rectY = row*blockSize+(blockSize//2)
            rect = pygame.Rect(rectX, rectY, aiSettings.blockSize, aiSettings.blockSize)
            pygame.draw.rect(screen,(0,0,0),rect,2)


            # Draws each individaul piece
            radius = 50
            startX = rectX + radius
            startY = rectY + radius
            black = (0,0,0)
            white = (255,255,255)
            if (row+col)%2 == 0:
                drawPiece(aiSettings,screen,black,startX,startY,radius)
            else:
                drawPiece(aiSettings,screen,white,startX,startY,radius)


def updateScreen(aiSettings, screen):
    """Updates screen."""
    # Redraw the screen, each pass through the loop.
    screen.fill(aiSettings.bgColor)
    
    # Draws the background grid
    drawGrid(aiSettings, screen)

    pygame.display.flip()