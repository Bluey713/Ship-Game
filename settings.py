class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings."""
        #Screen settings
        self.screen_width = 1200        #We are using this to be able to easily change settings by calling this method instead of manually having to change each instance
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #Ship settings
        self.ship_speed = 1.5
