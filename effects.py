import pygame
import random


class particles:
    def __init__(self,rect:pygame.Rect,dir:int=1):
        self.rect = rect  #pygame.Rect((self.pos),(4,4))
        self.pos = list(rect.topleft)
        self.velocity = [round(random.uniform(0.5,1),2)*dir,round(random.uniform(-1,1),2)]
        self.frames = 0
        self.alpha = 100
        self.collide = False
        self.tempsurf = pygame.Surface(self.rect.size,pygame.SRCALPHA).convert_alpha()
        self.tempsurf.fill((255, 255, 255,255))
    def explode(self,surface):
        if (self.frames >= 15):
            return False
        self.frames += 1
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.rect.topleft = self.pos
        self.draw(surface)
        return True
    
    def rain(self,surface):
        if self.pos[1] > -200 and self.pos[1] < surface.get_height()+20:
            self.pos[1] += 1
        else:
            return False
        self.rect.topleft = self.pos
        self.draw(surface)
        return True

    def fade(self,surface):
        if self.alpha > 0:
            self.alpha = max(0, self.alpha - 5)
            self.tempsurf.set_alpha(self.alpha)
            self.draw(self.tempsurf)
            surface.blit(self.tempsurf,self.rect)
            return True
        return False
    
    def reset(self):
            self.pos = [random.randint(100,700),-150]
            self.collide = False
    
    def draw(self,surface,pos=None):
         if not self.collide:
            if pos:
                draw_rect = pygame.Rect(pos, self.rect.size)
            else:
                draw_rect = self.rect
            pygame.draw.rect(surface,(250,250,250),draw_rect)

    def collision(self,obj):
        if self.rect.colliderect(obj.rect):
            self.collide = True
            self.pos[1]=1000
              
        