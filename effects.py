import pygame,math
import random

class particles:
    def __init__(self,pos: tuple):
        self.rect = pygame.Rect((pos),(10,10))
        self.pos = pos
        self.velocity = pygame.math.Vector2(0,3)
        self.velocity = self.velocity.rotate(random.randint(0,180))
        self.frames = 0
    def update(self,surface):
        if (self.frames == 20):
            return False
        self.frames += 1
        self.rect = self.rect.move(self.velocity)
        pygame.draw.rect(surface,(250,250,250),self.rect)
        return True