import pygame
from random import randint
from neuralnetwork import NeuralNetwork

V = 8

class Bird(pygame.sprite.Sprite):

   
    def __init__(self, nn=None):
        super().__init__()
        
        self.image = pygame.image.load("assets/sprites/redbird-midflap.png").convert_alpha()
        self.rect = self.image.get_rect()
        # Stores if player is jumping or not.
        self.isjump = 0     
        self.score = 0

        self.fitness = 0

        if nn != None:
          self.nn = nn
        else:
          self.nn = NeuralNetwork(5,8,2)

        #bird position
        self.rect.x = 144
        self.rect.y = randint(120, 200)

        self.falling = pygame.image.load("assets/sprites/redbird-downflap.png").convert_alpha()
        self.jumping = pygame.image.load("assets/sprites/redbird-upflap.png").convert_alpha()
        # Force (v) up and mass m.
        self.v = V
        self.m = 1

        self.stopped = False
    
    def increment_fitness(self):
        self.fitness+=1

    def reset(self):
        self.rect.x = 144
        self.rect.y = randint(0, 250)
        self.score = 0 
        
    def jump(self):
        if not self.stopped:
            self.g = 0
            self.start_point = self.rect.y
            self.v = V
            self.isjump = 1
            self.update()

    def not_jumping(self):
        return self.isjump != 1

    def is_collided_with(self, objects):
        for object in objects:
            if self.rect.colliderect(object.rect):
                self.kill()
                return True
            if(self.rect.y < 0 or self.rect.y > 512):
                self.kill()
                return True
        return False
    
    def pipes_passed(self, pipes):
        pipe = pipes[0]
        if (pipe.rect.x + pipe.rect.w) < self.rect.x:
            self.score += 1
            return True
        return False

    def stop(self):
        self.stopped = True
    
    def start(self):
        self.stopped = False

    def think(self, pipe_x, pipe_y, pipe2_y):
        predction = self.nn.predict([pipe_x, 
                            pipe_y, 
                            pipe2_y, 
                            self.rect.y/512,
                            self.v/8])
        if predction[0][0] > predction[0][1]:
            self.jump()

    def update(self):
        if not self.stopped:
            # Calculate force (F). F = 0.5 * mass * velocity^2.
            if self.v > 0:
                F = ( 0.08 * self.m * (self.v*self.v) )
            else:
                F = -( 0.08 * self.m * (self.v*self.v) )
    
            # Change position
            self.rect.y = self.rect.y - F

            # Change velocity
            self.v = self.v - 0.7

    def mutate(self, rate):
        self.nn.mutate(rate)
