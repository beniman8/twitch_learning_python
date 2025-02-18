import pygame
from os.path import join
from random import randint 
# General Setup
pygame.init()
WINDOW_WIDTH , WINDOW_HEIGHT = 1280 ,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Spaceship Game')
running = True
clock = pygame.time.Clock()


# plain Surface 
surf = pygame.Surface((100,200))
surf.fill('red')

# imports
path = join('images','player.png')
star_path = join('images','star.png')
meteor_path = join('images','meteor.png')
laser_path = join('images','laser.png')


meteor_surf = pygame.image.load(meteor_path).convert_alpha()
laser_surf = pygame.image.load(laser_path).convert_alpha()
star_surf = pygame.image.load(star_path).convert_alpha()
player_surf = pygame.image.load(path).convert_alpha()

player_rect = player_surf.get_frect(center= (WINDOW_WIDTH / 2,WINDOW_HEIGHT/2))
meteor_rect = meteor_surf.get_frect(center=(WINDOW_WIDTH / 2,WINDOW_HEIGHT/2))
laser_rect = laser_surf.get_frect(bottomleft = (20,WINDOW_HEIGHT - 20))

star_positions = [(randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)) for i in range(20)]

player_direction = 1
while running:
    clock.tick(60)
    # event loop 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    # draw the game  
    display_surface.fill('dark grey')
    #x += 0.1
    
    for pos in star_positions:
        display_surface.blit(star_surf,pos)
    
    
    
    display_surface.blit(laser_surf,laser_rect)
    display_surface.blit(meteor_surf,meteor_rect)
    
    
    player_rect.x += player_direction *0.8
    if player_rect.right > WINDOW_WIDTH or player_rect.left < 0:
        player_direction *= -1
    display_surface.blit(player_surf,player_rect)
    

    
    pygame.display.update()

pygame.quit()