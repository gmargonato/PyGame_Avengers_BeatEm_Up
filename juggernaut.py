
import pygame
import random
import math
from utils import *

class Juggernaut(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.events = []
        self.current_action = 'IDLE'
        self.current_frame = 0
        self.last_frame_update = 0
        self.speed = 5
        self.max_hp = 50
        self.hp = self.max_hp
        self.distance = SCREEN_WIDTH
        
        # Actions
        self.alive = True
        self.disabled = False
        self.walking = None   
        self.flip = True  
        self.blocking = 0
        self.attacking = -1 # -1: Not attacking. 0: Starting an attack. 1: Currently attacking
        self.attack_window = 0

        # Sprites
        self.animations = {
            'IDLE'      : load_sprites_from_folder(f'CHARACTERS/{self.name}/IDLE'),           
            'WALK'      : load_sprites_from_folder(f'CHARACTERS/{self.name}/WALK'),
            'HIT'       : load_sprites_from_folder(f'CHARACTERS/{self.name}/HIT'),
            'DEFEAT'    : load_sprites_from_folder(f'CHARACTERS/{self.name}/DEFEAT'),
            'BLOCK'     : load_sprites_from_folder(f'CHARACTERS/{self.name}/BLOCK'),
            'ATTACK1'   : load_sprites_from_folder(f'CHARACTERS/{self.name}/ATTACK1'),
            'ATTACK2'   : load_sprites_from_folder(f'CHARACTERS/{self.name}/ATTACK2'),
            'ATTACK3'   : load_sprites_from_folder(f'CHARACTERS/{self.name}/ATTACK3'),
            'ATTACK4'   : load_sprites_from_folder(f'CHARACTERS/{self.name}/ATTACK4'),
            'ATTACK5'   : load_sprites_from_folder(f'CHARACTERS/{self.name}/ATTACK5'),
            'SPECIAL'   : load_sprites_from_folder(f'CHARACTERS/{self.name}/SPECIAL'),
        }

        self.width      = 100 * 2
        self.heigth     = 130 * 2
        self.rect       = pygame.Rect(0, 0, self.width, self.heigth) 
        self.rect.midbottom = (x,y)
        self.hitbox = pygame.Rect(0, 0, 50, 50)
        
    def update(self, fps, player, projectile_group):
        if self.alive:
            self.ai_input(player)
            self.combat(player, projectile_group)
        self.animate(fps)

    def ai_input(self, player):
        if self.disabled: return

        # Walk
        self.distance = abs(player.rect.centerx - self.rect.centerx)
        if self.distance > 300:
            self.walking = True
            self.rect.x -= self.speed            
        elif self.distance < 295:
            self.walking = True
            self.rect.x += self.speed    
            self.attack_window = 0    
        else: 
            self.walking = None

        # If not walking, do something else
        if self.walking == None and self.attack_window <= 0:
            self.attacking = 0 # Can start an attack
            
    def combat(self, player, projectile_group):
        if self.attack_window > 0: self.attack_window -= 10
        if self.blocking > 0: self.blocking -= 10
        if self.current_action == 'BLOCK' and self.blocking <= 0: self.disabled = False
        
        # Check if still Alive
        if self.hp <= 0:
            self.alive = False
            self.disabled = True
            self.current_action = 'DEFEAT'
            self.speed = 255

        # Starting an attack
        if self.attacking == 0:
            self.attacking = 1
            self.current_frame = 0            
            self.disabled = True          
            self.attack_window = 300
            # if self.rect.x >= 800:
            #     self.current_action = 'SPECIAL'
            # else:
            #     self.current_action = random.choice(['ATTACK1','ATTACK2','ATTACK3','ATTACK4','ATTACK5',])
            self.current_action = random.choice(['ATTACK1','ATTACK2','ATTACK3','ATTACK4','ATTACK5',])

        # Hit by player
        if player.attacking == 1:
            if self.current_action in ['IDLE','WALK']:
                block_chance = random.randint(0,5)
                # Chance to block
                if block_chance == 0:
                    self.current_action = 'BLOCK'
                    self.disabled = True
                    self.blocking = 100
            # If not blocking, check collision
            if self.disabled == False:
                collide = pygame.Rect.colliderect(self.rect, player.hitbox)
                if collide: 
                    self.current_frame = 0
                    self.current_action = 'HIT'
                    self.disabled = True
                    self.hp -= 1
        # Boss is immune to projectiles
        for p in projectile_group:   
            collide = pygame.Rect.colliderect(self.rect, p.rect)
            if collide:
                if p.type == 'shield': p.status = -1

    def animate(self, fps):
        num_frames = len(self.animations[self.current_action])
        last_frame = num_frames - 1

        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_update < fps * 2:
            return
        else: 
            self.last_frame_update = current_time

        # Animation Loop
        if num_frames == 1:
            self.current_frame = 0
        else:
            if self.current_frame < last_frame: # Keep looping while state is true
                self.current_frame += 1     
                if self.current_action == 'SPECIAL': self.rect.x -= 50
            else: # If it is the last frame of animation              
                    self.current_frame = 0
                    self.disabled = False
                
        next_action = self.current_action

        if self.disabled:
            pass
        elif self.walking:
            next_action = 'WALK'    
        else:
            next_action = 'IDLE'            
        
        # Ensures the next action starts from frame 0
        if next_action != self.current_action:
            self.current_frame = 0
            self.current_action = next_action

        # Update Image
        self.image = pygame.transform.flip(self.animations[self.current_action][self.current_frame], self.flip, False)        
        # Update Hitbox
        self.hitbox.x = self.rect.x - (self.image.get_width()/1.9)
        self.hitbox.y = self.rect.y + self.heigth/4
        # Vanish effect after defeat
        if not self.alive:        
            self.speed -= 10
            self.image.set_alpha(self.speed)
            if self.speed <= 0: self.kill()

    def draw(self, screen, grid):

        # Shadow
        # pygame.draw.ellipse(screen, COLOR_BLACK, (self.rect.x-25, self.rect.midbottom[1]-20, self.width+50, 10))
        # shadow_aux = pygame.transform.flip(self.image, False, True)      
        shadow = pygame.mask.from_surface(pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()/3)))
        
        # Enemy Image
        if self.alive: screen.blit(shadow.to_surface(unsetcolor=(0,0,0,0), setcolor=(0,0,0,150)), (self.rect.x + self.rect.width - self.image.get_width() + 30, self.rect.y + self.rect.height - 105))
        screen.blit(self.image, (self.rect.x + self.rect.width - self.image.get_width() + 30, self.rect.y + self.rect.height - self.image.get_height()))
        
        # Boss portrait shows all the time and sits at the bottom of the screen
        if self.alive:
            # Health Bar
            ratio = self.hp / self.max_hp
            pygame.draw.rect(screen, COLOR_RED,     (SCREEN_WIDTH/4,SCREEN_HEIGHT-50,600,22))
            pygame.draw.rect(screen, COLOR_YELLOW,  (SCREEN_WIDTH/4,SCREEN_HEIGHT-50,600 * ratio,22))
            pygame.draw.rect(screen, COLOR_WHITE,   pygame.Rect(SCREEN_WIDTH/4, SCREEN_HEIGHT-50, 600, 22), 2)
            # Name & Score
            screen.blit(arcadefont.render(self.name, True, COLOR_BLACK), (SCREEN_WIDTH/2-40,SCREEN_HEIGHT-47))        
        if grid:
            # Hitbox
            pygame.draw.rect(screen, COLOR_RED, self.rect, 1)
            pygame.draw.rect(screen, COLOR_RED, self.hitbox, 1)

            # Debug            
            pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect(self.rect.x, self.rect.y-150, self.width, 60))
            screen.blit(smallfont.render(f"Action: {self.current_action} {self.current_frame}", True, COLOR_WHITE), (self.rect.x, self.rect.y-150))
            screen.blit(smallfont.render(f"Blocking: {self.blocking}", True, COLOR_WHITE), (self.rect.x, self.rect.y-140))
            screen.blit(smallfont.render(f"Disabled: {self.disabled} | Walking: {self.walking}", True, COLOR_WHITE), (self.rect.x, self.rect.y-130))
            screen.blit(smallfont.render(f"Life: {self.hp}/{self.max_hp}", True, COLOR_WHITE), (self.rect.x, self.rect.y-120))
            screen.blit(smallfont.render(f"Attacking: {self.attacking} | Window: {self.attack_window}", True, COLOR_WHITE), (self.rect.x, self.rect.y-110))
            
            # Midbottom Position
            pygame.draw.circle(screen, COLOR_WHITE, self.rect.midbottom, 5)
            pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect(self.rect.midbottom[0]-25, self.rect.midbottom[1]-20, 50, 12))
            screen.blit(smallfont.render(str(self.rect.midbottom), True, COLOR_WHITE), (self.rect.midbottom[0]-25, self.rect.midbottom[1]-20))
