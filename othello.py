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
from screens import *

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
        self.screens = Screens()
        pygame.display.set_caption("Othello")

        # Set the background color.
        self.bgColor = (0,153,0)

        self.running = True
        self.makeAIMoves = False
        self.currDisp = 5

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Mouse presses when the game is in play
            if (event.type == pygame.MOUSEBUTTONDOWN) and (self.currDisp == 0):
                mouseX,mouseY = pygame.mouse.get_pos()
                (row,col) = viewToModel(self.aiSettings,mouseX,mouseY)
                if (row in range(8) and col in range(8)):
                    if self.board.place(row, col):
                        updateScreen(self.aiSettings, self.screen, self.board)

            # Mouse presses when on the intro screen
            if (event.type == pygame.MOUSEBUTTONDOWN) and (self.currDisp == 1):
                mouseX,mouseY = pygame.mouse.get_pos()
                yUpperBound, yLowerBound = 185, 325
                if (30 <= mouseX <= 170) and (yUpperBound <= mouseY <= yLowerBound):
                    self.board.humanControlled = 0 #Both human players

                elif (230 <= mouseX <= 370) and (yUpperBound <= mouseY <= yLowerBound):
                    pass
                    # NOTE: MAKE WHITE OR BLACK SCREEN FOR HUMAN VS AI
                    #self.currDisp = 2
                elif (430 <= mouseX <= 570) and (yUpperBound <= mouseY <= yLowerBound):
                    self.board.humanControlled = 2 # No human players
                    self.currDisp = 2
                elif (175 <= mouseX <= 425) and (455 <= mouseY <= 535):
                    self.currDisp = 3
        
            # Mouse presses when on the AI screen
            if (event.type == pygame.MOUSEBUTTONDOWN) and (self.currDisp == 2):
                mouseX,mouseY = pygame.mouse.get_pos()
                yUpperBound, yLowerBound = 285, 345
                if (100 <= mouseX <= 200) and (yUpperBound <= mouseY <= yLowerBound):
                    print("Easy")
                elif (225 <= mouseX <= 375) and (yUpperBound <= mouseY <= yLowerBound):
                    print("Medium")
                elif (400 <= mouseX <= 500) and (yUpperBound <= mouseY <= yLowerBound):
                    self.currDisp = 0
                    self.makeAIMoves = True
                    print("Hard")

                elif (200 <= mouseX <= 400) and (435 <= mouseY <= 495):
                    print("Impossible")

            if event.type == pygame.KEYDOWN:
                if self.currDisp == 5: # Start screen
                    self.currDisp = 1
                elif (event.key == pygame.K_r) and (self.currDisp in (0,4)):
                    self.board.reset()

                # Other screen testing
                elif event.key == pygame.K_DOWN:
                    self.currDisp = 0 # Main game screen
                elif event.key == pygame.K_LEFT:
                    self.currDisp = 1 # Intro screen
                elif event.key == pygame.K_RIGHT:
                    self.currDisp = 2 # AI level screen
                elif event.key == pygame.K_UP:
                    self.currDisp = 3 # How to play screen

                elif not self.board.over:
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
            self.currDisp = 4
            
        if self.currDisp == 0:
            updateScreen(self.aiSettings, self.screen, self.board)
        elif self.currDisp == 1:
            self.screens.show_intro_screen()
        elif self.currDisp == 2:
            self.screens.show_AI_screen()  
        elif self.currDisp == 3:
            self.screens.show_howToPlay_screen()
        elif self.currDisp == 4:
            self.screens.show_go_screen()
        elif self.currDisp == 5:
            self.screens.show_start_screen()

        pygame.display.flip()
        self.PGclock.tick(40)

g = Game()

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
#Test