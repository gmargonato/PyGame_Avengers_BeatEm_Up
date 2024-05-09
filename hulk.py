
import pygame
from player import *

class Hulk(Player):
    def __init__(self, w, h, x, y, action, hp, score):        
        super().__init__(w, h, x, y, action, hp, score)       
        self.name = "Hulk"  
        self.animations = self.load_animations()

    def load_animations(self):
        animations_dict = {
            'INTRO'         : load_sprites_from_folder(f'CHARACTERS/HULK/INTRO'),
            'IDLE'          : load_sprites_from_folder(f'CHARACTERS/HULK/IDLE'),
            'WALK'          : load_sprites_from_folder(f'CHARACTERS/HULK/WALK_RIGHT'),
            'HIT'           : load_sprites_from_folder(f'CHARACTERS/HULK/HIT'),
            'DEFEAT'        : load_sprites_from_folder(f'CHARACTERS/HULK/DEFEAT'),
            'PUNCH1'        : load_sprites_from_folder(f'CHARACTERS/HULK/PUNCH1'),
            'PUNCH2'        : load_sprites_from_folder(f'CHARACTERS/HULK/PUNCH2'),
            'PUNCH3'        : load_sprites_from_folder(f'CHARACTERS/HULK/PUNCH3'),
            'KICK1'         : load_sprites_from_folder(f'CHARACTERS/HULK/KICK1'),
            'KICK2'         : load_sprites_from_folder(f'CHARACTERS/HULK/KICK2'),
            'KICK3'         : load_sprites_from_folder(f'CHARACTERS/HULK/KICK3'),
            'BLOCK'         : load_sprites_from_folder(f'CHARACTERS/HULK/BLOCK'),
            'SPECIAL'       : load_sprites_from_folder(f'CHARACTERS/HULK/SPECIAL'),
            'THROW'         : load_sprites_from_folder(f'CHARACTERS/HULK/THROW'),
        }
        return animations_dict
    
    def shoot(self, num_frames):        
        if self.current_action == 'THROW' and self.current_frame == 17:
            self.events.append( ('rock', (self.rect.centerx, self.rect.top, self.rect.bottom, self.flip) ))

    def special(self, num_frames):        
        if self.current_action == 'SPECIAL' and self.current_frame == 5:
            self.events.append( ('shockwave', (self.hitbox.centerx, self.hitbox.top, (0,255,0)) ))
