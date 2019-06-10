#import 3rd party libraries
import pygame
from pygame import freetype

#import my files
import camera
import input
import player
import resource
import screen
from settings import *
import sound_controller
import video_controller




class Game:
    def __init__(self):
        #initialize modules
        pygame.init()



        #instances of all the classes
        self.screen = screen.Screen(self)
        self.camera = camera.Camera(self)
        self.input = input.Input_Controller(self)
        self.player = player.Player(self)
        self.resource = resource.Resource(self)
        self.sound_controller = sound_controller.Sound(self)
        self.video_controller = video_controller.Video(self)

        #initialize all the variables and groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.items = pg.sprite.Group()

        #game specific variables
        self.paused = False
        self.running = True

    def show_start_screen(self):
        #start screen with menu would be referenced here
        pass

    def game_loop(self):
        self.show_start_screen()
        pg.mixer.music.play(loops=-1)
        while running:
            #dt is the delta time for the 60 fps clock
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            #events
            self.input.events()
            if not self.paused:
                self.update()
            self.screen.draw()
        #go screen means game over screen
        self.show_go_screen()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # game over?
        if 'game winning condition is met':
            self.playing = False

        '''
        #collision detection
        #define a variable as a list of sprites collided between a sprite and group        
        hits = pg.sprite.spritecollide(self.player, 'group the player collided with', False)
        for hit in hits:
            if hit.type == 'something':
                do something
            if hit.type == 'shotgun':
                #hit.kill removes the item
                hit.kill()

        #collision between two groups
        #bullets hit mobs
        
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            # hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = vec(0, 0)
        '''

    def show_go_screen(self):
        #game over screen
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.resource.title_font, 100, RED,
                       WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("Press a key to start", self.resource.title_font, 75, WHITE,
                       WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pg.display.flip()
        self.wait_for_key()


def main():
    game_instance = Game()
    game_instance.game_loop()


if __name__ == 'main':
    main()