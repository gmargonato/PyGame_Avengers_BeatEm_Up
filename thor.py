
import pygame
from player import *

class Thor(Player):
    def __init__(self, w, h, x, y, action, hp, score):        
        super().__init__(w, h, x, y, action, hp, score)       
        self.name = "Thor"  
        self.animations = self.load_animations()

    def load_animations(self):
        animations_dict = {
            'INTRO'         : load_sprites_from_folder(f'CHARACTERS/THOR/INTRO'),
            'IDLE'          : load_sprites_from_folder(f'CHARACTERS/THOR/IDLE'),
            'WALK'          : load_sprites_from_folder(f'CHARACTERS/THOR/WALK_RIGHT'),
            'HIT'           : load_sprites_from_folder(f'CHARACTERS/THOR/HIT'),
            'DEFEAT'        : load_sprites_from_folder(f'CHARACTERS/THOR/DEFEAT'),
            'PUNCH1'        : load_sprites_from_folder(f'CHARACTERS/THOR/PUNCH1'),
            'PUNCH2'        : load_sprites_from_folder(f'CHARACTERS/THOR/PUNCH2'),
            'PUNCH3'        : load_sprites_from_folder(f'CHARACTERS/THOR/PUNCH3'),
            'KICK1'         : load_sprites_from_folder(f'CHARACTERS/THOR/KICK1'),
            'KICK2'         : load_sprites_from_folder(f'CHARACTERS/THOR/KICK2'),
            'KICK3'         : load_sprites_from_folder(f'CHARACTERS/THOR/KICK3'),
            'BLOCK'         : load_sprites_from_folder(f'CHARACTERS/THOR/BLOCK'),
            'SPECIAL'       : load_sprites_from_folder(f'CHARACTERS/THOR/SPECIAL'),
            'THROW'         : load_sprites_from_folder(f'CHARACTERS/THOR/THROW'),
        }
        return animations_dict
    
    def shoot(self, num_frames):    
        if self.current_action == 'THROW' and self.current_frame == 7:
            self.events.append( ('mjolnir', (self.rect.centerx, self.rect.centery, self.rect.bottom, self.flip) ))

    def special(self, num_frames):    
        return    
        if self.current_action == 'SPECIAL' and self.current_frame == 5:
            self.events.append( ('shockwave', (self.hitbox.centerx, self.hitbox.top, (0,255,0)) ))
