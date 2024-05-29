
import pygame
import sys
import pretty_errors
from utils import *
from menu import *
from cutscene import *
from game import *

class Main():
    def __init__(self, current_state):
        # Pygame
        pygame.init()
        pygame.display.set_caption("Avengers: Battle for New York")
        pygame.mouse.set_visible(False)
        self.window     = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display    = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA)
        self.clock      = pygame.time.Clock()
        self.fps = 30

        # States
        self.state_menu     = Menu(self.fps, self.display)
        self.state_cutscene = Cutscene(self.fps, self.display)    
        self.state_game     = Game(None, 1, self.fps, self.display)    
        self.states = {
            'menu'      : self.state_menu,
            'cutscene'  : self.state_cutscene,
            'game'      : self.state_game,
        }
        self.current_state = current_state

    def run(self):        
        while True:    
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()     

            # Game States
            self.states[self.current_state].run()
            if self.current_state == 'menu' and self.state_menu.player:
                self.current_state = 'cutscene'
            elif self.current_state == 'cutscene' and self.state_cutscene.pos_y == -1:
                self.current_state = 'game'

            # Update screen
            self.window.blit(self.display, (0,0))
            pygame.display.update()            
            self.clock.tick(self.fps)

if __name__ == "__main__":
    game = Main('game')    
    game.run()