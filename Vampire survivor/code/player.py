from settings import *
from groups import *

class Player(pygame.sprite.Sprite):
    
    '''Class for the main player we are going to control'''

    def __init__(self,surf,pos, groups,collision_sprite):
        super().__init__(groups)
        self.load_images()
        self.state , self.frame_index ='down',0
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-60,-90)
        
        
        # movement
        self.direction = pygame.Vector2()
        self.speed = 500
        
        self.collision_sprite = collision_sprite
        
    def load_images(self):
        self.frames = {'left':[],'right':[],'up':[],'down':[]}
        
        for state in self.frames.keys():
            for folder_path,sub_folders,file_names in list(walk(join('images','player',state))):
                if file_names:
                    #sorted the list for safe guard incase the images do not show up in their respective orders
                    for file_name in sorted(file_names,key= lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path,file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)
        
        
    def input(self):
        '''The mechanics or inputs we are going to use in order to manipulate the player'''
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]  - keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s] - keys[pygame.K_UP] or keys[pygame.K_w])
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )

    
    def move(self,dt):
        ''' the actual movement that happens over time depending on the speed ,input and delta time'''
        
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        
        self.rect.center =self.hitbox_rect.center
        
    def collision(self,direction):
        '''We handel all the collision that happens to the player or gets done by the player here'''
        
        for sprite in self.collision_sprite:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    elif self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    elif self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
    
    def animate(self,dt):
        #get the state 
        if self.direction.x != 0:
            self.state='right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state='down' if self.direction.y > 0 else 'up'
        
        #this needs to be studied or understood clear time 5:19
        #animation 
        self.frame_index = self.frame_index + 5 * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
    def update(self, dt):
        
        self.input()
        self.move(dt)
        self.animate(dt)

        