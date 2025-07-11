import pygame

class Ship:
    """A class to manage the ship"""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen    #I believe this sets the image of the ship
        self.settings = ai_game.settings    #I beleive we call it ai_game.settings is because in AI, it calls from settings?
        self.screen_rect = ai_game.screen.get_rect()    #And this sets the location?

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')   #pygame.image.load(image) actually loads the image so we assign it
        self.rect = self.image.get_rect()   #This "gets" the location of the image

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

       #Store a float for the ship's exact horizontal position.
        self.x = float(self.rect.x) #rect only returns integers so we need to convert them to floats since we'll use a float for the speed

        #Movement flag: start with a ship that's not moving.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        #Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        #Update rect object form self.x.
        self.rect.x = self.x


    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)