
# Libraries
import pygame
from utils import *

class Object(pygame.sprite.Sprite):
    def __init__(self, name, scroll, x, y):
        pygame.sprite.Sprite.__init__(self)      
        self.name = name
        self.image = OBJECTS[name]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.initial_scroll = scroll

    def update(self, scroll, player):
        self.rect.x = SCREEN_WIDTH + self.initial_scroll - scroll

        if self.rect.colliderect(player.rect):
            if self.name == 'health':
                player.hp = min(player.hp + 20, 100)
                self.kill()

    def draw(self, screen, grid):
        # Shadow
        # shadow = pygame.mask.from_surface(pygame.transform.scale( pygame.transform.flip(self.image, False, True), (self.image.get_width(), self.image.get_height()/4)))        
        # screen.blit(shadow.to_surface(unsetcolor=(0,0,0,0), setcolor=(0,0,0,150)), (self.rect.x, self.rect.bottom-10))
        # Image
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # Hitbox
        if grid:
            pygame.draw.rect(screen, COLOR_GREEN, self.rect, 1)
            pygame.draw.circle(screen, COLOR_WHITE, self.rect.midbottom, 5)
            pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect(self.rect.midbottom[0]-25, self.rect.midbottom[1]-20, 60, 12))
            screen.blit(smallfont.render(str(self.rect.midbottom), True, COLOR_WHITE), (self.rect.midbottom[0]-25, self.rect.midbottom[1]-20))             
            