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

player_direction = pygame.math.Vector2()
player_speed = 300
while running:
    dt = clock.tick() / 1000
    
    # event loop 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
        #     print(1)
        # if event.type == pygame.MOUSEMOTION:
        #     player_rect.center = event.pos

    #input / controls
    
    keys = pygame.key.get_pressed()
    player_direction.x = int(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
    player_direction.y = int(keys[pygame.K_DOWN] - keys[pygame.K_UP])
    player_direction = player_direction.normalize() if player_direction else player_direction
    player_rect.center += player_direction * player_speed * dt
    
    
    # space
    recent_key = pygame.key.get_just_pressed()
    if recent_key[pygame.K_SPACE]:
        print('fire laser')
    
    
    # draw the game  
    display_surface.fill('dark grey')
    #x += 0.1
    
    for pos in star_positions:
        display_surface.blit(star_surf,pos)
    
    
    
    display_surface.blit(laser_surf,laser_rect)
    display_surface.blit(meteor_surf,meteor_rect)
    
    
    player_rect.center += player_direction * player_speed * dt
    

    
    display_surface.blit(player_surf,player_rect)
    

    
    pygame.display.update()

pygame.quit()