
import pygame
from utils import *

class Shockwave(pygame.sprite.Sprite):
    def __init__(self, x, y, color=(255, 255, 255)):
        super().__init__()
        self.type = 'shockwave'
        self.status = 1
        self.w = 10
        self.d = 10
        self.color = color
        self.max_size = SCREEN_WIDTH
        self.growth_rate = 50
        self.rect = pygame.Rect(x, y, self.w, self.d)
        
    def update(self, scroll, fps):
        # Increase the size of the shockwave
        self.w += self.growth_rate
        self.d += self.growth_rate

        if self.w >= self.max_size: self.kill()

        # Update the rectangle with the new size
        self.rect.inflate_ip(self.growth_rate, self.growth_rate)
        
    def draw(self, screen, grid):
        radius = min(self.rect.width, self.rect.height) // 2
        pygame.draw.circle(screen, self.color, (self.rect.centerx, self.rect.centery), radius, 2)
        pygame.draw.circle(screen, self.color, (self.rect.centerx, self.rect.centery), radius/2, 2)
        pygame.draw.circle(screen, self.color, (self.rect.centerx, self.rect.centery), radius/4, 2)
        if grid:
            pygame.draw.rect(screen, self.color, self.rect, 2)
