import sys
from time import sleep

import pygame

from settings import Settings       #This is importing the module we created
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien


"""The player controls a rocket ship that appears on the bottom center of the screen.
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
        #
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # This allows the game to go into full screen. or you can use the above
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")    #sets the title on the open window

        #Create an instance to store game statistics
        self.stats = GameStats(self)

        self.ship = Ship(self) #After crating the ship module, initialized the ship and by giving the "self" argument, the ship module has access to everything
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.game_active = True


        #Set the background color.
        # self.bg_color = (200, 200, 200)   #commented this out for now since it seems like its not doing anything and i think it was deleted once we created the settings

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()  #This is what updates the shift to move. it takes in the input by the above method if any is true, the ship moves
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)  # sets the frame rate to 60 frames per "tick" = second.




    def _check_events(self):    #This is a "helper method". This works inside a class but isn't meant to be used outside the class. Helper methods begin with "_"
        """Respond to keypresses and mouse events."""
        #We are using this to shorten our run_game method.
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():  # an event is any keyboard action or mouse click.
            if event.type == pygame.QUIT:  # clicking on the x button is an event of QUIT.
                sys.exit()
            elif event.type == pygame.KEYDOWN:  #Each keystroke is registered as a keydown event by pycharm
                self._check_keydown_events(event)   #Here we just give it the event since we've already checked the type to make sure its correct.
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:  # K_RIGHT is the right arrow key.
            # Move the ship to the right by one pixel
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:   #Added the exit function to also include the letter "q". I added escape
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update """
        #Update position of bullets and get rid of old bullets.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        #Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)  #Changing bullets to false allows bullets to continue after collisions

        if not self.aliens:
            #Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        #Create an alien and keep adding aliens until there's no room left.
        #Spacing between aliens is one alien width.

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finsihed a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entrie fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        #Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #Treat this the same as if the ship got hit. if you make a hole and an alien gets through, the game ends
                self._ship_hit()
                break


    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships left.
            self.stats.ships_left -= 1

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #Pause
            sleep(1.0)
        else:
            self.game_active = False

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)   #create the image of the alien on the screen

        # Make the most recently drawn screen visible.
        pygame.display.flip()  # refreshes the screen. documentation unclear maybe ask grok





ai = AlienInvasion()    #initialize "ai" as our game
ai.run_game()   #run the game by using the method which stores the loop