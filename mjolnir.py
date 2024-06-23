
import pygame
import math
import random
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
        self.speed = 40
        self.image = load_sprites_from_folder("CHARACTERS/THOR/PROJECTILE")[0] 
        self.image = pygame.transform.flip(self.image, self.flip, False)     
        self.rect = self.image.get_rect()
        self.index = 0
        self.rect.center = (x, y)        

    def generate_lightning(self, screen):
        x = random.randint(self.rect.left,self.rect.right)
        pygame.draw.line(screen, COLOR_CYAN, (x, self.rect.centery), (x, self.floor),2)

    def update(self, player, scroll, fps):
        # Trajectory
        self.path.append((self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))
        if len(self.path) > 50: self.path.pop(0)

        player_y = player.rect.centery
        dist_y = self.rect.centery - player_y

        # Going forward
        if self.status == 1:
            self.rect.x += self.speed 
            self.speed -= 1.5
            if player_y < self.rect.centery:
                self.rect.y -= 5
            else:
                self.rect.y += 5
            if self.speed < 0 and self.rect.colliderect(player.rect): 
                self.kill()
        # Retuning
        else:
            self.rect.x -= self.speed
            if self.rect.colliderect(player.rect): 
                self.kill()

    def draw(self, screen, grid):
        # Shadow
        shadow = pygame.mask.from_surface(pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()/3)))
        screen.blit(shadow.to_surface(unsetcolor=(0,0,0,0), setcolor=(0,0,0,150)), (self.rect.x, self.floor ))

        # Image
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # Lightining
        # self.generate_lightning(screen)

        if grid:
            # Hitbox
            pygame.draw.rect(screen, COLOR_GREEN, self.rect, 1)
            # Trajectory
            for i in range(1, len(self.path)):
                pygame.draw.line(screen, COLOR_GREEN, self.path[i - 1], self.path[i])
            
            # Top left corner Position
            pygame.draw.circle(screen, COLOR_WHITE, (self.rect.x, self.rect.y), 5)
            pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect(self.rect.x-25, self.rect.y-40, 75, 30))
            screen.blit(smallfont.render(f"({self.rect.x},{self.rect.y})", True, COLOR_WHITE), (self.rect.x-25, self.rect.y-40))
            screen.blit(smallfont.render(f"{self.flip} | {self.status}", True, COLOR_WHITE), (self.rect.x-25, self.rect.y-25))
            