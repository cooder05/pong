import pygame,math,random
from sys import exit

pygame.init()

screen_width = 700
screen_height = 400
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')
test_font = pygame.font.Font(None,50)
clock = pygame.time.Clock()
view ="start" 

class paddle():
    def __init__(self, player = False):
        
        self.y_offset = screen_height/20
        self.pos = [10+(screen_width-30)*(not player),screen_height/2 - self.y_offset]
        self.rect = pygame.Rect(self.pos,(10,screen_height/5))
        self.speed = 5
        self.player = player


    def move(self,ball_pos = [0,0]):
        if self.player:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN] and self.rect.bottom <= screen_height:
                self.pos[1] += self.speed
            elif keys[pygame.K_UP] and self.rect.top >= 0:
                self.pos[1] -= self.speed
        
        else:
            if ball_pos [1] - self.y_offset >= 0 and ball_pos[1] + self.y_offset <= screen_height and ball_pos[0] >= screen_width/2:
                self.pos[1] += (ball_pos[1] - self.rect.centery)*0.04

        self.rect = pygame.Rect(self.pos,(10,screen_height/5))

    def draw(self,surface):
        pygame.draw.rect(surface,(225,225,225),self.rect)

class ball():
    def __init__(self):
        #creating self.pos create unsessary ovrehead of kepping
        # it updated with tha actual rect pos hence it is advise to not use it
        # abd just update the rect pos directly
        #self.pos = [screen_width/2,screen_height/2]
        self.rect = pygame.Rect((screen_width/2,screen_height/2),(20,20))
        self.speed_x = random.randint(1,4)
        self.speed_y = random.randint(-4,4)

    def move(self,paddles):
        global s1,s2,view
        if self.rect.left <=0:
            s2 += 1
            self.__init__()
            
        if self.rect.right >= screen_width:
            s1 += 1
            self.__init__()
        
        
        newpos = self.rect.move(0,self.speed_y)
        if newpos.top <= 0 or newpos.bottom >= screen_height:
            self.speed_y = -self.speed_y
            
        for paddle in paddles:
            if newpos.colliderect(paddle) :
                newpos.y = paddle.bottom if newpos.top >= (paddle.centery) else paddle.top-newpos.h
                self.speed_y *= -1
        

        newpos = newpos.move(self.speed_x,0)
        if newpos.colliderect(paddles[0]) :
            newpos.left = paddles[0].right
            self.speed_x *= -1.1
            self.speed_x %= 10
            self.speed_x = math.floor(self.speed_x)
        if newpos.colliderect(paddles[1]) :
            newpos.right = paddles[1].left
            self.speed_x *= -1.1
            self.speed_x %= -10
            self.speed_x = math.floor(self.speed_x)
        
        self.rect = newpos
        
    def return_pos(self):
        return self.rect.center
        
    def draw(self,surface):
        pygame.draw.circle(surface,(225,225,225),(self.rect.centerx,self.rect.centery),10)


class btn:
    def __init__(self,text):
        self.text = text
        self.rect = pygame.Rect(0,0,0,0)
        self.surf = pygame.Surface((10,10))
        self.wave = pygame.Vector2((0,5))
        
    def display(self,surface,pos =(0,0)):
        self.surf = test_font.render(self.text,True,(255,255,255),(100,100,255))
        self.rect = self.surf.get_rect(center = pos)
        self.hover()
        pygame.draw.rect(surface,(255,255,255),self.rect.inflate(10,10),5)
        surface.blit(self.surf,self.rect)

    def hover(self):
        self.rect.y += self.wave[1]
        self.wave = self.wave.rotate(5) 


    def run(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            global view
            view = "game"


def display_text(text: str,surface,pos=(0,0),color = (255,255,255),bgcolor = (0,0,0)):
    text_surf = test_font.render(text,True,color)
    text_rect = text_surf.get_rect(center = pos)
    surface.blit(text_surf,text_rect)

Ball = ball()
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
player = paddle(True)
enemy_paddle = paddle() 
s1,s2 = 0,0
button = btn("single player")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            button.run()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Ball.__init__()
                player.__init__(True)
                enemy_paddle.__init__()
                view = "start"       

    if view == "game":
    #game window
        surface.fill('black')

        enemy_paddle.move(Ball.return_pos())
        player.move()
        Ball.move([player.rect,enemy_paddle.rect])

        pygame.draw.line(surface,(225,225,225),(screen_width/2,0),(screen_width/2,screen_height),2)
        
        enemy_paddle.draw(surface)
        player.draw(surface)
        Ball.draw(surface)
        display_text(str(s1),surface,(screen_width/4,20))
        display_text(str(s2),surface,(3*screen_width/4,20))

        screen.blit(surface,(0,0))
    elif view == "start":
        surface.fill((150,100,150))
        display_text("Pong",surface,(screen_width/2,screen_height/2 -100))
        button.display(surface,(screen_width/2,screen_height/2))

        screen.blit(surface,(0,0))
    pygame.display.update()
    clock.tick(60)
pygame.quit()