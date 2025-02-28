from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame

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
        self.all_sprite = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        
        self.setup()

        #sprites
        self.player = Player(self.player_surf,(500,300),self.all_sprite,self.collision_sprites)
        
        # run the game
        self.run_game()
        
    def setup(self):
        map = load_pygame(join('data','maps','world.tmx'))
        
        for x ,y , image in map.get_layer_by_name('Ground').tiles():
            Sprite((x*TILE_SIZE,y*TILE_SIZE),image,self.all_sprite)
        
        for  obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x,obj.y),obj.image,(self.all_sprite,self.collision_sprites))
            
        for col in map.get_layer_by_name('Collisions'):
            CollisionSprite((col.x,col.y),pygame.Surface((col.width,col.height)),self.collision_sprites)
            


    def run_game(self):

        while self.running:
            dt = self.clock.tick() / 1000

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running= False

            #update all sprites
            self.all_sprite.update(dt)


            # draw the game

            self.display_surface.fill("red")
            self.all_sprite.draw(self.display_surface)

            pygame.display.update()


        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run_game()



