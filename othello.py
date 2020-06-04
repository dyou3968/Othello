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

        self.board = Board()
        self.aiSettings = Settings()
        self.screen = pygame.display.set_mode(
            (self.aiSettings.screenWidth, self.aiSettings.screenHeight))
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
                print(self.board.state)
                mouseX,mouseY = pygame.mouse.get_pos()
                (row,col) = viewToModel(self.aiSettings,mouseX,mouseY)
                if (row in range(8) and col in range(8)):
                    if self.board.place(row, col):
                        pass
                        #nextMove = (minimax(board.state, 4, -1000000, 1000000, (True if board.turn == 1 else False)))
                        #print(nextMove)
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
        if self.makeAIMoves and self.board.over:
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

g = Game()
g.show_start_screen()
while g.running:
    g.update()

pygame.quit()
os._exit(0)