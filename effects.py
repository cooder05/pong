import pygame,math
import random

class particles:
    def __init__(self,pos: tuple,dir:int):
        self.rect = pygame.Rect((pos),(5,5))
        self.pos = pos
        self.velocity = [random.randint(1,10)/10 - dir,random.randint(1,20)/10 - 1]
        self.frames = 0
    def update(self,surface):
        if (self.frames == 15):
            return False
        self.frames += 1
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        pygame.draw.rect(surface,(250,250,250),self.rect)
        return True