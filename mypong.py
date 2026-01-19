import pygame,math,random
from sys import exit
from effects import particles

pygame.init()

screen_width = 700
screen_height = 400
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')
test_font = pygame.font.Font(None,50)
test_sound = pygame.mixer.Sound("10844.mp3")
test_sound2 = pygame.mixer.Sound("10676.mp3")
pygame.mixer.music.load("Themepong.mp3")
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()
clock2 = pygame.time.Clock()
view ="start"
waiting = bool
wait_start = 0
cooldown = 1

class paddle():
    def __init__(self, mykeys = [pygame.K_DOWN,pygame.K_UP] ,player = False, left = True):
        
        self.y_offset = screen_height/10
        self.pos = [10+(screen_width-30)*(not left),screen_height/2 - self.y_offset]
        self.rect = pygame.Rect(self.pos,(10,screen_height/5))
        self.speed = 5
        self.player = player
        self.mykeys = mykeys


    def move(self,ball_pos = [0,0]):
        if self.player:
            keys = pygame.key.get_pressed()
            if keys[self.mykeys[0]] and self.rect.bottom <= screen_height:
                self.pos[1] += self.speed
            elif keys[self.mykeys[1]] and self.rect.top >= 0:
                self.pos[1] -= self.speed
        
        else:
            if ball_pos [1] - self.y_offset >= 0 and ball_pos[1] + self.y_offset <= screen_height and ball_pos[0] >= screen_width/2:
                self.pos[1] += math.floor((ball_pos[1] - self.rect.centery)*0.08) #moves to the ball

        self.rect = pygame.Rect(self.pos,(10,screen_height/5))

    def draw(self,surface):
        pygame.draw.rect(surface,(225,225,225),self.rect)

    def setplayer(self,ck):
        self.player = True
        self.mykeys = ck

class ball():
    def __init__(self,side):
        #creating self.pos create unsessary ovrehead of kepping
        # it updated with tha actual rect pos hence it is advise to not use it
        # abd just update the rect pos directly
        #self.pos = [screen_width/2,screen_height/2]
        self.rect = pygame.Rect((screen_width/2,screen_height/2),(20,20))
        if side == 1:
            self.speed_x = random.randint(1,4)
        else:
            self.speed_x = random.randint(-4,-1)
        self.speed_y = random.randint(-4,4)

    def move(self,paddles):
        global boom
        global s1,s2,view
        if self.rect.left <=0:
            s2 += 1
            self.__init__(-1)
            
        if self.rect.right >= screen_width:
            s1 += 1
            self.__init__(+1)
        
        if s1 == 5 or s2 ==5:
            view = "end"
        
        newpos = self.rect.move(0,self.speed_y)
        if newpos.top <= 0 or newpos.bottom >= screen_height:
            self.speed_y = -self.speed_y
            
        for paddle in paddles:
            if newpos.colliderect(paddle) :
                newpos.y = paddle.bottom if newpos.top >= (paddle.centery) else paddle.top-newpos.h
                self.speed_y *= -1
                #self.speed_y += (self.rect.centery-paddle.centery)
        

        newpos = newpos.move(self.speed_x,0)
        if newpos.colliderect(paddles[0]) :
            newpos.left = paddles[0].right
            self.speed_x *= -1.1
            self.speed_x = math.fmod(self.speed_x,8)       #change '6' as it might set speed_x to zero
            self.speed_y += (self.rect.centery-paddles[0].centery)//25
            for _ in range(20):
                boom.append(particles(pygame.Rect((self.rect.center),(4,4))))
            test_sound.play()
        if newpos.colliderect(paddles[1]) :
            newpos.right = paddles[1].left
            self.speed_x *= -1.1
            self.speed_x = math.fmod(self.speed_x,8)
            self.speed_y += (self.rect.centery-paddles[1].centery)//25
            for _ in range(20):
                boom.append(particles(pygame.Rect((self.rect.center),(4,4)),-1))
            test_sound.play()
        
        self.rect = newpos
        
    def return_pos(self):
        return self.rect.center
        
    def draw(self,surface):
        pygame.draw.circle(surface,(225,225,225),(self.rect.centerx,self.rect.centery),10)


