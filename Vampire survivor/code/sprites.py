from settings import *


class Sprite(pygame.sprite.Sprite):
    ''' class for simple Sprite that just need to be displayed'''
    def __init__(self,pos,surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True

class CollisionSprite(pygame.sprite.Sprite):
    
    '''Class for the sprite that have or need collision'''
    
    def __init__(self,pos,surf, groups):
        super().__init__(groups)
        
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)