#####################################################################################
# Settings page 
#####################################################################################

class Settings():
    """Stores all the settings for the game."""

    def __init__(self):
        """ Game's static settings """
        # Screen settings.
        self.screenWidth = 600
        self.screenHeight = 600
        self.margin = 50
        self.blockSize = (self.screenHeight - self.margin * 2)/8
        self.bgColor = (0,153,0)
        self.possibleColor = (100, 0, 100)