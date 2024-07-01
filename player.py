
import pygame
from utils import *

class Player(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y, action, hp, score):
        pygame.sprite.Sprite.__init__(self)
        self.name = ""
        self.events = []
        self.current_action = action
        self.current_frame = 0       
        self.last_frame_update = -1 if action == 'INTRO' else 0
        self.last_hit_time = pygame.time.get_ticks()
        self.speed = 10
        self.max_hp = 100
        self.hp = hp
        self.score = score   
        self.stance = 1  
        
        # Actions
        self.flip = False
        self.disabled = True
        self.hit = False
        self.walking = None
        self.blocking = False        
        self.attacking = -1 # -1: Not attacking. 0: Starting an attack. 1: Currently attacking
        self.attack_type = None
        self.attack_cycle = 1
        self.attack_window = 0
        self.cooldown = 0
        
        # Sprites
        self.width      = w
        self.heigth     = h
        self.rect       = pygame.Rect(0, 0, self.width, self.heigth) 
        self.rect.midbottom = (x,y)
        self.hitbox = pygame.Rect(0, 0, 50, 50)
        self.animations = self.load_animations()
        self.image = self.animations[self.current_action][self.current_frame]
        
    def load_animations(self):
        animations_dict = {}
        return animations_dict

    def update(self, FPS, can_scroll, enemies):
        self.get_input()
        self.combat(enemies)
        self.move(can_scroll)
        self.animate(FPS)

    def get_input(self):
        if self.disabled or self.hit: return
        keys = pygame.key.get_pressed()

        # Walk
        if (
            (keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d])
            and self.attacking != 1 and self.blocking == False
        ):
            self.walking = True
            self.attacking = -1
            self.flip = True if keys[pygame.K_a] else False
        else:
            self.walking = None

        # Block
        if keys[pygame.K_b] and (self.attacking == -1):
            self.blocking = True
            self.walking = False
        else:
            self.blocking = False 

        # Attack
        if self.cooldown <= 0:
            if (keys[pygame.K_n] or keys[pygame.K_m]) and (self.attacking == -1):
                if (keys[pygame.K_n] and self.blocking) and self.stance == 1:
                    self.attack_type = 'THROW'
                elif (keys[pygame.K_m] and self.blocking and (self.score - 1000 >= 0) and self.stance == 1):
                    self.attack_type = 'SPECIAL'          
                    self.score -= 1000
                elif (keys[pygame.K_n] and not keys[pygame.K_m]):
                    self.attack_type = 'PUNCH'
                elif (keys[pygame.K_m] and not keys[pygame.K_n]):
                    self.attack_type = 'KICK'
                self.attacking = 0

    def combat(self, enemies):
        # Update attack mechanics
        self.attack_window = max(0, self.attack_window - 10)
        self.cooldown = max(0, self.cooldown - 10)

        # Starting an attack
        if self.attacking == 0:
            self.attacking = 1
            if self.attack_type in ['PUNCH','KICK']:
                if (self.attack_window == 0 or self.attack_cycle >= 3):
                    # Reset attack cycle back to 1
                    self.attack_cycle = 1
                else:
                    self.attack_cycle += 1
        
        # Checking enemy attacks
        for enemy in enemies:
            if enemy.attacking == 1:
                if self.rect.colliderect(enemy.hitbox) and pygame.time.get_ticks() - self.last_hit_time > 500 and self.current_action not in ['THROW','SPECIAL']:                                        
                    self.attacking = -1
                    self.attack_cycle = 0
                    self.walking = False
                    if enemy.boss:
                        self.rect.x += (100 if enemy.current_action == 'SLAM' else 25) * (-1 if enemy.rect.centerx > self.rect.centerx else 1)
                    if not self.blocking:
                        self.hit = True
                        self.hp -= 1                     
                        self.last_hit_time = pygame.time.get_ticks()                        
                        self.events.append( ('hit', (enemy.hitbox.x, enemy.hitbox.y)))

        if self.hp <= 0:
            self.disabled = True
            self.current_action = 'DEFEAT'
            
    def move(self, can_scroll):
        if self.walking:            
            keys = pygame.key.get_pressed()
            # Up
            if keys[pygame.K_w] and self.rect.midbottom[1] > 440:
                self.rect.y -= self.speed
            # Down
            if keys[pygame.K_s] and self.rect.midbottom[1] < 690:
                self.rect.y += self.speed
            if can_scroll == False:
                # Left      
                if keys[pygame.K_a] and self.rect.midbottom[0] > 140:
                    self.rect.x -= self.speed
                # Right
                if keys[pygame.K_d] and self.rect.midbottom[0] < SCREEN_WIDTH-140: 
                    self.rect.x += self.speed   

    def shoot(self):
        # Must be overwritten by each character
        return
    
    def special(self):
        # Must be overwritten by each character
        return

    def animate(self, FPS):
        # Trick to freeze animation until player press D
        if self.last_frame_update == -1: return 
        
        num_frames = len(self.animations[self.current_action])
        last_frame = num_frames - 1

        # Disassociate animation interval from game's FPS
        if pygame.time.get_ticks() - self.last_frame_update > FPS * 1.2:
            self.last_frame_update = pygame.time.get_ticks()
        else:
            return

        # Animation Loop
        if num_frames == 1:
            self.current_frame = 0
        else:            
            # Shoot Projectiles
            self.shoot(num_frames)
            # Cast Special
            self.special(num_frames)

            # Keep looping while state is true
            if self.current_frame < last_frame: 
                self.current_frame += 1
            
            # End of animation
            else: 
                self.current_frame = 0
                self.disabled = False
                if self.hit: self.hit = False
                if self.attacking == 1:
                    self.attacking = -1
                    self.attack_window = 100
                    self.attack_type = None
                    self.cooldown = 25
                    if self.attack_cycle == 3 or self.current_action == 'SPECIAL': self.cooldown = 100
                if self.current_action == 'DEFEAT':                    
                    self.last_frame_update = -1
                    self.current_frame = last_frame
                    self.disabled = True
                    self.events.append( ('defeat',None) )
                
        next_action = self.current_action

        if self.disabled:
            pass
        elif self.hit:
            next_action = 'HIT'
        elif self.walking:
            next_action = 'WALK'
        elif self.blocking:
            next_action = 'BLOCK'
        elif self.attacking == 1:            
            if self.attack_type in ['PUNCH','KICK']:
                next_action = f'{self.attack_type}{self.attack_cycle}'            
            elif self.attack_type == 'SPECIAL':   
                next_action = 'SPECIAL'
            elif self.attack_type == 'THROW':
                next_action = 'THROW'
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

    def draw(self, screen, grid):
        # Shadow
        # shadow = pygame.mask.from_surface(pygame.transform.scale( pygame.transform.flip(self.image, False, True), (self.image.get_width(), self.image.get_height()/4)))        
        # screen.blit(shadow.to_surface(unsetcolor=(0,0,0,0), setcolor=(0,0,0,150)), (
        #     self.rect.x + (self.rect.width - self.image.get_width() if self.flip else 0), 
        #     self.rect.bottom-15
        # ))        
        shadow = pygame.mask.from_surface(pygame.transform.scale( pygame.transform.flip(self.image, False, False), (self.image.get_width(), self.image.get_height()/4)))        
        screen.blit(shadow.to_surface(unsetcolor=(0,0,0,0), setcolor=(0,0,0,150)), (
            self.rect.x + (self.rect.width - self.image.get_width() if self.flip else 0), 
            self.rect.bottom - shadow.get_rect().height - 15
        ))        
        # Sprite
        screen.blit(self.image, (            
            self.rect.x + (self.rect.width - self.image.get_width() if self.flip else 0), 
            self.rect.y + self.rect.height - self.image.get_height()
        ))
        # Debug
        if grid:
            pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect(self.rect.x, self.rect.y - 130, self.width, 85))
            screen.blit(smallfont.render(f"Action: {self.current_action} {self.current_frame}", True, COLOR_WHITE), (self.rect.x, self.rect.y - 130))
            screen.blit(smallfont.render(f"Flip: {self.flip}", True, COLOR_WHITE), (self.rect.x, self.rect.y - 118))
            screen.blit(smallfont.render(f"Disabled: {self.disabled} | Cooldown: {self.cooldown}", True, COLOR_WHITE), (self.rect.x, self.rect.y - 106))
            screen.blit(smallfont.render(f"Walking: {self.walking} | Blocking: {self.blocking}", True, COLOR_WHITE), (self.rect.x, self.rect.y - 94))
            screen.blit(smallfont.render(f"Attacking: {self.attacking} | Type: {self.attack_type}", True, COLOR_WHITE), (self.rect.x, self.rect.y - 82))
            screen.blit(smallfont.render(f"Cycle: {self.attack_cycle} | Window: {self.attack_window}", True, COLOR_WHITE), (self.rect.x, self.rect.y - 70))
            screen.blit(smallfont.render(f"Life: {self.hp}/{self.max_hp}", True, COLOR_WHITE), (self.rect.x, self.rect.y - 58))
            # Hitbox
            pygame.draw.rect(screen, COLOR_GREEN, self.rect, 1)
            pygame.draw.rect(screen, COLOR_GREEN, self.hitbox, 1)
            # Midbottom Position
            pygame.draw.circle(screen, COLOR_WHITE, self.rect.midbottom, 5)
            pygame.draw.rect(screen, COLOR_BLACK, pygame.Rect(self.rect.midbottom[0]-25, self.rect.midbottom[1]-20, 50, 12))
            screen.blit(smallfont.render(str(self.rect.midbottom), True, COLOR_WHITE), (self.rect.midbottom[0]-25, self.rect.midbottom[1]-20))    
            
    def portrait(self, screen):
            # Image
            screen.blit(ASSETS[f'{self.name}_portrait'],   (50, 50))
            # Health Bar
            ratio = self.hp / self.max_hp
            pygame.draw.rect(screen, COLOR_RED,     (110,92,300,22))
            pygame.draw.rect(screen, COLOR_YELLOW,  (110,92,300 * ratio,22))
            pygame.draw.rect(screen, COLOR_WHITE,   pygame.Rect(110, 92, 300, 22), 2)
            # Name & Score
            screen.blit(arcadefont.render(self.name, True, COLOR_BLACK), (117,52))
            screen.blit(arcadefont.render(self.name, True, COLOR_WHITE), (115,50))
            screen.blit(arcadefont.render(str(self.score),True, COLOR_BLACK), (117,72))
            screen.blit(arcadefont.render(str(self.score),True, COLOR_WHITE), (115,70))
