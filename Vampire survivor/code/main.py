from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame

from groups import AllSprites

from random import randint


class Game:

    def __init__(self):
        #General Setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Survivor")
        self.running = True
        self.clock = pygame.time.Clock()

        # imports
        self.player_path = join("images","player","down","0.png")
        self.player_surf = pygame.image.load(self.player_path).convert_alpha()

        # Groups
        self.all_sprite = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        
        self.load_map()

        #sprites

        # run the game
        self.run_game()
        
    def load_map(self):
        ''' Load the map and the items in the map'''
        
        map = load_pygame(join('data','maps','world.tmx'))
        
        for x ,y , image in map.get_layer_by_name('Ground').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE),image,self.all_sprite)
        
        for  obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x,obj.y),obj.image,(self.all_sprite,self.collision_sprites))
            
        for col in map.get_layer_by_name('Collisions'):
            CollisionSprite((col.x,col.y),pygame.Surface((col.width,col.height)),self.collision_sprites)
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == "Player":
                # create the player only when you find the entity named Player
                self.player = Player(self.player_surf,(obj.x,obj.y),self.all_sprite,self.collision_sprites)
        

    def run_game(self):
        '''Game loop : run the game loop'''

        while self.running:
            dt = self.clock.tick() / 1000

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running= False

            #update all sprites
            self.all_sprite.update(dt)


            # draw the game

            self.display_surface.fill("black")
            self.all_sprite.draw(self.player.rect.center)

            pygame.display.update()


        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run_game()



