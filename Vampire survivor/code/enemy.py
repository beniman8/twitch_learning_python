from settings import *
from groups import *


class Enemy(pygame.sprite.Sprite):
    
    
    def __init__(self,pos,frames,groups,player,collision_sprites):
        super().__init__(groups)
        self.player = player
        self.distance=0
        
        # image
        self.frames , self.frame_index = frames , 0
        self.image =self.frames[self.frame_index]
        self.animation_speed = 6
        
        
        # rect 
        self.rect =self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-20,-40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 200
        
        #timer 
        self.death_time =0
        self.death_duration = 200    
        
             
    def animate(self,dt):
        self.frame_index += self.animation_speed * dt 
        self.image = self.frames[int(self.frame_index) % len(self.frames)]


    # def move(self,dt):
    #     #player_enemy_distance = pygame.Vector2()
    #     '''
    #     vector. distance = player_vector.distance_to(enemy_vector) print("Distance:", distance)
    #     '''
    #     # get direction
    #     player_pos = pygame.Vector2(self.player.rect.center)
    #     enemy_pos = pygame.Vector2(self.rect.center)
    #     distance = enemy_pos.distance_to(player_pos)
        
    #     self.direction = (player_pos - enemy_pos).normalize()
        
        
    def move(self,dt): 
        player_pos = pygame.Vector2(self.player.rect.center) 
        enemy_pos = pygame.Vector2(self.rect.center) 
        distance = enemy_pos.distance_to(player_pos) 
        
        if distance <= 400: 
            self.direction = (player_pos - enemy_pos).normalize()
        else:
            self.direction = pygame.Vector2(0,0)
            
        
        # update the rect position + collision
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center
        
        
    def collision(self,direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    elif self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    elif self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
    
    def destroy(self):
        self.death_time =pygame.time.get_ticks()
        
        surf = pygame.mask.from_surface(self.frames[0]).to_surface()
        surf.set_colorkey('black')
        self.image = surf
        
    def death_timer(self):
        current_time = pygame.time.get_ticks() 
        if current_time - self.death_time >= self.death_duration:
            self.kill()
        
        
    def update(self, dt):
        if self.death_time == 0:
            self.move(dt)
            self.animate(dt)
        else:
            self.death_timer()