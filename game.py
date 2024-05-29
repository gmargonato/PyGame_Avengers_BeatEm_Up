
# Libraries
import pygame
import random

from utils import *
from world import *
from level import *
from animation import *
from object import *
from spark import *
from captain import *
from hulk import *
from spider import *
from thor import *
from shield import *
from web import *
from webnet import *
from rock import *
from mjolnir import *
from shockwave import *
from enemy import *
from juggernaut import *

class Game():
    def __init__(self, player, level_id, fps, display):  

        # Game variables      
        self.fps            = fps
        self.display        = display  
        self.paused         = False
        self.game_over      = False
        self.grid           = False
        self.can_scroll     = True
        self.screen_shake   = 0        
        self.scroll         = 20
        self.level_id       = level_id
        self.aux_count      = 0
        self.timer          = pygame.time.get_ticks() 

        # Sprite groups
        self.characters_group   = pygame.sprite.Group()
        self.enemies_group      = pygame.sprite.Group()
        self.projectile_group   = pygame.sprite.Group()
        self.animation_group    = pygame.sprite.Group()
        self.object_group       = pygame.sprite.Group()

        # Game entities
        self.world  = World(self.level_id)
        self.level  = Level(self.level_id)
        self.sparks = []
        if player:
            self.player = player
        else:
            # self.player = Captain(w=160,h=220, x=SCREEN_WIDTH/2, y=550, stance=1, action='IDLE', hp=10, score=10000)
            # self.player = Hulk(w=160,   h=230, x=SCREEN_WIDTH/2, y=550, action='IDLE', hp=10, score=10000)
            # self.player = Spider(w=160, h=230, x=SCREEN_WIDTH/2, y=550, action='IDLE', hp=10, score=10000)
            self.player = Thor(w=160,   h=230, x=SCREEN_WIDTH/2, y=550, action='IDLE', hp=10, score=10000)
        self.characters_group.add(self.player)

    def handle_game_events(self):
        if pygame.time.get_ticks() - self.timer < 100:
            return            
        else:
            self.timer = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] and not self.game_over:
                self.paused = not self.paused # Switch between True and False
                self.aux_count = 1 if self.paused else 0
            if keys[pygame.K_ESCAPE] and self.game_over:                        
                # To-do
                pygame.quit()
                sys.exit()  
            if keys[pygame.K_BACKQUOTE]:                    
                for character in self.enemies_group:
                    if not isinstance(character, Player):
                        character.kill()
            if keys[pygame.K_1]:
                self.spawn_enemy(1, 'Thug')
            if keys[pygame.K_2]:
                self.spawn_enemy(1, 'Juggernaut')
            if keys[pygame.K_g]:
                self.grid = not self.grid
                pygame.mouse.set_visible(self.grid)                
            if self.grid: 
                if keys[pygame.K_UP]:
                    self.fps = min(self.fps + 1, 60)
                if keys[pygame.K_DOWN]:
                    self.fps = max(self.fps - 1, 5)
                if keys[pygame.K_RIGHT]:
                    self.scroll += 100
                if keys[pygame.K_LEFT]:
                    self.scroll -= 100
    
    def end_level(self, scroll, reset):
        self.level.visited_checkpoints = []
        self.can_scroll = True
        self.scroll = 20
        self.player.rect.y = 350
        self.aux_count = 0
        if reset == False:
            self.level_id += 1
            self.world = World(self.level_id)
            self.level = Level(self.level_id)

    def pause_menu(self):
        if self.game_over:            
            draw_rect_alpha(self.display, (255,0,0,255), 0,0,SCREEN_WIDTH, SCREEN_WIDTH)                
            self.display.blit(arcadefont.render(f"Game Over", True, COLOR_BLACK), (SCREEN_WIDTH/2-48, SCREEN_HEIGHT/2))
            self.display.blit(arcadefont.render(f"Game Over", True, COLOR_WHITE), (SCREEN_WIDTH/2-50, SCREEN_HEIGHT/2))
            self.display.blit(arcadefont.render(f"Score: {self.player.score}", True, COLOR_YELLOW), (SCREEN_WIDTH/3+150, SCREEN_HEIGHT/2+50))
            self.display.blit(arcadefont.render(f"Press ESC to select a new hero", True, COLOR_BLACK), (SCREEN_WIDTH/3+70, SCREEN_HEIGHT-150))
        else:
            if self.aux_count == 1:
                draw_rect_alpha(self.display, (0,0,0,150), 0,0,SCREEN_WIDTH, SCREEN_WIDTH)
                self.aux_count = 2
            self.display.blit(arcadefont.render(f"Game Paused", True, COLOR_WHITE), (SCREEN_WIDTH/2-50, SCREEN_HEIGHT/2))

    def spawn_enemy(self, n, name):
        if name == 'Thug':
            for i in range(n):
                enemy = Enemy(
                    name=random.choice(['Guile','Jill']),
                    x=random.choice([-100 - (i * 400), SCREEN_WIDTH +100 + (i*400)]),
                    # x = random.choice([SCREEN_WIDTH/3, SCREEN_WIDTH/1.5]),
                    y=random.choice([500,600,700]),
                )
                self.enemies_group.add(enemy)
                self.characters_group.add(enemy)
        elif name == 'Juggernaut':
            enemy = Juggernaut(
                name='Juggernaut',
                x = SCREEN_WIDTH-150,
                y = 0,
            )
            self.screen_shake = 20
            self.enemies_group.add(enemy)
            self.characters_group.add(enemy)

    def check_can_scroll(self):
        if len(self.projectile_group) > 0: return False
        for character in self.characters_group:
            if not isinstance(character, Player):
                return False            
        return True
    
    def generate_spark(self, x, y):
        for i in range(5): 
            self.sparks.append(
                Spark(loc=[x, y], angle=math.radians(random.randint(0,360)), speed=20, scale=1)
            )

    def grid_mode(self):       
        # Current Scroll
        pygame.draw.rect(self.display, COLOR_BLACK, pygame.Rect(15, SCREEN_HEIGHT-70, 150, 50))
        self.display.blit(font.render(f"Locked: {not self.can_scroll}", True, COLOR_WHITE), (15, SCREEN_HEIGHT-70))
        self.display.blit(font.render(f"Scroll: {self.scroll}", True, COLOR_WHITE), (15, SCREEN_HEIGHT-50))
        
    def run(self):
        # Handle Game Events
        self.handle_game_events()

        shake_x = 0
        shake_y = 0
        if self.paused: 
            self.pause_menu()            
        else:
            
            # World ---------------------------------------------------------------------- #
            self.display.fill(COLOR_BLACK)
            self.world.draw_background(self.display, self.scroll)
            self.world.draw_midground(self.display, self.scroll)
            
            if self.screen_shake:
                shake_x += random.randint(0, 8) - 4
                shake_y += random.randint(0, 8) - 4
            if self.screen_shake > 0: self.screen_shake -= 1

            # Objects --------------------------------------------------------------------- #
            for object in self.object_group:
                object.update(self.scroll, self.player)
                object.draw(self.display, self.grid)

            # Player ---------------------------------------------------------------------- #
            self.player.update(self.fps, self.can_scroll, self.enemies_group)
            # Events
            for event in self.player.events:
                event_type  = event[0]
                event_value = event[1]                                            
                if event_type == 'defeat':
                    anim = Animation(name='defeat', transparency=False, flip=False, x=0, y=0)
                    self.animation_group.add(anim)
                    self.player.events.remove(event)                    
                if event_type == 'hit':
                    self.generate_spark(event_value[0], event_value[1])
                    self.player.events.remove(event)
                if event_type == 'shield':
                    shield = Shield(x=event_value[0], y=event_value[1], initial_scroll=self.scroll, dir=self.player.flip, floor=self.player.rect.midbottom[1], status=1)
                    self.projectile_group.add(shield)
                    self.player.events.remove(event)
                    # Chage player stance
                    self.player.change_instance(2)
                if event_type == 'rock':
                    rock = Rock(x=event_value[0], y=event_value[1], floor=event_value[2], flip=event_value[3])
                    self.projectile_group.add(rock)
                    self.player.events.remove(event)
                if event_type == 'mjolnir':
                    hammer = Mjolnir(x=event_value[0], y=event_value[1], floor=event_value[2], flip=event_value[3], status=1)
                    self.projectile_group.add(hammer)
                    self.player.events.remove(event)
                if event_type == 'web':
                    web = Web(x=event_value[0], y=event_value[1], floor=self.player.rect.midbottom[1], flip=event_value[3])
                    self.projectile_group.add(web)
                    self.player.events.remove(event)
                if event_type == 'webnet':
                    if len(self.enemies_group) > 0:
                        for enemy in self.enemies_group:
                            if 0 < enemy.rect.right and enemy.rect.left < SCREEN_WIDTH:
                                webnet = Webnet(enemy.rect.centerx, enemy.rect.top - enemy.rect.height - 350)
                                if not enemy.boss: self.projectile_group.add(webnet)
                                # print(f"Webnet created at {enemy.rect.centerx}")
                    self.player.events.remove(event)
                if event_type == 'shockwave':
                    self.screen_shake = 10
                    wave = Shockwave(x = event_value[0], y=event_value[1], color=event_value[2])
                    self.projectile_group.add(wave)
                    self.player.events.remove(event)

            # Enemies -------------------------------------------------------------------------- #
            for enemy in self.enemies_group:
                enemy.update(self.fps, self.player, self.projectile_group)
                # Events
                for event in enemy.events:
                    event_type  = event[0]
                    event_value = event[1]
                    if event_type == 'hit':
                        self.generate_spark(event_value[0], event_value[1])
                        enemy.events.remove(event)

            # Blit characters on screen (Players, Enemies and Bosses) -------------------------- #
            for character in sorted(self.characters_group, key=lambda x: x.rect.midbottom[1] ):
                character.draw(self.display, self.grid)
            
            # Projectiles ---------------------------------------------------------------------- #
            for projectile in self.projectile_group:
                projectile.update(self.scroll, self.fps)
                projectile.draw(self.display, self.grid)
                if projectile.type == 'shield':
                    if self.player.rect.colliderect(projectile.rect): 
                        if projectile.status == 0:
                            self.player.recover("air")
                            projectile.kill()
                        elif projectile.status == -1: 
                            self.player.recover("floor")                                
                            projectile.kill()
                elif projectile.type == 'rock':
                    if projectile.index == 1: self.screen_shake = 10

            # Hit particles ------------------------------------------------------------------- #
            for i, spark in sorted(enumerate(self.sparks), reverse=True):
                spark.move(1)
                spark.draw(self.display)
                if not spark.alive: self.sparks.pop(i)

            # World Foreground ---------------------------------------------------------------- #
            self.world.draw_foreground(self.display, self.scroll, self.can_scroll)

            # Level ---------------------------------------------------------------------- #
            self.can_scroll = self.check_can_scroll()
            self.level.checkpoint(self.scroll)
            if len(self.enemies_group) == 0:
                if self.aux_count <= 81: 
                    self.aux_count += 1
                    if (0 < self.aux_count < 20) or (30 < self.aux_count < 50) or (60 < self.aux_count < 80):
                        self.display.blit(ASSETS['checkpoint_go'],(SCREEN_WIDTH-180, 50))
            else:
                self.aux_count = 0
            # if self.can_scroll:                    
                # Re-center player if needed
            if self.can_scroll and self.player.walking:                        
                self.scroll = max(0, self.scroll + 10 * (-1 if self.player.flip else 1))
                if self.player.rect.midbottom[0] > SCREEN_WIDTH/2:
                    self.player.rect.x -= 5
                elif self.player.rect.midbottom[0] < SCREEN_WIDTH/2:
                    self.player.rect.x += 5
            # Events
            for event in self.level.events:
                event_type  = event[0]
                event_value = event[1]
                if event_type == 'startlevel':       
                    anim = Animation(name='fade_in', transparency=False, flip=False, x=0, y=0)
                    self.animation_group.add(anim)
                    self.level.events.remove(event)  
                elif event_type == 'endlevel':       
                    anim = Animation(name='fade_out', transparency=False, flip=False, x=0, y=0)
                    self.animation_group.add(anim)
                    self.level.events.remove(event)    
                elif event_type == 'enemy':
                    enemy_name = event_value[0]
                    enemy_qtt = event_value[1]
                    self.spawn_enemy(enemy_qtt, enemy_name)
                    self.level.events.remove(event)
                elif event_type == 'boss':
                    enemy_name = event_value[0]
                    enemy_qtt = event_value[1]
                    self.spawn_enemy(enemy_qtt, enemy_name)
                    self.level.events.remove(event)
                elif event_type == 'object':
                    obj = Object(name=event_value, scroll=self.scroll, x=640, y=500)
                    self.object_group.add(obj)                
                    self.level.events.remove(event)
                else:
                    # Pass
                    self.level.events.remove(event)    

            # Animations ---------------------------------------------------------------------- #
            for animation in self.animation_group:
                finished = animation.update(self.fps, self.display)                    
                if finished: 
                    if animation.name == 'fade_out': self.end_level(20, False)                                  
                    if animation.name == 'defeat': self.paused = True; self.game_over = True
                    animation.kill()

            self.player.portrait(self.display)
            for enemy in self.enemies_group:
                if enemy.boss: enemy.portrait(self.display)
                else: continue
            if self.grid: 
                self.grid_mode()
        
        self.display.blit(pygame.transform.scale(self.display,(SCREEN_WIDTH, SCREEN_HEIGHT)), (shake_x, shake_y))

