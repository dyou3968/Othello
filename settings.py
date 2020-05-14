#####################################################################################
# Settings page 
#####################################################################################

class Settings():
    """Stores all the settings for the game."""

    def __init__(self):
        """ Game's static settings """
        # Screen settings.
        self.screenWidth = 900
        self.screenHeight = 900
        self.blockSize = 100
        self.margin = 50
        self.bgColor = (0,153,0)