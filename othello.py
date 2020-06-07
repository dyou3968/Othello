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
        self.currDisp = 0

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif (event.type == pygame.MOUSEBUTTONDOWN) and (self.currDisp == 0):
                mouseX,mouseY = pygame.mouse.get_pos()
                (row,col) = viewToModel(self.aiSettings,mouseX,mouseY)
                if (row in range(8) and col in range(8)):
                    if self.board.place(row, col):
                        updateScreen(self.aiSettings, self.screen, self.board)
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_r) and (self.currDisp == 0):
                    self.board.reset()

                # Other screen testing
                if event.key == pygame.K_DOWN:
                    self.currDisp = 0
                if event.key == pygame.K_LEFT:
                    self.currDisp = 1 
                if event.key == pygame.K_RIGHT:
                    self.currDisp = 2
                if event.key == pygame.K_UP:
                    self.currDisp = 3

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