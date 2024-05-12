
# Libraries
import pygame
import sys
import random
import pretty_errors
import time

from utils import *
from world import *
from level import *
from animation import *
from object import *
from spark import *
from captain import *
from hulk import *
from spider import *
from shield import *
from web import *
from rock import *
from shockwave import *
from enemy import *
from juggernaut import *

class Game():
    def __init__(self, state):  
        # Pygame
        pygame.init()
        pygame.display.set_caption("Avengers: Battle for New York")
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.current_state = state

        # Game variables        
        self.paused             = False
        self.game_over          = False
        self.grid               = False
        self.can_scroll         = True
        self.screen_shake       = 0
        self.fps                = 30
        self.scroll             = 20
        self.level_id           = 1
        self.aux_count          = 0

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

        if self.current_state == 'menu':
            self.player_menu_cap    = Captain(w=160, h=220, x=150, y=550, stance=1, action='INTRO', hp=100, score=0)
            self.player_menu_hulk   = Hulk(w=160, h=230, x=500, y=550, action='INTRO', hp=100, score=0)
            self.player_menu_spider = Spider(w=160, h=230, x=700, y=550, action='INTRO', hp=100, score=0)
            self.characters_group.add(self.player_menu_cap, self.player_menu_hulk, self.player_menu_spider)
        else:
            self.player = Spider(w=160, h=220, x=SCREEN_WIDTH/2, y=550, action='IDLE', hp=3, score=10000)
            # self.player = Captain(w=160, h=220, x=SCREEN_WIDTH/2, y=550, stance=1, action='IDLE', hp=3, score=10000)
            # self.player = Hulk(w=160, h=230, x=SCREEN_WIDTH/2, y=550, action='IDLE', hp=3, score=10000)
            self.characters_group.add(self.player)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()     
            if event.type == pygame.KEYDOWN:
                if self.current_state == 'game':
                    if event.key == pygame.K_ESCAPE and not self.game_over:
                        self.paused = not self.paused # Switch between True and False
                        self.aux_count = 1 if self.paused else 0
                    if event.key == pygame.K_ESCAPE and self.game_over:                        
                        self.__init__('menu')
                    if event.key == pygame.K_BACKQUOTE:                    
                        for character in self.enemies_group:
                            if not isinstance(character, Player):
                                character.kill()
                    if event.key == pygame.K_1:
                        self.spawn_enemy(1, 'Thug')
                    if event.key == pygame.K_2:
                        self.spawn_enemy(1, 'Juggernaut')
                    if event.key == pygame.K_g:
                        self.grid = not self.grid
                        pygame.mouse.set_visible(self.grid)                
                    if self.grid: 
                        if event.key == pygame.K_UP:
                            self.fps = min(self.fps + 5, 60)
                        if event.key == pygame.K_DOWN:
                            self.fps = max(self.fps - 5, 5)
                        if event.key == pygame.K_RIGHT:
                            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                                self.scroll += 1000           
                            else:
                                self.scroll += 500
                        if event.key == pygame.K_LEFT:
                            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                                self.scroll -= 1000
                            else:    
                                self.scroll -= 500
                elif self.current_state == 'intro':
                    if event.key == pygame.K_ESCAPE:
                        self.animation_group.add(Animation(name='fade_out', transparency=False, flip=False, x=0, y=0))
                elif self.current_state == 'menu':
                    if (event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3) and self.aux_count == 0:
                        if event.key == pygame.K_1:
                            self.player_menu_cap.last_frame_update = 0
                            self.player = Captain(w=160, h=220, x=SCREEN_WIDTH/2, y=550, stance=1, action='IDLE', hp=100, score=0)                            
                        elif event.key == pygame.K_2:                            
                            self.player_menu_hulk.last_frame_update = 0
                            self.player = Hulk(w=160, h=230, x=SCREEN_WIDTH/2, y=550, action='IDLE', hp=100, score=0)
                        else:
                            self.player_menu_spider.last_frame_update = 0
                            self.player = Spider(w=160, h=230, x=SCREEN_WIDTH/2, y=550, action='IDLE', hp=100, score=0)
                        self.aux_count = 1

    def end_level(self, scroll, reset):
        self.level.visited_checkpoints = []
        self.can_scroll = True
        self.scroll = scroll
        self.player.rect.y = 350
        if reset == False:
            self.level_id += 1
            self.world = World(self.level_id)

    def pause_menu(self):
        if self.game_over:            
            draw_rect_alpha(self.display, (255,0,0,255), 0,0,SCREEN_WIDTH, SCREEN_WIDTH)                
            self.display.blit(arcadefont.render(f"Game Over", True, COLOR_BLACK), (SCREEN_WIDTH/2-48, SCREEN_HEIGHT/2+2))
            self.display.blit(arcadefont.render(f"Game Over", True, COLOR_WHITE), (SCREEN_WIDTH/2-50, SCREEN_HEIGHT/2))
            self.display.blit(arcadefont.render(f"Press ESC to select a new hero", True, COLOR_BLACK), (SCREEN_WIDTH/3+70, SCREEN_HEIGHT/2+50))
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
                x = SCREEN_WIDTH,
                y = 600,
            )
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
        # Game's FPS
        self.display.blit(font.render(f"FPS: {str(int(self.clock.get_fps()))}", True, COLOR_WHITE), (0, 0))
        # Current Scroll
        pygame.draw.rect(self.display, COLOR_BLACK, pygame.Rect(15, SCREEN_HEIGHT-70, 150, 50))
        self.display.blit(font.render(f"Locked: {not self.can_scroll}", True, COLOR_WHITE), (15, SCREEN_HEIGHT-70))
        self.display.blit(font.render(f"Scroll: {self.scroll}", True, COLOR_WHITE), (15, SCREEN_HEIGHT-50))
        
    def state_menu(self):
        if self.aux_count < 2:
            self.display.fill(COLOR_BLACK)
            # Page Title
            self.display.blit(arcadefont.render(f"SELECT YOUR HERO", True, COLOR_YELLOW), (SCREEN_WIDTH/2-50, 100))
            # Heroes
            self.display.blit(arcadefont.render(f"CAPTAIN AMERICA", True, COLOR_WHITE), (100, SCREEN_HEIGHT/3))
            self.display.blit(arcadefont.render(f"THE INCREDIBLE HULK", True, COLOR_WHITE), (400, SCREEN_HEIGHT/3))            
            self.display.blit(arcadefont.render(f"SPIDER-MAN", True, COLOR_WHITE), (700, SCREEN_HEIGHT/3))            
            for player in self.characters_group:
                player.update(self.fps, self.can_scroll, self.enemies_group)
                player.draw(self.display, self.grid)
                if not player.disabled:
                    self.aux_count = 3
            # Key
            self.display.blit(arcadefont.render(f"Press 1", True, COLOR_WHITE), (100, SCREEN_HEIGHT-140))
            self.display.blit(arcadefont.render(f"Press 2", True, COLOR_WHITE), (400, SCREEN_HEIGHT-140))
            self.display.blit(arcadefont.render(f"Press 3", True, COLOR_WHITE), (700, SCREEN_HEIGHT-140))
        
        else:           
            self.characters_group.empty()
            self.characters_group.add(self.player)
            self.current_state = 'intro'
            self.aux_count = 0
        self.screen.blit(pygame.transform.scale(self.display,(SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

    def state_intro(self):
        self.display.blit(ASSETS['intro_image'], (0,self.aux_count))
        self.display.blit(ASSETS['intro_meanwhile'], (50,50))
        if self.aux_count > -1000: 
            self.aux_count -= 15
        elif self.aux_count <= -1000:             
            self.animation_group.add(Animation(name='fade_out', transparency=False, flip=False, x=0, y=0))
        self.display.blit(arcadefont.render("Press 'ESC' to Skip intro", True, COLOR_BLACK), (SCREEN_WIDTH-268, SCREEN_HEIGHT-48))
        self.display.blit(arcadefont.render("Press 'ESC' to Skip intro", True, COLOR_WHITE), (SCREEN_WIDTH-270, SCREEN_HEIGHT-50))
        for animation in self.animation_group:
            finished = animation.update(self.fps, self.display)                    
            if finished: 
                self.aux_count = 0           
                self.current_state = 'game'
                animation.kill()        
        self.screen.blit(pygame.transform.scale(self.display,(SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

    def state_game(self):
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

            # Level ---------------------------------------------------------------------- #
            self.can_scroll = self.check_can_scroll()
            self.level.checkpoint(self.scroll)
            if not self.can_scroll: 
                self.display.blit(ASSETS['checkpoint_stop'],(SCREEN_WIDTH-120, 100))
            else:                    
                for visited_scroll in self.level.visited_checkpoints:
                    if abs(visited_scroll - self.scroll) <= 200: 
                        self.display.blit(ASSETS['checkpoint_go'],(SCREEN_WIDTH-200, 100))
                # Re-center player if needed
                if self.player.walking:                        
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
                elif event_type == 'object':
                    obj = Object(name=event_value, scroll=self.scroll, x=640, y=500)
                    self.object_group.add(obj)                
                    self.level.events.remove(event)
                else:
                    # Pass
                    self.level.events.remove(event)    

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
                if event_type == 'web':
                    web = Web(x=event_value[0], y=event_value[1], floor=self.player.rect.midbottom[1], flip=event_value[3])
                    self.projectile_group.add(web)
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

            # particles ----------------------------------------------------------------------- #
            # Hit spark
            for i, spark in sorted(enumerate(self.sparks), reverse=True):
                spark.move(1)
                spark.draw(self.display)
                if not spark.alive: self.sparks.pop(i)

            # World Foreground ---------------------------------------------------------------- #
            self.world.draw_foreground(self.display, self.scroll)

            # Animations ---------------------------------------------------------------------- #
            for animation in self.animation_group:
                finished = animation.update(self.fps, self.display)                    
                if finished: 
                    if animation.name == 'fade_out': self.end_level(20, True)                                  
                    if animation.name == 'defeat': self.paused = True; self.game_over = True
                    animation.kill()

            player_portrait(self.display, self.player)
            if self.grid: self.grid_mode()
        self.screen.blit(pygame.transform.scale(self.display,(SCREEN_WIDTH, SCREEN_HEIGHT)), (shake_x, shake_y))

    def run(self):        
        while True:            
            # Events
            self.handle_events()

            # Game States
            if self.current_state == 'menu':
                self.state_menu()
            elif self.current_state == 'intro':
                self.state_intro()
            else:
                self.state_game()

            # Update display
            pygame.display.update()            
            self.clock.tick(self.fps)

if __name__ == "__main__":
    game = Game('menu')    
    game.run()