class btn:
    def __init__(self,text,v):
        self.text = text
        self.rect = pygame.Rect(0,0,0,0)
        self.surf = pygame.Surface((10,10))
        self.wave = v
        self.clicked = False
        
    def display(self,surface,pos =(0,0)):
        self.surf = test_font.render(self.text,True,(255,255,255),(100,100,255))
        self.rect = self.surf.get_rect(center = pos)
        self.hover()
        pygame.draw.rect(surface,(255,255,255),self.rect.inflate(10,10),5)
        surface.blit(self.surf,self.rect)

    def hover(self):
        self.rect.y += self.wave[1]
        self.wave = self.wave.rotate(5) 


    def run(self,type):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and self.clicked == False:
            test_sound2.play()
            self.clicked = True
        if not pygame.mouse.get_pressed()[0] and self.clicked:
            global view, players
            if type == "start1":
                players = 1
                view = "game"
                pygame.mixer.music.stop()
            elif type == "start2":
                players = 2
                view = "game"
                pygame.mixer.music.stop()
            elif type == "end":
                view = "start"
                pygame.mixer.music.play(-1)
            self.clicked = False
def display_text(text: str,surface,pos=(0,0),color = (255,255,255),bgcolor = (0,0,0)):
    text_surf = test_font.render(text,True,color)
    text_rect = text_surf.get_rect(center = pos)
    surface.blit(text_surf,text_rect)

Ball = ball(-1)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
p_1 = paddle([pygame.K_DOWN,pygame.K_UP],True)
players = 1
p_2 = paddle([pygame.K_s,pygame.K_w],False,False) 
s1,s2 = 0,0
b1 = btn("1 player",pygame.Vector2((0,5)))
b2 = btn("2 player",pygame.Vector2((0,-5)))
b3 = btn("main menu",pygame.Vector2((0,-5)))
powerup = particles(pygame.Rect(400,0,20,20))
boom= []
remove= []
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if view == "game":
        #game window
        surface.fill('black')
        if players == 1: 
            p_2.move(Ball.return_pos())
        elif players == 2 :
            p_1.setplayer([pygame.K_s,pygame.K_w])
            p_2.setplayer([pygame.K_DOWN,pygame.K_UP])
            players = 1
        p_1.move()
        Ball.move([p_1.rect,p_2.rect])

        for i in range(7):
            pygame.draw.line(surface,(255,225,225),(screen_width/2,screen_height*i/6+20),(screen_width/2,screen_height*i/6+50),2)
       
        p_2.draw(surface)
        p_1.draw(surface)
        Ball.draw(surface)
        for particle in boom:
            if not particle.explode(surface):
                boom.remove(particle)
                """remove.append(particle)
        for par in remove:
            boom.remove(par)
        remove.clear()
        """
        if not powerup.rain(surface):
            if not waiting:
                waiting = True
                wait_start = pygame.time.get_ticks()

        if waiting and pygame.time.get_ticks() - wait_start >= cooldown*1000:
            waiting = False
            powerup.reset()
            cooldown = random.randint(1,5)

        display_text(str(s1),surface,(screen_width/4,20))
        display_text(str(s2),surface,(3*screen_width/4,20))

    elif view == "start":
        s1,s2 = 0,0
        surface.fill((150,100,150))
        display_text("Pong",surface,(screen_width/2,screen_height/2 -100))
        
        b1.display(surface,(screen_width/2,screen_height/2))
        b1.run("start1")
        b2.display(surface,(screen_width/2,screen_height/2 + 80))
        b2.run("start2")
    elif view == "end":
        p_1.setplayer([pygame.K_DOWN,pygame.K_UP])
        p_2.player = False
        surface.fill((150,100,150))
        display_text("p1 won" if s1==5 else "p2 won",surface,(screen_width/2,screen_height/2 -100))
        b3.display(surface,(screen_width/2,screen_height/2))
        b3.run("end")
    screen.blit(surface,(0,0))
    pygame.display.update()
    clock.tick(60)
pygame.quit()