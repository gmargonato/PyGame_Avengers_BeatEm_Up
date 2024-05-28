
import pygame
import csv
from utils import *

MAP_SCALE = 2.5

class World():
    def __init__(self, level):
        self.level = level
        self.layer_0, self.layer_1, self.layer_2, self.layer_3 = self.load_level()
        self.layer_0_images  = load_sprites_from_folder('SCENARIO/SKY',MAP_SCALE)
        self.layer_1_images  = load_sprites_from_folder(f'SCENARIO/BACKGROUND/LEVEL_{self.level}',  MAP_SCALE)
        self.layer_2_images  = load_sprites_from_folder(f'SCENARIO/MIDGROUND/LEVEL_{self.level}',   MAP_SCALE)
        self.layer_3_images  = load_sprites_from_folder('SCENARIO/FOREGROUND/',  MAP_SCALE)

    def load_level(self):  
        with open(f'world_{self.level}.csv', newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for i, row in enumerate(csv_reader):
                row_values = [int(cell) for cell in row]
                # Assign the row values to the appropriate layers based on the row index
                if   i == 0:
                    layer_0 = row_values
                elif i == 1:
                    layer_1 = row_values
                elif i == 2:
                    layer_2 = row_values
                elif i == 3:
                    layer_3 = row_values
        return layer_0, layer_1, layer_2, layer_3

    def draw_background(self, screen, scroll):
        screen.fill(COLOR_BLACK)
        # Draw Layer 0 (sky)
        for i,tile in enumerate(self.layer_0):
            image = self.layer_0_images[tile]
            screen.blit(image, (i*(360*MAP_SCALE) + scroll * (-1), 0))        
        # Draw Layer 1 (buildings)
        for i,tile in enumerate(self.layer_1):
            image = self.layer_1_images[tile]
            screen.blit(image, (i*(360*MAP_SCALE) + scroll * (-1), 0))
            
    def draw_midground(self, screen, scroll):
        # Draw Layer 2 (street)
        for i,tile in enumerate(self.layer_2):
            image = self.layer_2_images[tile]
            screen.blit(image, (i*(360*MAP_SCALE) + scroll * (-1), self.layer_1_images[0].get_height()))
            
    def draw_foreground(self, screen, scroll, can_scroll):
        # Draw Layer 3 (foreground)
        for i,tile in enumerate(self.layer_3):
            if tile >= 0:
                image = self.layer_3_images[tile]
                if can_scroll == False:
                    image.set_alpha(150)
                else:
                    image.set_alpha(255)
                screen.blit(image, (i*720 + scroll * (-1), 0), special_flags=0)                
