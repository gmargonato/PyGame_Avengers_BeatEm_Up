
import pygame
from utils import *
from animation import *

class Cutscene():
    def __init__(self, fps, display):
        self.fps = fps
        self.display = display
        self.pos_y = 0
        self.animation_group = pygame.sprite.Group()

    def run(self):     
        # Events
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if (self.pos_y >= -500 or self.pos_y <= -1000) and len(self.animation_group) == 0:
                self.animation_group.add(Animation(name='fade_out', transparency=False, flip=False, x=0, y=0))

        self.display.blit(ASSETS['intro_image'], (0,self.pos_y))
        self.display.blit(ASSETS['intro_text_1'], (50,50))
        if self.pos_y > -1000: 
            self.pos_y -= 15
        else:
            self.display.blit(ASSETS['intro_text_2'], (0,0))
             
        # self.display.blit(font.render(f"[DEBUG] {self.pos_y}", True, COLOR_BLACK), (100, SCREEN_HEIGHT-100))
        for animation in self.animation_group:
            finished = animation.update(self.fps, self.display)                    
            if finished: 
                self.pos_y = -1
                animation.kill()
        # self.screen.blit(pygame.transform.scale(self.display,(SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))        
