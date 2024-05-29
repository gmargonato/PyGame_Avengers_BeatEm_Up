
import pygame
import os

pygame.font.init()
font = pygame.font.SysFont('Arial Black', 20)
smallfont = pygame.font.SysFont('Arial', 10)
arcadefont = pygame.font.SysFont('nutshell-news', 15)

SCREEN_WIDTH    = 1280
SCREEN_HEIGHT   = 700

COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)
COLOR_RED   = (255,0,0)
COLOR_GREEN = (0,255,0)
COLOR_BLUE  = (0,0,255)
COLOR_PINK  = (255,0,255)
COLOR_YELLOW = (255,255,0)

def load_sprites_from_folder(path, scale=2, transparency=False):
    images_list = []
    files = os.listdir(path)
    png_files = [file for file in files if file.endswith('.png')]
    png_files.sort(key=lambda x: int(x.split('.')[0]))    
    for png_file in png_files:
        full_path = os.path.join(path, png_file)
        image = re_scale_image(pygame.image.load(full_path), scale)
        if transparency: image.set_colorkey((0, 0, 0))
        images_list.append(image)
    return images_list

def re_scale_image(image, scale):
    return pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))

def draw_rect_alpha(surface, color, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

ASSETS = {
    'character_selection'       : re_scale_image(pygame.image.load("ASSETS/character_selection.png"), 1),
    'intro_image'               : re_scale_image(pygame.image.load("ASSETS/level_1_intro.png"), 2.6),
    'intro_text_1'              : re_scale_image(pygame.image.load("ASSETS/intro_text_1.png"), 1),
    'intro_text_2'              : re_scale_image(pygame.image.load("ASSETS/intro_text_2.png"), 1),
    'checkpoint_stop'           : re_scale_image(pygame.image.load("ASSETS/CHECKPOINT/stop.png"), 2),
    'checkpoint_go'             : re_scale_image(pygame.image.load("ASSETS/CHECKPOINT/go.png"), 2),
    'Captain America_portrait'  : re_scale_image(pygame.image.load("ASSETS/PORTRAITS/captain.png"), 2),
    'Hulk_portrait'             : re_scale_image(pygame.image.load("ASSETS/PORTRAITS/hulk.png"), 2),
    'Thor_portrait'             : re_scale_image(pygame.image.load("ASSETS/PORTRAITS/temp.png"), 2),
    'Spider-Man_portrait'       : re_scale_image(pygame.image.load("ASSETS/PORTRAITS/spider.png"), 2),
    'Guile_portrait'            : re_scale_image(pygame.image.load("ASSETS/PORTRAITS/guile.png"), 2),
    'Jill_portrait'             : re_scale_image(pygame.image.load("ASSETS/PORTRAITS/jill.png"), 2),    
    'Juggernaut_portrait'             : re_scale_image(pygame.image.load("ASSETS/PORTRAITS/juggernaut.png"), 2),    
}

OBJECTS = {
     'mjolnir'  : re_scale_image(pygame.image.load("ASSETS/OBJECTS/mjolnir.png"), 2),
     'health'   : re_scale_image(pygame.image.load("ASSETS/OBJECTS/health.png"), 2),
}