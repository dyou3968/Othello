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

                # Other screen testing
                if event.key == pygame.K_LEFT:
                    self.show_intro_screen()
                if event.key == pygame.K_RIGHT:
                    self.show_AI_screen()  
                if event.key == pygame.K_UP:
                    self.show_howToPlay_screen()

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
        
        pygame.display.flip()
        self.wait_for_key()

    def generateText(self, startX, startY, line1, line3, spacing, font):
        # Generates the three lines of text given the input and the spacing
        renderCenteredText(self.screen, line1, font, startX, startY - spacing, (0,0,0))
        renderCenteredText(self.screen, 'Vs.', font, startX, startY, (0,0,0))
        renderCenteredText(self.screen, line3, font, startX, startY + spacing, (0,0,0))

#####################################################################################
# This is the intro screen where the player chooses from the following four options

# Easy
# Medium
# Hard
# Impossible
#####################################################################################

    def show_AI_screen(self):
        self.screen.fill(self.bgColor)
        titleFontSize = 64
        buttonFontSize = 32
        thickness = 2
        startWidth = self.aiSettings.screenWidth//4
        startHeight = self.aiSettings.screenHeight//2

        # Extra spacing for design purposes
        widthSpacing = 30 
        heightSpacing = 30

        # Title
        renderCenteredText(self.screen, "AI Levels", titleFontSize, self.aiSettings.screenWidth//2, self.aiSettings.screenHeight*2//10, (0,0,0))

        levels = ["Easy", "Medium", "Hard"]
        for i in range(len(levels)):
            curLevel = levels[i]
            placement = i + 1
            renderCenteredText(self.screen, curLevel, buttonFontSize, startWidth*placement, startHeight, (0,0,0))
            curWidth, curHeight = self.textSize(curLevel, buttonFontSize)[0], self.textSize(curLevel, buttonFontSize)[1]
            self.generateTextBox(startWidth*placement, startHeight + heightSpacing//2, curWidth + widthSpacing, curHeight + heightSpacing, thickness)

        # Impossible
        renderCenteredText(self.screen, "Impossible", buttonFontSize, self.aiSettings.screenWidth*2//4, self.aiSettings.screenHeight*3//4, (0,0,0))
        impossibleWidth, impossibleHeight = self.textSize("Impossible", buttonFontSize)[0], self.textSize("Impossible", buttonFontSize)[1]
        self.generateTextBox(self.aiSettings.screenWidth*2//4, self.aiSettings.screenHeight*3//4 + heightSpacing//2, impossibleWidth + widthSpacing, impossibleHeight + heightSpacing, thickness)

        pygame.display.flip()
        self.wait_for_key()


#####################################################################################
# How to Play Screen
#####################################################################################

    def show_howToPlay_screen(self):
        """
        Note:
        The text does not look good nor does it fit when I try to put all 10 bullet points on the same page
        Given the spacing as well, I believe the best approach would be to split it up, increase the spacing, and 
        put the text for 6-10 on a second page.
        """
        self.screen.fill(self.bgColor)
        titleFontSize = 64
        buttonFontSize = 32
        thickness = 2
        startWidth = self.aiSettings.screenWidth//2
        startHeight = self.aiSettings.screenHeight//5
        
        # Extra spacing for design purposes
        widthSpacing = 30 
        heightSpacing = 30

        # Title
        renderCenteredText(self.screen, "How to Play", titleFontSize, self.aiSettings.screenWidth//2, self.aiSettings.screenHeight//20, (0,0,0))

        # Description
        # Gameplay taken from https://www.fgbradleys.com/rules/Othello.pdf
        description = [ "1. White always goes first.", 
                        "2. If on your turn, you cannot outflank and flip at least one opposing disc",
                        "   your turn is forfeited and your opponent moves again. However, if a move",
                        "   is available to you, you may not forfeit your turn.",
                        "3. A disc may outflank any number of discs in one or more rows in any number",
                        "   of directions at the same time – horizontally, vertically or diagonally",
                        "4. You may not skp over your own color disc to outflank an opposing disc.",
                        "5. Disc(s) may only be outflanked as a direct result of a move and must fall",
                        "   in the direct line of the disc placed down.",
                        "6. All discs outflanked in any one move must be flipped, even if it is to",
                        "   the player's advantage not to flip them at all.",
                        "7. A player who flips a disc which should not have been turned may correct",
                        "   the mistake as long as the opponent has not made a subsequent move.",
                        "   If the opponent has already moved, it is too late to change and the",
                        "   disc(s) remain as is.",
                        "8. Once a disc is placed on a square, it can never be moved to another",
                        "   square later in the game.",
                        "9. If a player runs out of discs, but still has an opportunity to",
                        "   outflank an opposing disc on his or her turn, the opponent must give the",
                        "   player a disc to use.",
                        "10. When it is no longer possible for either player to move, the game is over.",
                        "   Discs are counted and the player with the majority of his or her color",
                        "   discs on the board is the winner."]


        for i in range(len(description)):
            curLevel = description[i]
            spacing = 40 * i
            renderCenteredText(self.screen, curLevel, int(buttonFontSize//2.1), startWidth, startHeight + spacing, (0,0,0))

        # Return to Home Screen
        renderCenteredText(self.screen, "Return to Home Screen", buttonFontSize, startWidth, self.aiSettings.screenHeight*9//10, (0,0,0))
        impossibleWidth, impossibleHeight = self.textSize("Return to Home Screen", buttonFontSize)[0], self.textSize("Return to Home Screen", buttonFontSize)[1]
        self.generateTextBox(startWidth, self.aiSettings.screenHeight*9//10 + heightSpacing//2, impossibleWidth + widthSpacing, impossibleHeight + heightSpacing, thickness)

        pygame.display.flip()
        self.wait_for_key()


#####################################################################################
# Useful helper functions for all screens
#####################################################################################

    def textSize(self, text, size):
        # Returns the width and height of the text
        font = pygame.font.Font('freesansbold.ttf', size)
        return font.size(text)


    def generateTextBox(self, centerX, centerY, boxWidth, boxHeight, thickness):
        # Generates the textbox around the lines of text
        leftSide = centerX - boxWidth//2
        topSide = centerY - boxHeight//2
        rect = pygame.Rect(leftSide,topSide,boxWidth,boxHeight)
        pygame.draw.rect(self.screen, (0,0,0), rect, thickness)




#####################################################################################

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