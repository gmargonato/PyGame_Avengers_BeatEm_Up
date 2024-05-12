
import pygame
from player import *

class Spider(Player):
    def __init__(self, w, h, x, y, action, hp, score):        
        super().__init__(w, h, x, y, action, hp, score)       
        self.name = "Spider-Man"  
        self.animations = self.load_animations()

    def load_animations(self):
        animations_dict = {
            'INTRO'         : load_sprites_from_folder(f'CHARACTERS/SPIDER/INTRO'),
            'IDLE'          : load_sprites_from_folder(f'CHARACTERS/SPIDER/IDLE'),
            'WALK'          : load_sprites_from_folder(f'CHARACTERS/SPIDER/WALK_RIGHT'),
            'HIT'           : load_sprites_from_folder(f'CHARACTERS/SPIDER/HIT'),
            'DEFEAT'        : load_sprites_from_folder(f'CHARACTERS/SPIDER/DEFEAT'),
            'PUNCH1'        : load_sprites_from_folder(f'CHARACTERS/SPIDER/PUNCH1'),
            'PUNCH2'        : load_sprites_from_folder(f'CHARACTERS/SPIDER/PUNCH2'),
            'PUNCH3'        : load_sprites_from_folder(f'CHARACTERS/SPIDER/PUNCH3'),
            'KICK1'         : load_sprites_from_folder(f'CHARACTERS/SPIDER/KICK1'),
            'KICK2'         : load_sprites_from_folder(f'CHARACTERS/SPIDER/KICK2'),
            'KICK3'         : load_sprites_from_folder(f'CHARACTERS/SPIDER/KICK3'),
            'BLOCK'         : load_sprites_from_folder(f'CHARACTERS/SPIDER/BLOCK'),
            'SPECIAL'       : load_sprites_from_folder(f'CHARACTERS/SPIDER/SPECIAL'),
            'THROW'         : load_sprites_from_folder(f'CHARACTERS/SPIDER/THROW'),
        }
        return animations_dict
    
    def shoot(self, num_frames):        
        if self.current_action == 'THROW' and self.current_frame == 3 and self.cooldown <= 0:
            self.cooldown = 100
            self.events.append( ('web', (self.hitbox.left, self.hitbox.bottom, self.rect.bottom, self.flip) ))

    def special(self, num_frames):        
        if self.current_action == 'SPECIAL' and self.current_frame == 1:
            self.events.append( ('shockwave', (self.hitbox.centerx, self.hitbox.top, (255,255,255)) ))
