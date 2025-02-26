from settings import *


class Player(pygame.sprite.Sprite):
    
    def __init__(self,surf,pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)

# imports 
player_path = join("images","player","down","0.png")
player_surf = pygame.image.load(player_path).convert_alpha()

# Groups 

all_sprite = pygame.sprite.Group()

player = Player(player_surf,(WINDOW_WIDTH/2,WINDOW_HEIGHT/2),all_sprite)

class Game:
    
    def __init__(self):
        #General
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption("Vampire Survivor")
        self.running = True 
        self.clock = pygame.time.Clock()
        
        self.run_game()
        
        
    def run_game(self):
        
        while self.running:
            dt = self.clock.tick() / 1000
            
            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running= False
                    
                    
            # draw the game
            
            self.display_surface.fill("red")
            #all_sprite.draw(self.display_surface)
            
            pygame.display.update()
            
            
        pygame.quit()
        
if __name__ == "__main__":
    game = Game()
    game.run_game()
            
        
        
