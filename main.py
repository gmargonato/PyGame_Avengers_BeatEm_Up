
import pygame
import sys
import pretty_errors
from utils import *
from menu import *
from cutscene import *
from game import *

class Main():
    def __init__(self, initial_state):
        # Pygame
        pygame.init()
        pygame.display.set_caption("Avengers: Battle for New York")
        pygame.mouse.set_visible(False)
        self.window     = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display    = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA)
        self.clock      = pygame.time.Clock()
        self.fps = 30

        # States
        # Initially, only Menu is loaded. Additional states are loaded as needed
        self.states = {
            'menu' :  Menu(self.fps, self.display)
        }

        # Temporary code to boot directly into the game state
        if initial_state == 'game':
            # player = Captain(w=160,h=230, x=SCREEN_WIDTH/2, y=550, stance=1, action='IDLE', hp=50, score=10000)
            player = Hulk(w=160,   h=230, x=SCREEN_WIDTH/2, y=550, action='IDLE', hp=5, score=10000)
            # player = Spider(w=160, h=230, x=SCREEN_WIDTH/2, y=550, action='IDLE', hp=5, score=10000)
            # player = Thor(w=160,   h=230, x=SCREEN_WIDTH/2, y=550, action='IDLE', hp=5, score=10000)
            self.states['game'] = Game(player, 1, self.fps, self.display)
            
        self.current_state = initial_state

    def run(self):        
        while True:    
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()     

            # Run the current game state
            self.states[self.current_state].run()
 
            # Move from Menu to Cutscene
            if self.current_state == 'menu' and self.states['menu'].player:
                self.states['cutscene'] = Cutscene(self.fps, self.display)
                self.current_state = 'cutscene'
            # Move from Cutscene to Game
            elif self.current_state == 'cutscene' and self.states['cutscene'].pos_y == -1:
                self.current_state = 'game'
                self.states['game'] = Game(self.states['menu'].player, 1, self.fps, self.display)
                self.states['cutscene'] = None
            # Move from Game back to Menu
            elif self.current_state == 'game' and self.states['game'].fps == -1:
                self.current_state = 'menu'                
                self.states['menu'].__init__(self.fps, self.display)
                self.states['game'] = None
            
            # Update screen
            self.window.blit(self.display, (0,0))
            pygame.display.update()            
            self.clock.tick(self.fps)

if __name__ == "__main__":
    game = Main('game')    
    game.run()