import pygame
from background import Background
from bird import Bird
from pipe import Pipe
from flor import Flor
import copy
from random import randint

HEIGHT_BETWEEN_PIPES = 110

class Game():

    def __init__(self, game_width, game_height, pipe_distance, n_birds=1):
        
        self.game_width = game_width
        self.game_height = game_height

        self.pipe_distance = pipe_distance
        self.screen = self.init_screen()

        self.front_sprites = pygame.sprite.Group()
        self.middle_sprites = pygame.sprite.Group()


        self.n_birds = n_birds
        self.killed_birds = []

        self.birds = []
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.init_bird()
        self.init_pipes()
        self.init_flor()

        
        self.score_label = pygame.font.SysFont("monospace", 20)

        self.game_objects = self.get_game_objects()
        
        self.front_pipes = self.get_front_pipes()


    def init_bird(self):
        for i in range(self.n_birds):
            bird = Bird()
            self.birds.append(bird)
            self.middle_sprites.add(bird)       
    
    def init_flor(self):
        self.flor = Flor()
        self.front_sprites.add(self.flor)

    def init_pipes(self):
        
        self.pipe_up = Pipe(reversed=True, start_x = 288, start_y = randint(-240, -30))
        self.pipe_bottom = Pipe(start_x = 288, start_y = self.pipe_up.rect.y + HEIGHT_BETWEEN_PIPES + self.pipe_up.rect.h)

        self.pipe_up2 = Pipe(reversed=True, start_x= 288 + self.pipe_distance, start_y= randint(-240, -30))
        self.pipe_bottom2 = Pipe(start_x = 288 + self.pipe_distance, start_y = self.pipe_up2.rect.y + HEIGHT_BETWEEN_PIPES + self.pipe_up2.rect.h)
        
       
        self.middle_sprites.add(self.pipe_bottom)
        self.middle_sprites.add(self.pipe_up)

        self.middle_sprites.add(self.pipe_bottom2)
        self.middle_sprites.add(self.pipe_up2)

    def init_screen(self):
        pygame.init()
        screen = pygame.display.set_mode((self.game_width, self.game_height))
        pygame.display.set_caption("Flappy bird")
        return screen

    def get_game_objects(self):
        return [
                self.pipe_bottom, 
                self.pipe_up, 
                self.pipe_bottom2, 
                self.pipe_up2, 
                self.flor
            ]

    def tick(self,tick_number):
        self.clock.tick(tick_number)

    def get_front_pipes(self):
        return [self.pipe_bottom, self.pipe_up]

    def reset(self):
        for bird in self.birds:
            bird.reset()
            bird.stop()

        self.pipe_bottom.reset()
        self.pipe_bottom.stop()
        self.pipe_up.reset()
        self.pipe_up.stop()
        self.pipe_bottom2.reset()
        self.pipe_bottom2.stop()
        self.pipe_up2.reset()
        self.pipe_up2.stop()
        self.front_pipes = self.get_front_pipes()
        

    def move_pipes(self):
        self.pipe_bottom.move()
        self.pipe_up.move()

        self.pipe_up.reset_position()
        self.pipe_bottom.reset_position(up_pipe_y=self.pipe_up.rect.y)

        self.pipe_bottom2.move()
        self.pipe_up2.move()

        self.pipe_up2.reset_position()
        self.pipe_bottom2.reset_position(up_pipe_y=self.pipe_up2.rect.y)

    def update_middle_sprites(self):
        self.middle_sprites.update()

    def update_front_sprites(self):
        self.front_sprites.update()
    
    def fill_game_screen(self):
        self.screen.fill([255,255,255])
        self.screen.blit(self.background.image, self.background.rect)

    def draw_front_sprites(self):
        self.front_sprites.draw(self.screen)
    
    def draw_middle_sprites(self):
        self.middle_sprites.draw(self.screen)

    #def render_score(self):
        #label = self.score_label.render(str(self.bird.score), 2, (255,255,0))
       # self.screen.blit(label, (100, 100))
    #   print('score')

    def start(self):
        for bird in self.birds:
            bird.start()
        self.pipe_bottom.start()
        self.pipe_up.start()
        self.pipe_bottom2.start()
        self.pipe_up2.start()

    def remove_bird(self, bird):
        self.birds.remove(bird)
        self.killed_birds.append(bird)
    
    def check_end_game(self):
        if len(self.birds) == 0:
            self.killed_birds.sort(key=lambda x:x.fitness, reverse=True)
            best_bird = self.killed_birds[0]
            self.new_population(best_bird)
            self.killed_birds = []
            self.reset()
            self.start()

    def new_population(self, best_bird):
        for i in range(self.n_birds):
            bird_nn = copy.deepcopy(best_bird.nn)
            new_bird = Bird(bird_nn)
            new_bird.mutate(0.1)
            self.middle_sprites.add(new_bird)
            self.birds.append(new_bird)
        

    def count_score(self):
        for bird in self.birds:
            if bird.pipes_passed(self.front_pipes):
                if self.front_pipes.count(self.pipe_bottom) > 0:
                    self.front_pipes = [self.pipe_bottom2, self.pipe_up2]
                else:
                    self.front_pipes = [self.pipe_bottom, self.pipe_up]