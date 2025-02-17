import pygame
from os.path import join
from random import randint 
# General Setup
pygame.init()
WINDOW_WIDTH , WINDOW_HEIGHT = 1280 ,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Spaceship Game')
running = True


# plain Surface 
surf = pygame.Surface((100,200))
surf.fill('red')

# import an image 
path = join('images','player.png')
star_path = join('images','star.png')

player_surf = pygame.image.load(path).convert_alpha()
star_surf = pygame.image.load(star_path).convert_alpha()
star_positions = [(randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)) for i in range(20)]
x = 100

while running:
    # event loop 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    # draw the game  
    display_surface.fill('dark grey')
    x += 0.1
    
    for pos in star_positions:
        display_surface.blit(star_surf,pos)
    
    display_surface.blit(player_surf,(x,150))
    pygame.display.update()

pygame.quit()