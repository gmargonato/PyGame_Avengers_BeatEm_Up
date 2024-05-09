
import pygame
from player import *

class Captain(Player):
    def __init__(self, w, h, x, y, stance, action, hp, score):        
        super().__init__(w, h, x, y, action, hp, score)       
        self.name = "Captain America"  
        self.stance = stance
        self.animations = self.load_animations()

    def load_animations(self):
        animations_dict = {
            'INTRO'         : load_sprites_from_folder(f'CHARACTERS/CAPTAIN/STANCE{self.stance}/INTRO'),
            'IDLE'          : load_sprites_from_folder(f'CHARACTERS/CAPTAIN/STANCE{self.stance}/IDLE'),
            'WALK'          : load_sprites_from_folder(f'CHARACTERS/CAPTAIN/STANCE{self.stance}/WALK_RIGHT'),
            'HIT'           : load_sprites_from_folder(f'CHARACTERS/CAPTAIN/STANCE{self.stance}/HIT'),
            'DEFEAT'        : load_sprites_from_folder(f'CHARACTERS/CAPTAIN/STANCE1/DEFEAT'),
            'PUNCH1'        : load_sprites_from_folder(f'CHARACTERS/CAPTAIN/STANCE{self.stance}/PUNCH1'),
            'PUNCH2'        : load_sprites_from_folder(f'CHARACTERS/CAPTAIN/STANCE{self.stance}/PUNCH2'),
            'PUNCH3'        : load_sprites_from_folder(f'CHARACTERS/CAPTAIN/STANCE{self.stance}/PUNCH3'),
            'KICK1'         : load_sprites_from_folder(f'CHARACTERS/CAPTAIN/STANCE{self.stance}/KICK1'),
            'KICK2'         : load_sprites_from_folder(f'CHARACTERS/CAPTAIN/STANCE{self.stance}/KICK2'),
            'KICK3'         : load_sprites_from_folder(f'CHARACTERS/CAPTAIN/STANCE{self.stance}/KICK3'),
            'BLOCK'         : load_sprites_from_folder(f'CHARACTERS/CAPTAIN/STANCE{self.stance}/BLOCK'),
            'SPECIAL'       : load_sprites_from_folder(f'CHARACTERS/CAPTAIN/STANCE1/SPECIAL'),
            'THROW'         : load_sprites_from_folder(f'CHARACTERS/CAPTAIN/STANCE1/THROW1'),
            'RECOVER_FLOOR' : load_sprites_from_folder(f'CHARACTERS/CAPTAIN/STANCE2/SHIELD_RECOVER_FLOOR'),
            'RECOVER_AIR'   : load_sprites_from_folder(f'CHARACTERS/CAPTAIN/STANCE2/SHIELD_RECOVER_AIR'),
        }
        return animations_dict
    
    def shoot(self, num_frames):        
        if self.stance == 1 and self.current_action == 'THROW' and self.current_frame == num_frames-4:
            self.events.append( ('shield',(self.hitbox.x-20, self.hitbox.y+10)))

    def special(self, num_frames):        
        if self.stance == 1 and self.current_action == 'SPECIAL' and self.current_frame == num_frames-2:
            self.events.append( ('shockwave', (self.rect.centerx, self.rect.centery, (0,255,255)) ))

    def change_instance(self, instance, action='INTRO'):
        self.__init__(w=self.width, h=self.heigth, x=self.rect.midbottom[0], y=self.rect.midbottom[1], stance=instance, action=action, hp=self.hp, score=self.score)
        self.last_frame_update = 0

    def recover(self, type):
        self.disabled = True
        self.walking = False
        self.blocking = False
        self.attacking = -1
        self.current_frame = 0
        if type == 'air':
            action = 'RECOVER_AIR'
        else:
            action = 'RECOVER_FLOOR'
        self.change_instance(1, action)