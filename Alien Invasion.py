import sys
import pygame
from settings import Settings       #This is importing the module we created
from ship import Ship

"""The player controsl a rocket ship that appears on the bottom center of the screen.
The player can move the ship left and right and shoots bullets with the space bar.
When the game begins a fleet of aliens appears."""

class AlienInvasion:
    """Overall class to manage game assets and behavior"""
    def __init__(self) -> None:
        """Initialized the game, and create game resources"""
        pygame.init()   #initialized all imported modules instead of initializing each one we use
        self.clock = pygame.time.Clock()    #Creates an object to help track time; which we'll then use to track fps
        self.settings = Settings()  #here we initialize the Settings module by calling it self.settings.whatever_method_is_in_Settings.

        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height)) #returns a "surface" = screen. see documentation
        pygame.display.set_caption("Alien Invasion")    #sets the title on the open window

        self.ship = Ship(self) #After crating the ship module, initialized the ship and by giving the "self" argument, the ship module has access to everything

        #Set the background color.
        # self.bg_color = (200, 200, 200)   #commented this out for now since it seems like its not doing anything

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            #Redraw the screen during each pass through the loop.
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()

            #Make the most recently drawn screen visible.
            pygame.display.flip()   #refreshes the screen. documentation unclear maybe ask grok
            self.clock.tick(60)     #sets the frame rate to 60 frames per "tick" = second.

    def _check_events(self):    #This is a "helper method". This works inside a class but isn't meant to be used outside the class. Helper methods begin with "_"
        """Respond to keypresses and mouse events."""
        #We are using this to shorten our run_game method.
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():  # an event is any keyboard action or mouse click.
            if event.type == pygame.QUIT:  # clicking on the x button is an event of QUIT.
                sys.exit()


ai = AlienInvasion()    #initialize "ai" as our game
ai.run_game()   #run the game by using the method which stores the loop