from os import listdir
import random
import math
import pygame
from os.path import isfile, join
from player import Player

pygame.init()

pygame.display.set_caption('Platformer')

BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 1000, 800

FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join('assets', dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]
    
    all_sprites = {}
    
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        
        sprites = []
        for i in range(sprite_sheet.get_width()//width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i*width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
            
        if direction:
            all_sprites[image.replace('.png', '')+'_right'] = sprites
            all_sprites[image.replace('.png', '')+'_left'] = flip(sprites)
        else:
            all_sprites[image.replace('.png', '')] = sprites
            
    return all_sprites

def get_background(name):
    image = pygame.image.load('./assets/background/Pink.png')
    _, _, width, height = image.get_rect()
    tiles = []
    
    for i in range(WIDTH//width+1):
        for j in range(HEIGHT//height+1):
            pos = (i*width, j*height)
            tiles.append(pos)
            
    return tiles, image
    
def draw(window, bg, bg_image, player):
    for tile in bg:
        window.blit(bg_image, tile)
        
    player.draw(window)
    
    pygame.display.update()
    
def handle_move(player):
    keys = pygame.key.get_pressed()
    
    player.x_vel = 0
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)

def main(window):
    clock = pygame.time.Clock()
    bg, bg_image = get_background('Pink.png')
    sprites = load_sprite_sheets('player', 'PinkMan', 32, 32, True)
    player = Player(100, 100, 50, 50, sprites)

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
          
        player.loop(FPS)
        handle_move(player)  
        draw(window, bg, bg_image, player)    

    pygame.quit()
    quit()


if __name__ == "__main__": # forces entry point
    main(window)