import sys
import pygame

"""The player controsl a rocket ship that appears on the bottom center of the screen.
The player can move the ship left and right and shoots bullets with the space bar.
When the game begins a fleet of aliens appears."""

class AlienInvasion:
    """Overall class to manage game assets and behavior"""
    def __init__(self):
        """Initialized the game, and create game resources"""
        pygame.init()

        self.screen = pygame.display.set_mode((1200,800))
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            #Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            #Make the most recently drawn screen visible.
            pygame.display.flip()

ai = AlienInvasion()
ai.run_game()