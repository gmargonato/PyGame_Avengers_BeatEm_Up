
import pygame
from utils import *

class Webnet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'webnet'                
        self.sprites = load_sprites_from_folder("ASSETS/WEBNET")
        self.image_web_down = self.sprites[0]
        self.image_web_up = self.sprites[1]
        self.rect = self.image_web_down.get_rect()
        self.rect.center = (x, 0)
        self.enemy_y = y
        self.status = 0
        
    def update(self, scroll, fps):        
        if self.status == 0:
            if self.rect.y < self.enemy_y:
                self.rect.y += 20
            else:
                self.status = 1
        else:
            self.rect.y -= 40
            if self.rect.bottom < -100:
                self.kill()

    def draw(self, screen, grid):
        # Image
        if self.status == 0:
            screen.blit(self.image_web_down, (self.rect.x,self.rect.y))
        else:
            screen.blit(self.image_web_up, (self.rect.x,self.rect.y))

        if grid:
            # Hitbox
            pygame.draw.rect(screen, COLOR_GREEN, self.rect, 1)
        