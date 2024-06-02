
import pygame
from player import *

SCALE = 1.8

class Thor(Player):
    def __init__(self, w, h, x, y, action, hp, score):        
        super().__init__(w, h, x, y, action, hp, score)       
        self.name = "Donald Blake"  
        self.animations = self.load_animations()

    def load_animations(self):
        animations_dict = {
            'INTRO'         : load_sprites_from_folder(f'CHARACTERS/THOR/INTRO',SCALE),
            'IDLE'          : load_sprites_from_folder(f'CHARACTERS/THOR/IDLE',SCALE),
            'WALK'          : load_sprites_from_folder(f'CHARACTERS/THOR/WALK_RIGHT',SCALE),
            'HIT'           : load_sprites_from_folder(f'CHARACTERS/THOR/HIT',SCALE),
            'DEFEAT'        : load_sprites_from_folder(f'CHARACTERS/THOR/DEFEAT',SCALE),
            'PUNCH1'        : load_sprites_from_folder(f'CHARACTERS/THOR/PUNCH1',SCALE),
            'PUNCH2'        : load_sprites_from_folder(f'CHARACTERS/THOR/PUNCH2',SCALE),
            'PUNCH3'        : load_sprites_from_folder(f'CHARACTERS/THOR/PUNCH3',SCALE),
            'KICK1'         : load_sprites_from_folder(f'CHARACTERS/THOR/KICK1',SCALE),
            'KICK2'         : load_sprites_from_folder(f'CHARACTERS/THOR/KICK2',SCALE),
            'KICK3'         : load_sprites_from_folder(f'CHARACTERS/THOR/KICK3',SCALE),
            'BLOCK'         : load_sprites_from_folder(f'CHARACTERS/THOR/BLOCK',SCALE),
            'SPECIAL'       : load_sprites_from_folder(f'CHARACTERS/THOR/SPECIAL',SCALE),
            'THROW'         : load_sprites_from_folder(f'CHARACTERS/THOR/THROW',SCALE),
        }
        return animations_dict
    
    def shoot(self, num_frames):    
        if self.current_action == 'THROW' and self.current_frame == 7:
            self.events.append( ('mjolnir', (self.rect.centerx, self.rect.centery, self.rect.bottom, self.flip) ))

    def special(self, num_frames):    
        return    
        if self.current_action == 'SPECIAL' and self.current_frame == 5:
            self.events.append( ('shockwave', (self.hitbox.centerx, self.hitbox.top, (0,255,0)) ))
