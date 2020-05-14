#####################################################################################
# Othello 
# By David You

# A pygame recreation of the original othello board game
# Heavy pygame inspiration taken from:
# https://github.com/ehmatthes/pcc/tree/master/chapter_14
#####################################################################################


class Settings():
    """Stores all the settings for the game."""

    def __init__(self):
        """ Game's static settings """
        # Screen settings.
        self.screen_width = 800
        self.screen_height = 800
        self.bg_color = (0,153,0)