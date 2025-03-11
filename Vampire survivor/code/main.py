from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from enemy import *
from groups import AllSprites

from random import randint,choice


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
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        
        
        

        #gun timer 
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100
        
        #enemy timer 
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event,500)
        self.spawn_positions = []
        
        # audio
        self.shoot_sound= pygame.mixer.Sound(join('audio','shoot.wav'))
        self.shoot_sound.set_volume(0.2)
        
        self.impact_sound= pygame.mixer.Sound(join('audio','impact.ogg'))
        self.impact_sound.set_volume(0.2)
        
        
        self.music= pygame.mixer.Sound(join('audio','music.wav'))
        self.music.set_volume(0.05)
        self.music.play(loops=-1)
        
        # setup
        self.load_images()
        self.load_map()
        
        
        
        # run the game
        self.run_game()
        
    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images','gun','bullet.png')).convert_alpha()
        folders  = list(walk(join('images','enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path,_,files_names  in walk(join('images','enemies',folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(files_names,key = lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path,file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)
                    
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
                self.gun = Gun(self.player,self.all_sprite)
            else:
                self.spawn_positions.append((obj.x,obj.y))
                
    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet,self.enemy_sprites,False,pygame.sprite.collide_mask)
                if collision_sprites:
                    for sprite in collision_sprites:
                        sprite.destroy()
                        self.impact_sound.play()
                    bullet.kill()
                    
    def player_collision(self):
        if pygame.sprite.spritecollide(self.player,self.enemy_sprites,False,pygame.sprite.collide_mask):
            self.running = False
        
        
    def input(self):
        '''checking for game inputs'''
        #left mouse button is clicked and the shooting is available
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 50
            self.shoot_sound.play()
            Bullet(self.bullet_surf,pos,self.gun.player_direction,(self.all_sprite,self.bullet_sprites))
            self.can_shoot = False 
            self.shoot_time = pygame.time.get_ticks()
            
    def gun_timer(self):
        '''resetting the gun timer'''
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True 
            
            
    def run_game(self):
        '''Game loop : run the game loop'''

        while self.running:
            dt = self.clock.tick() / 1000

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running= False
                if event.type == self.enemy_event:
                    Enemy(choice(self.spawn_positions),choice(list(self.enemy_frames.values())),(self.all_sprite,self.enemy_sprites),self.player,self.collision_sprites)
                
            
            #update all sprites
            self.gun_timer()
            self.input()
            self.all_sprite.update(dt)
            self.bullet_collision()
            self.player_collision()


            # draw the game

            self.display_surface.fill("black")
            self.all_sprite.draw(self.player.rect.center)

            #updating game
            pygame.display.update()


        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run_game()



