
import pygame
import math
from utils import *

class Web(pygame.sprite.Sprite):
    def __init__(self, x, y, floor, flip):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'web'
        self.path = []
        self.flip = flip
        self.speed = 30
        sprites = load_sprites_from_folder("CHARACTERS/SPIDER/PROJECTILE", 1.5)
        self.sprite_forward = sprites[0]
        self.rect = self.sprite_forward.get_rect()
        self.sprite_webbed = sprites[1]
        self.sprite_dissolve = sprites[2:]
        self.index = 0
        self.rect.center = (x,y)
        self.status = 1 #1: Going, 0: webbed, -1: dissolving
        self.last_frame_update = 0
        self.floor = floor

    def update(self, player, FPS, scroll):
        self.path.append((self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))
        if len(self.path) > 50: self.path.pop(0)

        # Hits the edge of screen
        if self.rect.centerx < 0 or self.rect.centerx > SCREEN_WIDTH: self.kill()

        # Going        
        if self.status == 1:
            self.rect.x += self.speed * (-1 if self.flip else 1)
            self.image = self.sprite_forward
        elif self.status == 0:
            self.image = self.sprite_webbed
        else:
            # Update animation
            last_frame = len(self.sprite_dissolve) - 1
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_update > FPS*2:
                self.index += 1
                if self.index == last_frame:
                    self.kill()
                self.image = self.sprite_dissolve[self.index]       

    def draw(self, screen, grid):

        # Shadow
        shadow = pygame.mask.from_surface(pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()/3)))
        if self.status == 1: screen.blit(shadow.to_surface(unsetcolor=(0,0,0,0), setcolor=(0,0,0,150)), (self.rect.x, self.floor))

        # Image
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x, self.rect.y - (50 if self.status < 1 else 0)))
        
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
            