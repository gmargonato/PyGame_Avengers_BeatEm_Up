
# Libraries
import pygame
from utils import *

ANIMATION_LIST = {
    'lightning' : load_sprites_from_folder(f'ASSETS/LIGHTNING', scale=2, transparency=False),  
    'fade_in'   : 80,
    'fade_out'  : 600,
    'defeat'    : 600,
}
        
class Animation(pygame.sprite.Sprite):
    def __init__(self, name, transparency, flip, x, y):
        pygame.sprite.Sprite.__init__(self)      
        self.name = name
        self.transparency = transparency
        self.flip = flip
        self.x = x
        self.y = y
        self.current_frame = 0        
        self.frames = ANIMATION_LIST[name]
        self.last_frame_update = 0

    def update(self, FPS, screen):     
        finished = False   
        current_time = pygame.time.get_ticks()
        # General purpose animations
        if self.name in ['lightning','hit']:
            last_frame = len(self.frames) - 1
            MULT_FPS = 2
            if current_time - self.last_frame_update < FPS*MULT_FPS:
                return
            else: 
                self.last_frame_update = current_time
                self.current_frame += 1
                image = self.frames[self.current_frame]               
                screen.blit(pygame.transform.flip(image, self.flip, False), (self.x, self.y)) #, special_flags = pygame.BLEND_SUB or BLEND_ADD
            if self.current_frame == last_frame: finished = True
        # Transition effects
        elif self.name == 'fade_in':            
            self.frames -= 1
            if self.frames <= 0: finished = True
            transition_surf = pygame.Surface(screen.get_size())
            pygame.draw.circle(transition_surf, (255,255,255), (screen.get_width() // 2, screen.get_height() // 2), (80 - abs(self.frames)) * 16)
            transition_surf.set_colorkey((255,255,255))
            screen.blit(transition_surf, (0,0))
            # screen.blit(font.render(str(self.frames), True, COLOR_WHITE), (SCREEN_WIDTH-100, SCREEN_HEIGHT-100))
        elif self.name == 'fade_out':            
            if self.frames > 0: self.frames -= 20
            if self.frames == 0: finished = True
            transition_surf = pygame.Surface(screen.get_size())
            pygame.draw.circle(transition_surf, (255,255,255), (screen.get_width() // 2, screen.get_height() // 2), self.frames)
            transition_surf.set_colorkey((255,255,255))
            screen.blit(transition_surf, (0,0))
            # screen.blit(font.render(str(self.frames), True, COLOR_WHITE), (SCREEN_WIDTH-100, SCREEN_HEIGHT-100))
        elif self.name == 'defeat':            
            if self.frames > 0: self.frames -= 40
            if self.frames == 0: finished = True
            transition_surf = pygame.Surface(screen.get_size())
        return finished        