
import pygame
import math
from utils import *

class Shield(pygame.sprite.Sprite):
    def __init__(self, x, y, initial_scroll, dir, floor, status):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'shield'
        self.path = []
        self.initial_dir = dir
        self.initial_scroll = initial_scroll
        self.speed_x = 40
        self.speed_y = 20
        sprites = load_sprites_from_folder("CHARACTERS/CAPTAIN/STANCE1/PROJECTILE")
        self.sprite_forward = sprites[0]
        self.rect = self.sprite_forward.get_rect()
        self.sprite_backward = sprites[1:14]
        self.sprite_floor = sprites[15:]
        self.index = 0
        self.rect.center = (x,y)
        self.floor = floor
        self.status = status #1: Going, 0: Retuning, -1: Floor
        self.last_frame_update = 0

    def update(self, FPS, scroll):
        self.path.append((self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))
        if len(self.path) > 50: self.path.pop(0)
        if scroll != self.initial_scroll: self.path = []

        # Going
        if self.status == 1:
            self.image = self.sprite_forward
            # Update position
            if self.initial_dir == False:
                self.rect.x += self.speed_x * (-1 if self.initial_dir else 1)
            else:
                self.rect.x -= self.speed_x
            if self.rect.x >= SCREEN_WIDTH or self.rect.x <= 0:
                self.status = 0
        
        # Returning
        elif self.status == 0:
            # Update animation
            last_frame = len(self.sprite_backward) - 1
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_update > FPS*1.25:
                self.index += 1
                if self.index == last_frame:
                    self.index = 0
                self.image = self.sprite_backward[self.index]       
            # Update position (parabolic trajectory)
            self.speed_x = max(0, self.speed_x - 1.5)
            if self.initial_dir == False:
                self.rect.x -= self.speed_x
            else:
                self.rect.x += self.speed_x
            self.rect.y -= self.speed_y
            self.speed_y -= 1.5
            if self.rect.y >= self.floor:
                self.status = -1
                self.index = 0
                
        # Lying on the floor
        else: 
            # Update animation
            last_frame = len(self.sprite_floor) - 1
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_update > FPS*1.5:
                self.index += 1
                if self.index == last_frame:
                    self.index = 0
                self.image = self.sprite_floor[self.index]  
            # Stay on the floor                   
            self.rect.y = min(self.floor, 670)         

    def draw(self, screen, grid):

        # Shadow
        shadow = pygame.mask.from_surface(pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()/3)))
        if self.status != -1: screen.blit(shadow.to_surface(unsetcolor=(0,0,0,0), setcolor=(0,0,0,150)), (self.rect.x, self.floor))

        # Image
        screen.blit(pygame.transform.flip(self.image, False, False), (self.rect.x, self.rect.y))
        
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
            