#####################################################################################
# Othello 
# By David You and Sean Swayze

# A pygame recreation of the original othello board game
# Heavy pygame inspiration taken from:
# https://github.com/ehmatthes/pcc/tree/master/chapter_14
# https://www.pygame.org/docs/
#####################################################################################

import pygame, os
from settings import *
from gameFunctions import *

pygame.init()

class Game:
    def __init__(self):
        # Initialize pygame, settings, and screen object.
        # Taken from https://github.com/ehmatthes/pcc/blob/master/chapter_14/alien_invasion.py
        self.PGclock = pygame.time.Clock()

        self.aiSettings = Settings()
        self.screen = pygame.display.set_mode(
            (self.aiSettings.screenWidth, self.aiSettings.screenHeight))
        self.board = Board()
        pygame.display.set_caption("Othello")

        # Set the background color.
        self.bgColor = (0,153,0)

        self.running = True
        self.makeAIMoves = False

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX,mouseY = pygame.mouse.get_pos()
                (row,col) = viewToModel(self.aiSettings,mouseX,mouseY)
                if (row in range(8) and col in range(8)):
                    if self.board.place(row, col):
                        updateScreen(self.aiSettings, self.screen, self.board)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.board.reset()
                if not self.board.over:
                    if event.key == pygame.K_d:
                        self.board.displayPossible = not self.board.displayPossible
                    elif event.key == pygame.K_w:
                        self.board.humanControlled = 1
                    elif event.key == pygame.K_b:
                        self.board.humanControlled = -1
                    elif event.key == pygame.K_h:
                        self.board.humanControlled = 0
                    elif event.key == pygame.K_n:
                        self.board.humanControlled = 2
                    elif event.key == pygame.K_a:
                        self.makeAIMoves = not self.makeAIMoves

        if self.makeAIMoves and not self.board.over:
            makeAIMove(self.board)
            updateScreen(self.aiSettings, self.screen, self.board)
        if self.board.over:
            # Shows the gameover screen
            self.show_go_screen()
        
        updateScreen(self.aiSettings, self.screen, self.board)
        
        pygame.display.flip()
        self.PGclock.tick(40)



#####################################################################################
# Adapted from https://github.com/kidscancode/pygame_tutorials/blob/master/platform/part%207/main.py
#####################################################################################
    def wait_for_key(self):
        # Executes a specific function when any key is pressed
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False
                    if event.key == pygame.K_r:
                        self.board.reset()

    def show_start_screen(self):
        # Othello start screen
        self.screen.fill(self.bgColor)
        renderCenteredText(self.screen, "Othello", 48, self.aiSettings.screenWidth//2, self.aiSettings.screenHeight//3, (0,0,0))
        renderCenteredText(self.screen, "Press any key to start", 24, self.aiSettings.screenWidth//2, self.aiSettings.screenHeight*2//3, (0,0,0))
        pygame.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # Screen when the game is over
        if not self.running:
            return
        renderCenteredText(self.screen, "Game Over", 48, self.aiSettings.screenWidth//2, self.aiSettings.screenHeight//3, (150,0,150))
        renderCenteredText(self.screen, "Press r to play again", 22, self.aiSettings.screenWidth//2, self.aiSettings.screenHeight*3//4, (150,0,150))
        pygame.display.flip()
        self.wait_for_key()


#####################################################################################


#####################################################################################
# This is the intro screen where the player chooses from the following three options

# Human Vs. Human
# Human Vs. AI
# AI Vs. AI

# There is also a screen that goes to the "how to play" screen
#####################################################################################

    def show_intro_screen(self):
        # Othello start screen
        self.screen.fill(self.bgColor)
        text1 = 'Human'
        text2 = 'AI '
        spacing = 50
        fontSize = 36
        startWidth = self.aiSettings.screenWidth//6
        startHeight = self.aiSettings.screenHeight*2//5
        boxWidth = fontSize*4
        boxHeight = fontSize*4 #The pixel height is always one more than the font size. Since we have three lines here, it has three extra
        thickness = 2

        # Leftmost human vs. human 
        self.generateText(startWidth, startHeight, text1, text1, spacing, fontSize)
        self.generateTextBox(startWidth, startHeight + spacing//3, boxWidth, boxHeight, thickness)

         # Middle human vs. AI
        self.generateText(startWidth*3, startHeight, text1, text2, spacing, fontSize)
        self.generateTextBox(startWidth*3, startHeight + spacing//3, boxWidth, boxHeight, thickness)

         # Rightmost AI vs. AI
        self.generateText(startWidth*5, startHeight, text2, text2, spacing, fontSize)
        self.generateTextBox(startWidth*5, startHeight + spacing//3, boxWidth, boxHeight, thickness)

        # How to play text and textbox
        renderCenteredText(self.screen, "How to Play", fontSize, self.aiSettings.screenWidth//2, self.aiSettings.screenHeight*8//10, (0,0,0))
        howToPlayWidth = self.textSize("How to Play", fontSize)[0] + spacing
        howToPlayHeight = self.textSize("How to Play", fontSize)[1] + spacing
        self.generateTextBox(self.aiSettings.screenWidth//2, self.aiSettings.screenHeight*8//10 + spacing//3, howToPlayWidth, howToPlayHeight, thickness)
        #print(self.textSize("How to Play", fontSize))
        
        pygame.display.flip()
        self.wait_for_key()

    def textSize(self, text, size):
        # Returns the width and height of the text
        font = pygame.font.Font('freesansbold.ttf', size)
        return font.size(text)

    def generateText(self, startX, startY, line1, line3, spacing, font):
        # Generates the three lines of text given the input and the spacing
        renderCenteredText(self.screen, line1, font, startX, startY - spacing, (0,0,0))
        renderCenteredText(self.screen, 'Vs.', font, startX, startY, (0,0,0))
        renderCenteredText(self.screen, line3, font, startX, startY + spacing, (0,0,0))

    def generateTextBox(self, centerX, centerY, boxWidth, boxHeight, thickness):
        # Generates the textbox around the lines of text
        leftSide = centerX - boxWidth//2
        topSide = centerY - boxHeight//2
        rect = pygame.Rect(leftSide,topSide,boxWidth,boxHeight)
        pygame.draw.rect(self.screen, (0,0,0), rect, thickness)




#####################################################################################

g = Game()
g.show_intro_screen()
while g.running:
    g.update()

pygame.quit()
os._exit(0)


# g = Game()
# #g.show_start_screen()
# g.show_intro_screen()
# while g.running:
#     g.update()

# pygame.quit()
# os._exit(0)