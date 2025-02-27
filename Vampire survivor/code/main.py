from settings import *
from player import Player
from sprites import *
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

        #sprites
        for i in range(6):
            x , y = randint(0,WINDOW_WIDTH) , randint(0,WINDOW_HEIGHT)
            w,h = randint(60,100) , randint(50,100)
            CollisionSprite(pos=(x,y),size=(w,h),groups=(self.all_sprite,self.collision_sprites))

        self.player = Player(self.player_surf,(WINDOW_WIDTH/2,WINDOW_HEIGHT/2),self.all_sprite,self.collision_sprites)
        
        # run the game
        self.run_game()


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



