from settings import *

class Player(pygame.sprite.Sprite):

    def __init__(self,surf,pos, groups,collision_sprite):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-60,0)
        
        # movement
        self.direction = pygame.Vector2()
        self.speed = 300
        
        self.collision_sprite = collision_sprite
        
        
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN] - keys[pygame.K_UP])
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )     
    
    def move(self,dt):
        
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        
        self.rect.center =self.hitbox_rect.center
        
    def collision(self,direction):
        
        for sprite in self.collision_sprite:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    def update(self, dt):
        
        self.input()
        self.move(dt)

        