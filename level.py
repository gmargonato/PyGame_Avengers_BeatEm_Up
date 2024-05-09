
import pygame
import csv
from utils import *

# intro_image = re_scale_image(pygame.image.load("SCENARIO/Level_1_Intro.png"), 2)

class Level():
    def __init__(self, level_id):        
        self.events = []
        self.level_id = level_id
        self.visited_checkpoints = []
        self.level_checkpoints = {            
            1 : [20, 900, 2540, 2850, 5080, 6210, 9770, 11470],
        }

    def checkpoint(self, scroll):
        if (scroll in self.level_checkpoints[self.level_id]) and (not scroll in self.visited_checkpoints):
            if scroll == 20:    self.events.append( ('startlevel', None) )
            if scroll == 900:   self.events.append( ('enemy', ('Thug', 10)) )            
            if scroll == 2540:  self.events.append( ('enemy', ('Thug', 20)) )
            if scroll == 2850:  self.events.append( ('object', 'health') )
            if scroll == 5080:  self.events.append( ('enemy', ('Thug', 30)) )
            if scroll == 6210:  self.events.append( ('enemy', ('Thug', 40)) )
            if scroll == 9770:  self.events.append( ('boss',  ('Juggernaut', 1)) )
            if scroll == 11470: self.events.append( ('endlevel', None) )
            self.visited_checkpoints.append(scroll)
            