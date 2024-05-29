
import pygame
import math
from utils import *

class Mjolnir(pygame.sprite.Sprite):
    def __init__(self, x, y, floor, flip, status):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'hammer'
        self.path = []
        self.last_frame_update = 0        
        self.status = status #1: Going, 0: Returning
        self.floor = floor
        self.flip = flip
        self.image = load_sprites_from_folder("CHARACTERS/THOR/PROJECTILE")[0] 
        self.image = pygame.transform.flip(self.image, self.flip, False)     
        self.rect = self.image.get_rect()
        self.index = 0
        self.rect.center = (x, y)
        
        # if self.status == 1: 
        #     self.speed = 100
        # else:
        #     self.speed = -1
        self.speed = 100

    def update(self, scroll, fps):
        # Trajectory
        self.path.append((self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))
        if len(self.path) > 50: self.path.pop(0)
        # Movement
        self.rect.x += self.speed
        self.rect.y -= 2
        self.speed -= 10
        
        # if self.speed < 0: self.status = 0
        if self.rect.centerx < 0 or self.rect.centerx > SCREEN_WIDTH: self.kill()
        
    def draw(self, screen, grid):

        # Shadow
        shadow = pygame.mask.from_surface(pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()/3)))
        screen.blit(shadow.to_surface(unsetcolor=(0,0,0,0), setcolor=(0,0,0,150)), (self.rect.x, self.floor ))

        # Image
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        if grid:
            # Hitbox
            pygame.draw.rect(screen, COLOR_GREEN, self.rect, 1)
            # Trajectory
            for i in range(1, len(self.path)):
                pygame.draw.line(screen, COLOR_GREEN, self.path[i - 1], self.path[i])
            
            # Top left corner Position
            pygame.draw.circle(screen, COLOR_WHITE, (self.rect.x, self.rect.y), 5)
            pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect(self.rect.x-25, self.rect.y-20, 75, 12))
            screen.blit(smallfont.render(f"({self.rect.x},{self.rect.y})", True, COLOR_WHITE), (self.rect.x-25, self.rect.y-20))
            