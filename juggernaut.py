
import pygame
import random
import math
from utils import *

class Juggernaut(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.boss = True
        self.events = []
        self.current_action = 'INTRO'
        self.current_frame = 0
        self.last_frame_update = 0
        self.last_hit_time = 0
        self.speed = 5
        self.max_hp = 50
        self.hp = self.max_hp
        self.distance_x = SCREEN_WIDTH
        self.distance_y = SCREEN_HEIGHT
        self.flip = True
        self.safe_distance = 300
        
        # Actions
        self.alive = True
        self.disabled = True
        self.walking = False     
        self.blocking = 0
        self.attacking = -1 # -1: Not attacking. 0: Starting an attack. 1: Currently attacking
        self.attack_type = 0
        self.attack_window = 0

        # Sprites
        self.animations = {
            'INTRO'     : load_sprites_from_folder(f'CHARACTERS/JUGGERNAUT/INTRO'),
            'IDLE'      : load_sprites_from_folder(f'CHARACTERS/JUGGERNAUT/IDLE'),
            'WALK'      : load_sprites_from_folder(f'CHARACTERS/JUGGERNAUT/WALK_FORWARD'),
            'WALK_BACK' : load_sprites_from_folder(f'CHARACTERS/JUGGERNAUT/WALK_BACK'),
            'HIT'       : load_sprites_from_folder(f'CHARACTERS/JUGGERNAUT/HIT'),
            'DEFEAT'    : load_sprites_from_folder(f'CHARACTERS/JUGGERNAUT/DEFEAT'),
            'BLOCK'     : load_sprites_from_folder(f'CHARACTERS/JUGGERNAUT/BLOCK'),
            'ATTACK1'   : load_sprites_from_folder(f'CHARACTERS/JUGGERNAUT/ATTACK1'),
            'ATTACK2'   : load_sprites_from_folder(f'CHARACTERS/JUGGERNAUT/ATTACK2'),
            'ATTACK3'   : load_sprites_from_folder(f'CHARACTERS/JUGGERNAUT/ATTACK3'),
            'SPECIAL'   : load_sprites_from_folder(f'CHARACTERS/JUGGERNAUT/SPECIAL'),
        }

        self.width      = 200
        self.heigth     = 270
        self.rect       = pygame.Rect(0, 0, self.width, self.heigth) 
        self.rect.midbottom = (x,y)
        self.hitbox = pygame.Rect(0, 0, 150, 50)
        
    def update(self, fps, player, projectiles):
        if self.alive:
            self.ai_input(player)
            self.combat(fps, player, projectiles)
        self.animate(fps)

    def ai_input(self, player):
        if self.disabled: return
        self.distance_x = player.rect.midbottom[0] - self.rect.midbottom[0]
        self.distance_y = player.rect.midbottom[1] - self.rect.midbottom[1]
        # Look towards player
        if self.rect.centerx< player.rect.centerx and self.attacking == -1: 
            self.flip = False 
        else:
            self.flip = True
        # Check horizontal distance
        self.distance = abs(player.rect.centerx - self.rect.centerx)
        if abs(self.distance_x) > self.safe_distance:
            # Move right
            if self.distance_x > 0:
                self.walking = True
                self.rect.x += self.speed           
            # Move left
            else: 
                self.walking = True
                self.rect.x -= self.speed 
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
                attack_chance = random.randint(0,5)
                if attack_chance == 0: self.attacking = 0 # Can start an attack
            
    def combat(self, FPS, player, projectile_group):
        if self.attack_window > 0: self.attack_window -= 10
        if self.blocking > 0: self.blocking -= 10
        if self.current_action == 'BLOCK' and self.blocking <= 0: self.disabled = False
        
        # Check if still Alive
        if self.hp <= 0:
            self.alive = False
            self.disabled = True
            self.current_action = 'DEFEAT'
            self.current_frame = 0
            self.speed = 255

        # Starting an attack
        if self.attacking == 0:
            self.attacking = 1
            self.current_frame = 0
            self.current_action = random.choice(['ATTACK1','ATTACK2','ATTACK3','SPECIAL'])
            self.disabled = True          
            self.attack_window = 500

        # Getting hit        
        # By player
        if player.attacking == 1:
            if self.current_action in ['IDLE','WALK']:
                block_chance = random.randint(0,15)
                # Chance to block
                if block_chance == 0 and abs(self.distance_x) <= self.safe_distance:
                    self.current_action = 'BLOCK'
                    self.disabled = True
                    self.blocking = 200
            # If not blocking, check collision
            if self.disabled == False:
                if (
                    pygame.Rect.colliderect(self.rect, player.hitbox) 
                    and (player.attack_type not in ['THROW','SPECIAL'])
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

        # By projectiles (Bosses ae imune to projectiles)
        for p in projectile_group:
            if pygame.Rect.colliderect(self.rect, p.rect) and self.alive:
                if p.type == 'shield': p.status = -1
                else: pass

    def animate(self, FPS):
        if self.current_frame < 0: return
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
                if self.current_action == 'SPECIAL': 
                    self.rect.x += 25 * (-1 if self.flip else 1)
                elif self.current_action == 'INTRO':
                    self.rect.y += 70 
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
            self.hitbox.x = self.rect.x + (img_width/2)
        else: 
            self.hitbox.x = self.rect.x - (img_width/2.2)

        if not self.alive:        
            self.speed -= 10
            self.image.set_alpha(self.speed)
            if self.speed <= 0: self.kill()

    def portrait(self, screen):
        # Boss portrait shows all the time and sits at the bottom of the screen
        if self.alive:
            # Image
            screen.blit(ASSETS[f'{self.name}_portrait'],   (SCREEN_WIDTH-280, SCREEN_HEIGHT-92))

            # Health Bar
            ratio = self.hp / self.max_hp
            pygame.draw.rect(screen, COLOR_RED,     (300, SCREEN_HEIGHT-50, 700,22))
            pygame.draw.rect(screen, COLOR_YELLOW,  (300, SCREEN_HEIGHT-50, 700 * ratio,22))
            pygame.draw.rect(screen, COLOR_WHITE,   pygame.Rect(300, SCREEN_HEIGHT-50, 700, 22), 2) 

            # Name & Score
            screen.blit(arcadefont.render(self.name, True, COLOR_BLACK), (182,SCREEN_HEIGHT-45))
            screen.blit(arcadefont.render(self.name, True, COLOR_WHITE), (180,SCREEN_HEIGHT-47))
   

    def draw(self, screen, grid):

        # Shadow
        # pygame.draw.ellipse(screen, COLOR_BLACK, (self.rect.x-25, self.rect.midbottom[1]-20, self.width+50, 10))
        # shadow_aux = pygame.transform.flip(self.image, False, True)      
        shadow = pygame.mask.from_surface(pygame.transform.scale( pygame.transform.flip(self.image, False, False), (self.image.get_width(), self.image.get_height()/4)))        
        
        # Enemy Image
        if self.alive: 
            screen.blit(
                shadow.to_surface(unsetcolor=(0,0,0,0), setcolor=(0,0,0,150)), (
                self.rect.x + (self.rect.width - self.image.get_width() if self.flip else 0), 
                self.rect.bottom - shadow.get_rect().height - 15
            ))    
        screen.blit(
            self.image, 
            (
                # self.rect.x + self.rect.width - self.image.get_width() + 30, 
                self.rect.x + (self.rect.width - self.image.get_width() if self.flip else 0), 
                self.rect.y + self.rect.height - self.image.get_height()
            )
        )
         
        if grid:
            # Hitbox
            pygame.draw.rect(screen, COLOR_RED, self.rect, 1)
            pygame.draw.rect(screen, COLOR_RED, self.hitbox, 1)

            # Debug            
            pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect(self.rect.x, self.rect.y-150, self.width, 60))
            screen.blit(smallfont.render(f"Action: {self.current_action} {self.current_frame}", True, COLOR_WHITE), (self.rect.x, self.rect.y-150))
            screen.blit(smallfont.render(f"Blocking: {self.blocking} | Disabled: {self.disabled}", True, COLOR_WHITE), (self.rect.x, self.rect.y-140))
            screen.blit(smallfont.render(f"Walking: {self.walking} | Safe: {self.safe_distance}", True, COLOR_WHITE), (self.rect.x, self.rect.y-130))
            screen.blit(smallfont.render(f"Life: {self.hp}/{self.max_hp} | Flip: {self.flip}", True, COLOR_WHITE), (self.rect.x, self.rect.y-120))
            screen.blit(smallfont.render(f"Attacking: {self.attacking} | Window: {self.attack_window}", True, COLOR_WHITE), (self.rect.x, self.rect.y-110))
            
            # Midbottom Position
            pygame.draw.circle(screen, COLOR_WHITE, self.rect.midbottom, 5)
            pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect(self.rect.midbottom[0]-25, self.rect.midbottom[1]-20, 50, 12))
            screen.blit(smallfont.render(str(self.rect.midbottom), True, COLOR_WHITE), (self.rect.midbottom[0]-25, self.rect.midbottom[1]-20))
