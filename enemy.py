
import pygame
import random
import math
from utils import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.events = []
        self.current_action = 'IDLE'
        self.current_frame = 0
        self.last_frame_update = 0
        self.last_hit_time = 0
        self.speed = 5
        self.max_hp = 3
        self.hp = self.max_hp
        self.distance_x = SCREEN_WIDTH
        self.distance_y = SCREEN_HEIGHT
        self.flip = False
        self.safe_distance = random.randint(195,210)
        
        # Actions
        self.alive = True
        self.disabled = False
        self.walking = False     
        self.blocking = 0
        self.attacking = -1 # -1: Not attacking. 0: Starting an attack. 1: Currently attacking
        self.attack_window = 0

        # Sprites
        self.animations = {
            'IDLE'      : load_sprites_from_folder(f'CHARACTERS/{self.name}/IDLE'),
            'WALK'      : load_sprites_from_folder(f'CHARACTERS/{self.name}/WALK'),
            'HIT'       : load_sprites_from_folder(f'CHARACTERS/{self.name}/HIT'),
            'KNOCKBACK' : load_sprites_from_folder(f'CHARACTERS/{self.name}/KNOCKBACK'),
            'GETUP'     : load_sprites_from_folder(f'CHARACTERS/{self.name}/GETUP'),
            'BLOCK'     : load_sprites_from_folder(f'CHARACTERS/{self.name}/BLOCK'),
            'ATTACK1'   : load_sprites_from_folder(f'CHARACTERS/{self.name}/ATTACK1'),
            'ATTACK2'   : load_sprites_from_folder(f'CHARACTERS/{self.name}/ATTACK2'),
            'ATTACK3'   : load_sprites_from_folder(f'CHARACTERS/{self.name}/ATTACK3'),
            'ATTACK4'   : load_sprites_from_folder(f'CHARACTERS/{self.name}/ATTACK4'),
        }

        self.width      = 55 * 2
        self.heigth     = 90 * 2
        self.rect       = pygame.Rect(0, 0, self.width, self.heigth) 
        self.rect.midbottom = (x,y)
        self.hitbox = pygame.Rect(0, 0, 50, 50)
        
    def update(self, fps, player, projectiles):
        if self.alive:
            self.ai_input(player)
            self.combat(fps, player, projectiles)
        self.animate(fps)

    def ai_input(self, player):
        if self.disabled: return
        self.distance_x = player.rect.midbottom[0] - self.rect.midbottom[0]
        self.distance_y = player.rect.midbottom[1] - self.rect.midbottom[1]
        if self.distance_x < 0: self.flip = True
        # Check horizontal distance
        if abs(self.distance_x) > self.safe_distance:
            self.walking = True
             # Move right
            if self.distance_x > 0:
                self.rect.x += self.speed
                self.flip = False                
            # Move left
            else: 
                self.rect.x -= self.speed
                self.flip = True        
        # Check vertical distance
         # Move up
        elif self.distance_y > 1:
            self.walking = True
            self.rect.y += self.speed/2
         # Move down
        elif self.distance_y < 0:
            self.walking = True
            self.rect.y -= self.speed/2
        else:
            self.walking = False
        
        # If not walking, do something else
        if self.walking == False and player.hp > 0:
            if self.attack_window <= 0:
                attack_chance = random.randint(0,10)
                if attack_chance == 0: self.attacking = 0 # Can start an attack
            
    def combat(self, FPS, player, projectile_group):
        if self.attack_window > 0: self.attack_window -= 10
        if self.blocking > 0: self.blocking -= 10
        if self.current_action == 'BLOCK' and self.blocking <= 0: self.disabled = False
        
        # Check if still Alive
        if self.hp <= 0:
            self.alive = False
            self.disabled = True
            self.current_action = 'KNOCKBACK'
            self.current_frame = 0
            self.speed = 255

        # Starting an attack
        if self.attacking == 0:
            self.attacking = 1
            self.current_frame = 0
            self.current_action = random.choice(['ATTACK1','ATTACK2','ATTACK3','ATTACK4'])
            self.disabled = True          
            self.attack_window = 300

        # Getting hit        
        # By player
        if player.attacking == 1:
            if self.current_action in ['IDLE','WALK']:
                block_chance = random.randint(0,15)
                # Chance to block
                if block_chance == 0 and abs(self.distance_x) <= self.safe_distance:
                    self.current_action = 'BLOCK'
                    self.disabled = True
                    self.blocking = 150
            # If not blocking, check collision
            if self.disabled == False:
                if (
                    pygame.Rect.colliderect(self.rect, player.hitbox) 
                    and abs(self.distance_y) <= 50
                    and pygame.time.get_ticks() - self.last_hit_time > 500
                ):
                    self.last_hit_time = pygame.time.get_ticks()
                    self.current_frame = 0
                    self.current_action = 'HIT'
                    self.events.append( ('hit', (player.hitbox.x, player.hitbox.y)) )      
                    self.disabled = True
                    self.hp -= 1
                    player.score += 50        
                    if player.attack_type == 'KICK': self.rect.x += 25 * (-1 if self.distance_x > 0 else 1)               
        # By projectiles        
        for p in projectile_group:
            if pygame.Rect.colliderect(self.rect, p.rect) and p.status == 1 and pygame.time.get_ticks() - self.last_hit_time > 500:
                self.last_hit_time = pygame.time.get_ticks()
                self.walking = False
                self.current_frame = 0
                self.current_action = 'KNOCKBACK'
                self.disabled = True
                self.hp -= 1
                player.score += 25

    def animate(self, FPS):
        num_frames = len(self.animations[self.current_action])
        last_frame = num_frames - 1
        if pygame.time.get_ticks() - self.last_frame_update > FPS * 2:
            self.last_frame_update = pygame.time.get_ticks()
        else:
            return

        # Animation Loop
        if num_frames == 1:
            self.current_frame = 0
        else:
            if self.current_frame < last_frame: # Keep looping while state is true
                self.current_frame += 1  
            else: # If it is the last frame of animation  
                if self.current_action == 'KNOCKBACK':
                    # if not self.alive: self.kill()
                    # else:                        
                    if self.alive:
                        self.current_frame = 0                    
                        self.current_action = 'GETUP'
                else: # If it is the last frame of animation
                    self.current_frame = 0
                    self.disabled = False
                    if self.attacking == 1:
                        self.attacking = -1
                    
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
        self.hitbox.y = self.rect.y + self.heigth/4
        img_width = self.image.get_width()
        if not self.flip: 
            self.hitbox.x = self.rect.x + (img_width/1.2)
        else: 
            self.hitbox.x = self.rect.x - (img_width/2.2)

        if not self.alive:        
            self.speed -= 10
            self.image.set_alpha(self.speed)
            if self.speed <= 0: self.kill()

    def draw(self, screen, grid):

        # Shadow
        shadow = pygame.mask.from_surface(pygame.transform.scale( pygame.transform.flip(self.image, False, True), (self.image.get_width(), self.image.get_height()/4)))        
        screen.blit(shadow.to_surface(unsetcolor=(0,0,0,0), setcolor=(0,0,0,150)), (
            self.rect.x + (self.rect.width - self.image.get_width() if self.flip else 0), 
            self.rect.bottom-15
        ))        
        
        # Image
        screen.blit(self.image, (
            # self.rect.x + self.rect.width - self.image.get_width() + 30, 
            self.rect.x + (self.rect.width - self.image.get_width() if self.flip else 0), 
            self.rect.y + self.rect.height - self.image.get_height()
        ))
        
        # Portrait shows when hit
        if pygame.time.get_ticks() - self.last_hit_time < 1000 and 0 <= self.rect.centerx <= SCREEN_WIDTH:
            # Image
            screen.blit(ASSETS[f'{self.name}_portrait'],   (SCREEN_WIDTH-80, 20))
            # Health Bar
            ratio = self.hp / self.max_hp
            pygame.draw.rect(screen, COLOR_RED,     (SCREEN_WIDTH-280,62,200,22))
            pygame.draw.rect(screen, COLOR_YELLOW,  (SCREEN_WIDTH-280,62,200 * ratio,22))
            pygame.draw.rect(screen, COLOR_WHITE,   pygame.Rect(SCREEN_WIDTH-280, 62, 200, 22), 2)
            # Name & Score
            screen.blit(arcadefont.render(self.name, True, COLOR_BLACK), (SCREEN_WIDTH-280,42))
            screen.blit(arcadefont.render(self.name, True, COLOR_WHITE), (SCREEN_WIDTH-280,40))
            
        if grid:
            # Hitbox
            pygame.draw.rect(screen, COLOR_RED, self.rect, 1)
            pygame.draw.rect(screen, COLOR_RED, self.hitbox, 1)

            # Debug            
            pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect(self.rect.x, self.rect.y-150, self.width+30, 100))
            screen.blit(smallfont.render(f"Action: {self.current_action}", True, COLOR_WHITE), (self.rect.x, self.rect.y-150))
            screen.blit(smallfont.render(f"Frame: {self.current_frame}", True, COLOR_WHITE), (self.rect.x, self.rect.y-135))
            screen.blit(smallfont.render(f"Alive: {self.alive} | Life: {self.hp}/{self.max_hp}", True, COLOR_WHITE), (self.rect.x, self.rect.y-120))
            screen.blit(smallfont.render(f"Blocking: {self.blocking} | Disabled: {self.disabled}", True, COLOR_WHITE), (self.rect.x, self.rect.y-105))
            screen.blit(smallfont.render(f"Attacking: {self.attacking} | Window: {self.attack_window}", True, COLOR_WHITE), (self.rect.x, self.rect.y-90))
            screen.blit(smallfont.render(f"Distance: {self.distance_x},{self.distance_y}", True, COLOR_WHITE), (self.rect.x, self.rect.y-75))
            
            # Midbottom Position
            pygame.draw.circle(screen, COLOR_WHITE, self.rect.midbottom, 5)
            pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect(self.rect.midbottom[0]-25, self.rect.midbottom[1]-20, 50, 12))
            screen.blit(smallfont.render(str(self.rect.midbottom), True, COLOR_WHITE), (self.rect.midbottom[0]-25, self.rect.midbottom[1]-20))

            # Distance to player
            # midpoint = (player.rect.centerx + self.rect.centerx)  // 2
            # pygame.draw.line(screen, COLOR_WHITE, (self.rect.midbottom[0], self.rect.midbottom[1]), (player.rect.midbottom[0], player.rect.midbottom[1]))   
            # pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect( midpoint-25 , self.rect.midbottom[1], 50, 15))
            # screen.blit(smallfont.render(str(self.distance), True, COLOR_WHITE), (midpoint-10, self.rect.midbottom[1]))