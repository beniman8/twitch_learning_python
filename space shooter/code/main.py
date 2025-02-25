import pygame
from os.path import join
from random import randint, uniform

# General Setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Spaceship Game")
running = True
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):

    def __init__(self, *groups):
        super().__init__(*groups)
        self.original_surf = pygame.image.load(path).convert_alpha()
        self.image = self.original_surf
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300

        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400



    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN] - keys[pygame.K_UP])
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )
        self.rect.center += self.direction * self.speed * dt

        # shooting mechanism
        recent_key = pygame.key.get_just_pressed()
        if recent_key[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()
        


class Star(pygame.sprite.Sprite):
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(
            center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))
        )


class Laser(pygame.sprite.Sprite):

    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)


    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom == 0:
            self.kill()


class Meteor(pygame.sprite.Sprite):

    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = self.original_surf
        self.rect = self.image.get_frect(center=pos)
        self.created_time = pygame.time.get_ticks()
        self.death_time = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)
        self.rotation_speed = randint(20,50)
        self.rotation = 0


    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.created_time >= self.death_time:
            self.kill()
        
        # continuous rotation 
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf,self.rotation,1)
        self.rect = self.image.get_frect(center = self.rect.center)


def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time),True,(240,240,240))
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2,WINDOW_HEIGHT -50))
    display_surface.blit(text_surf,text_rect)
    pygame.draw.rect(display_surface,'red',text_rect.inflate(20,10).move(0,-8),3,10)
def collision():
    global running
    collided_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True,pygame.sprite.collide_mask)

    if collided_sprites:
        running = False
        
    for laser in laser_sprites:

        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()


# plain Surface
surf = pygame.Surface((100, 200))
surf.fill("red")

# imports
path = join("images", "player.png")
star_path = join("images", "star.png")
meteor_path = join("images", "meteor.png")
laser_path = join("images", "laser.png")
font = pygame.font.Font(join("images", "Oxanium-Bold.ttf"),40)
text_surf = font.render('text',True,(255,255,255))


# surface
star_surf = pygame.image.load(star_path).convert_alpha()
laser_surf = pygame.image.load(laser_path).convert_alpha()
meteor_surface = pygame.image.load(meteor_path).convert_alpha()
# groups
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()


for i in range(20):
    Star(star_surf, all_sprites)

player = Player(all_sprites)
player_direction = pygame.math.Vector2()
player_speed = 300

# custom event - > meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor(meteor_surface, (x, y), (all_sprites, meteor_sprites))

    all_sprites.update(dt)

    # collision
    collision()

    # draw the game
    display_surface.fill("#3a2e3f")

    all_sprites.draw(display_surface)
    display_score()
    
    
    #draw test rect(surface, color, rect, width=0, border_radius=0, border_top_left_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1, border_bottom_right_radius=-1)
   

    pygame.display.update()

pygame.quit()
