
import pygame
import csv
from utils import *

# intro_image = re_scale_image(pygame.image.load("SCENARIO/Level_1_Intro.png"), 2)

class Level():
    def __init__(self, level_id):        
        self.events = []
        self.level_id = level_id
        self.visited_checkpoints = []

    def checkpoint(self, scroll):
        if (scroll not in self.visited_checkpoints):
            if self.level_id == 1:
                if scroll == 20:    
                    self.events.append( ('startlevel', None) )
                    self.visited_checkpoints.append(scroll)
                if scroll == 900:   
                    self.events.append( ('enemy', ('Thug', 5)) ) 
                    self.visited_checkpoints.append(scroll)           
                if scroll == 2540:  
                    self.events.append( ('enemy', ('Thug', 10)) )
                    self.visited_checkpoints.append(scroll)
                if scroll == 2850:  
                    self.events.append( ('object', 'health') )
                    self.visited_checkpoints.append(scroll)
                if scroll == 4500:  
                    self.events.append( ('enemy', ('Thug', 15)) )
                    self.visited_checkpoints.append(scroll)
                if scroll == 6500:  
                    self.events.append( ('enemy', ('Thug', 20)) )
                    self.visited_checkpoints.append(scroll)
                if scroll == 8100:  
                    self.events.append( ('object', 'health') )
                    self.visited_checkpoints.append(scroll)
                if scroll == 9770:  
                    self.events.append( ('boss',  ('Juggernaut', 1)) )
                    self.visited_checkpoints.append(scroll)
                if scroll == 11200:  
                    self.events.append( ('object', 'mjolnir') )
                    self.visited_checkpoints.append(scroll)
                if scroll == 11470: 
                    self.events.append( ('endlevel', None) )
                    self.visited_checkpoints.append(scroll)
            elif self.level_id == 2:
                if scroll == 20:    
                    self.events.append( ('startlevel', None) )
                    self.visited_checkpoints.append(scroll)
                