import pygame,math
import random

class particles:
    def __init__(self,pos: tuple,dir:int):
        self.pos = list(pos)
        self.rect = pygame.Rect((self.pos),(4,4))
        self.velocity = [round(random.uniform(0,0.5),2)*dir,round(random.uniform(0,2),2)- 1]
        self.frames = 0
    def update(self,surface):
        if (self.frames == 15):
            return False
        self.frames += 1
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.rect.topleft = self.pos
        pygame.draw.rect(surface,(250,250,250),self.rect)
        return True