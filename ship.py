import pygame

class Ship:
    """A class to manage the ship"""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen    #I believe this sets the image of the ship
        self.screen_rect = ai_game.screen.get_rect()    #And this sets the location?

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')   #pygame.image.load(image) actually loads the image so we assign it
        self.rect = self.image.get_rect()   #This "gets" the location of the image

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)