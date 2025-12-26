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
    
    player = Player(100, 100, 50, 50)

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