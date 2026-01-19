import pygame
import random


class particles:
    def __init__(self,rect:pygame.Rect,dir:int=1):
        self.rect = rect  #pygame.Rect((self.pos),(4,4))
        self.pos = list(rect.topleft)
        self.velocity = [round(random.uniform(0.5,1),2)*dir,round(random.uniform(-1,1),2)]
        self.frames = 0
    def explode(self,surface):
        if (self.frames >= 15):
            return False
        self.frames += 1
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.rect.topleft = self.pos
        pygame.draw.rect(surface,(250,250,250),self.rect)
        return True
    
    def rain(self,surface):
        if self.pos[1] > -20 and self.pos[1] < surface.get_height()+20:
            self.pos[1] += 2
        else:
            return False
        self.rect.topleft = self.pos
        pygame.draw.rect(surface,(250,250,250),self.rect)
        return True
    
    def reset(self):
            self.pos = [random.randint(100,700),-10]
        