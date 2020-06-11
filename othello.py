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
        self.screens = Screens(self)
        pygame.display.set_caption("Othello")

        # Set the background color.
        self.bgColor = (0,153,0)

        # Set the current display to the start screen
        self.currDisp = 5
        
        # Boolean conditions
        self.running = True
        self.currDisp = 5
        self.infoScroll = 0
        self.maxInfoScroll = 220
        self.makeAIMovesEasy = False
        self.makeAIMovesMedium = False
        self.makeAIMovesHard = False
        self.makeAIMovesImpossible = False

#####################################################################################
# Current Display Notes:
# 0 = Main game screen
# 1 = Intro screen
# 2 = AI level screen
# 3 = how to play screen
# 4 = gameover screen
# 5 = start screen
# 6 = white or black screen
#####################################################################################

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (event.type == pygame.MOUSEBUTTONDOWN):
                self.mousePresses(event)
            if (event.type == pygame.KEYDOWN):
                self.keyPresses(event)

        self.screenUpdates()

        pygame.display.flip()
        self.PGclock.tick(40)



#####################################################################################
# Update helper functions
#####################################################################################
    
    def screenUpdates(self):
        # Screen updates for the game
        updateScreen(self.aiSettings, self.screen, self.board)
        if self.board.over: # Shows the gameover screen
            self.currDisp = 4
            #updateScreen(self.aiSettings, self.screen, self.board)
        else: # Game still in play
            self.AIMoves()
        self.changeScreens(self.currDisp)

    def AIMoves(self):
        if self.makeAIMovesEasy:
            makeAIMovesEasy(self.board)        
        elif self.makeAIMovesMedium:
            pass
            #makeAIMovesMedium(self.board)      
        elif self.makeAIMovesHard:
            makeAIMovesHard(self.board)
        elif self.makeAIMovesImpossible:
            pass
            #makeAIMovesImpossible(self.board)     

    def mousePresses(self, event):
        # Mouse presses when the game is in play
        if self.currDisp == 0:
            self.gameplayMousePresses()
        # Mouse presses when on the intro screen
        elif self.currDisp == 1:
            self.introScreenMousePresses()
        # Mouse presses when on the AI screen
        elif self.currDisp == 2:
            self.AIScreenMousePresses()
        # Mouse presses when on the how to play screen
        elif self.currDisp == 3:
            self.howToPlayMousePresses(event)
        # Mouse presses when on the white or black screen
        elif self.currDisp == 6:
            self.whiteOrBlackMousePresses()

    def howToPlayMousePresses(self, event):
        # Updates when the how to play screen mouse presses
        mouseX,mouseY = pygame.mouse.get_pos()
        if (100 <= mouseX <= 525) and (495 <= mouseY <= 585):
            self.currDisp = 1
        #Idea from https://stackoverflow.com/questions/24518573/pygame-scrolling-down-page
        if event.button == 4: 
            self.infoScroll = min(self.infoScroll + 15, 0)
        if event.button == 5: 
            self.infoScroll = max(self.infoScroll - 15, -self.maxInfoScroll)

    def gameplayMousePresses(self):
        # Updates when the game is in play
        mouseX,mouseY = pygame.mouse.get_pos()
        (row,col) = viewToModel(self.aiSettings,mouseX,mouseY)
        if (row in range(8) and col in range(8)):
            if self.board.place(row, col):
                updateScreen(self.aiSettings, self.screen, self.board)

    def introScreenMousePresses(self):
        # Updates the intro screen mouse presses
        mouseX,mouseY = pygame.mouse.get_pos()
        yUpperBound, yLowerBound = 185, 325
        if (30 <= mouseX <= 170) and (yUpperBound <= mouseY <= yLowerBound):
            self.board.humanControlled = 0 #Both human players
            self.currDisp = 0
        elif (230 <= mouseX <= 370) and (yUpperBound <= mouseY <= yLowerBound):
            self.currDisp = 6 # One human player, choose white or black
        elif (430 <= mouseX <= 570) and (yUpperBound <= mouseY <= yLowerBound):
            self.board.humanControlled = 2 # No human players
            self.currDisp = 2
        elif (175 <= mouseX <= 425) and (455 <= mouseY <= 535):
            self.currDisp = 3

    def AIScreenMousePresses(self):
        # Updates the AI screen mouse presses
        mouseX,mouseY = pygame.mouse.get_pos()
        yUpperBound, yLowerBound = 285, 345
        if (100 <= mouseX <= 200) and (yUpperBound <= mouseY <= yLowerBound):
            self.currDisp = 0
            self.makeAIMovesEasy = True
        elif (225 <= mouseX <= 375) and (yUpperBound <= mouseY <= yLowerBound):
            print("Medium")
            #self.currDisp = 0
            #self.makeAIMovesMedium = True
        elif (400 <= mouseX <= 500) and (yUpperBound <= mouseY <= yLowerBound):
            self.currDisp = 0
            self.makeAIMovesHard = True
        elif (200 <= mouseX <= 400) and (435 <= mouseY <= 495):
            print("Impossible")
            #self.currDisp = 0
            #self.makeAIMovesImpossible = True

    def whiteOrBlackMousePresses(self):
        mouseX,mouseY = pygame.mouse.get_pos()
        if (140 <= mouseX <= 260) and (285 <= mouseY <= 345):
            self.board.humanControlled = 1 # Human is white
            self.currDisp = 2
        elif (340 <= mouseX <= 460) and (285 <= mouseY <= 345):
            self.board.humanControlled = -1 # Human is black
            self.currDisp = 2

    def keyPresses(self, event):
        if self.currDisp == 5: # Start screen
            self.currDisp = 1
        elif (event.key == pygame.K_r) and (self.currDisp in (0,4)):
            self.board.reset()
            self.currDisp = 0
        elif not self.board.over:
            if event.key == pygame.K_d:
                self.board.displayPossible = not self.board.displayPossible

    def changeScreens(self, currDisp):
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
        elif self.currDisp == 6:
            self.screens.white_or_black_screen()

#####################################################################################

g = Game()
while g.running:
    g.update()

pygame.quit()
os._exit(0)
