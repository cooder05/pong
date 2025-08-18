import pygame


class particles:
    def __init__(self,pos: tuple):
        self.rect = pygame.Rect((pos),(10,10))
        self.pos = pos

    def draw(self,surface):
        pygame.draw.rect(surface,(250,250,250),self.rect)