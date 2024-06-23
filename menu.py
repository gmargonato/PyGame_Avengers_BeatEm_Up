
import pygame, time

from utils import *
from captain import *
from hulk import *
from spider import *
from thor import *
from mjolnir import *

class Menu():
    def __init__(self, fps, display):
        self.fps = fps
        self.display = display
        self.projectile_group = pygame.sprite.Group()
        
        # Character Selection - Available Heroes        
        self.menu_cap    = Captain(w=160, h=220, x=200, y=470, stance=1, action='INTRO', hp=100, score=0)
        self.menu_hulk   = Hulk(w=160, h=230, x=600, y=470, action='INTRO', hp=100, score=0)
        # self.menu_thor   = Thor(w=160, h=230, x=1600, y=470, action='INTRO', hp=100, score=0)
        self.menu_spider = Spider(w=160, h=230, x=1000, y=470, action='INTRO', hp=100, score=0)
        self.available_heroes = pygame.sprite.Group()
        self.available_heroes.add(self.menu_cap, self.menu_hulk, self.menu_spider)
        self.selected = False
        self.player = None

    def run(self):
        # Handle Events
        if not self.selected:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_1] or keys[pygame.K_2] or keys[pygame.K_3]:# or keys[pygame.K_4]:
                self.selected = True        
                if keys[pygame.K_1]:        
                    self.menu_cap.last_frame_update = 0                
                elif keys[pygame.K_2]:                            
                    self.menu_hulk.last_frame_update = 0                      
                elif keys[pygame.K_3]:
                    self.menu_spider.last_frame_update = 0
                # elif keys[pygame.K_4]:
                #     self.menu_thor.last_frame_update = 0
                #     hammer = Mjolnir(x=SCREEN_WIDTH, y=self.menu_thor.rect.centery-60, floor=self.menu_thor.rect.bottom-20, flip=False, status=0)
                #     self.projectile_group.add(hammer)

        # Display Heroes
        self.display.fill(COLOR_BLACK)
        self.display.blit(ASSETS['character_selection'], (0,0))  

        # Display Projectiles
        for projectile in self.projectile_group:
            projectile.update(self.menu_thor, 0, self.fps)
            projectile.draw(self.display, False)

        for p in self.available_heroes:
            p.update(self.fps, False, pygame.sprite.Group())
            p.draw(self.display, False)
            
            # Once the selected hero finishes the intro animation 
            if not p.disabled:
                if p.name == "Captain America":
                    self.player = Captain(w=160, h=220, x=SCREEN_WIDTH/2, y=550, stance=1, action='IDLE', hp=100, score=0)      
                elif p.name == "Hulk": 
                    self.player = Hulk(w=160, h=230, x=SCREEN_WIDTH/2, y=550, action='IDLE', hp=100, score=0)
                elif p.name == "Spider-Man":
                    self.player = Spider(w=160, h=230, x=SCREEN_WIDTH/2, y=550, action='IDLE', hp=100, score=0)
                    
        