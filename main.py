from os import listdir
import random
import math
import pygame
from os.path import isfile, join
from player import Player
from object import Object
from block import Block

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

def get_block(size):
    path = './assets/terrain/Terrain.png'
    image = pygame.image.load(path).convert_alpha() 
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
    
def get_background(name):
    image = pygame.image.load('./assets/background/Pink.png')
    _, _, width, height = image.get_rect()
    tiles = []
    
    for i in range(WIDTH//width+1):
        for j in range(HEIGHT//height+1):
            pos = (i*width, j*height)
            tiles.append(pos)
            
    return tiles, image
    
def draw(window, bg, bg_image, player, objects, offset_x):
    for tile in bg:
        window.blit(bg_image, tile)
        
    for object in objects:
        object.draw(window, offset_x)
        
    player.draw(window, offset_x)
    
    pygame.display.update()
    
    
def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
                
        collided_objects.append(obj)
        
    return collided_objects 

def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break
        
    player.move(-dx, 0)
    player.update()
    return collided_object
    
def handle_move(player, objects):
    keys = pygame.key.get_pressed()
    
    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL*2)
    collide_right = collide(player, objects, PLAYER_VEL*2)
    
    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)
        
    handle_vertical_collision(player, objects, player.y_vel)

def main(window):
    clock = pygame.time.Clock()
    bg, bg_image = get_background('Pink.png')
    sprites = load_sprite_sheets('player', 'PinkMan', 32, 32, True)
    block_size = 96
    player = Player(100, 100, 50, 50, sprites)
    floor = [Block(i*block_size, HEIGHT - block_size, block_size, get_block) 
             for i in range(-WIDTH//block_size, (WIDTH*2)//block_size)]
    objects = [*floor, Block(0, HEIGHT - block_size*2, block_size, get_block), 
               Block(block_size*3, HEIGHT - block_size*4, block_size, get_block)]
    
    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.jump_count < 2:
                    player.jump()
            
        player.loop(FPS)
        handle_move(player, objects)  
        draw(window, bg, bg_image, player, objects, offset_x) 
        
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or ( 
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel   

    pygame.quit()
    quit()


if __name__ == "__main__": # forces entry point
    main(window)