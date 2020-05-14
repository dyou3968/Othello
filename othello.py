#####################################################################################
# Othello 
# By David You

# A pygame recreation of the original othello board game
# Heavy pygame inspiration taken from:
# https://github.com/ehmatthes/pcc/tree/master/chapter_14
#####################################################################################

import pygame
from settings import Settings
import gameFunctions as gf

def runGame():
    # Initialize pygame, settings, and screen object.
    # Taken from https://github.com/ehmatthes/pcc/blob/master/chapter_14/alien_invasion.py
    pygame.init()
    aiSettings = Settings()
    screen = pygame.display.set_mode(
        (aiSettings.screenWidth, aiSettings.screenHeight))
    pygame.display.set_caption("Othello")

    # Set the background color.
    bgColor = (0,153,0)

    while True:
        gf.checkEvents(aiSettings,screen)
        gf.updateScreen(aiSettings,screen)


runGame()