import sys
import pygame
from settings import Settings

"""The player controsl a rocket ship that appears on the bottom center of the screen.
The player can move the ship left and right and shoots bullets with the space bar.
When the game begins a fleet of aliens appears."""

class AlienInvasion:
    """Overall class to manage game assets and behavior"""
    def __init__(self) -> None:
        """Initialized the game, and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #Set the background color.
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            #Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            #Redraw the screen during each pass through the loop.
            self.screen.fill(self.settings.bg_color)

            #Make the most recently drawn screen visible.
            pygame.display.flip()
            self.clock.tick(60)     #sets the frame rate to 60fps

ai = AlienInvasion()
ai.run_game()