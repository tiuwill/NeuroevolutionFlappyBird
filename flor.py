import pygame

class Flor(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("assets/sprites/base.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.y = 512 - self.rect.h