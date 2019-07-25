import pygame
from random import randint
HEIGHT_BETWEEN_PIPES = 110
PIPE_DISTANCE = 250

class Pipe(pygame.sprite.Sprite):

    def __init__(self, reversed=False, start_x=0, start_y=0, velocity = 2):
        super().__init__()

        self.image = pygame.image.load("assets/sprites/pipe-green.png").convert_alpha()
        self.reversed = reversed
        if reversed:
            self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()

        self.start_x = start_x + self.rect.w
        self.start_y = start_y

        self.rect.x = self.start_x
        self.rect.y = self.start_y

        self.velocity = velocity

        self.stoped = False

    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        
    def move(self):
        if not self.stoped:
            self.rect.x -= self.velocity

    def stop(self):
        self.stoped = True
    
    def start(self):
        self.stoped = False

    def reset_position(self, up_pipe_y=0):
      if self.rect.x + self.rect.w < 0:
            self.rect.x = 350
            if up_pipe_y == 0:
                self.rect.y = randint(-240, -30)
            else:
                self.rect.y = up_pipe_y + HEIGHT_BETWEEN_PIPES + self.rect.h