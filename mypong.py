import pygame,math,random
from sys import exit
from effects import particles

pygame.init()

screen_width = 1000
screen_height = 500
WHITE = (255,255,255)
GRAY = (150,150,150)
BLACK = (0,0,0)
screen = pygame.display.set_mode((screen_width,screen_height),pygame.SCALED)
#screen_width, screen_height = screen.get_size()
pygame.display.set_caption('Pong')
test_font = pygame.font.Font(None,50)
bounce_sound = pygame.mixer.Sound("10844.mp3")
click_sound = pygame.mixer.Sound("10676.mp3")
pygame.mixer.music.load("Themepong.mp3")
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()
clock2 = pygame.time.Clock()
view ="start"
waiting = False
wait_start = 0
cooldown = 1
display_modes = pygame.display.list_modes()[15:17]
display_modes.append((screen_width,screen_height))
new_display_modes = []
for i in display_modes:
    i = (i,test_font.render(str(i),True,WHITE,BLACK))
    new_display_modes.append(i)

class paddle():
    def __init__(self, mykeys = [pygame.K_DOWN,pygame.K_UP] ,player = False, left = True):
        
        self.y_offset = screen_height/10
        self.pos = [10+(screen_width-30)*(not left),screen_height/2 - self.y_offset]
        self.rect = pygame.Rect(self.pos,(10,70))
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

        self.rect = pygame.Rect(self.pos,(self.rect.w,self.rect.h))

    def draw(self,surface):
        pygame.draw.rect(surface,(225,225,225),self.rect)

    def setplayer(self,ck):
        self.player = True
        self.mykeys = ck

class ball():
    def __init__(self,side):
        #creating self.pos create unsessary ovrehead but usefull in some cases on in the Ball class below
        # it updated with tha actual rect pos hence it is advise to not use it
        # abd just update the rect pos directly
        #self.pos = [screen_width/2,screen_height/2]
        self.rect = pygame.Rect((screen_width/2,screen_height/2),(20,20))
        self.trailarr =[]
        if side == 1:
            self.speed_x = random.randint(2,4)
        else:
            self.speed_x = random.randint(-4,-2)
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
        for p in paddles:
            if newpos.colliderect(p):
                side = 1 if newpos.centerx >p.centerx else -1
                self.speed_x *= -1
                self.speed_x = math.fmod(self.speed_x,8)
                self.speed_x += side*2
                self.speed_y += (self.rect.centery-p.centery)//20
                if side > 0:
                    newpos.left = p.right
                else:
                    newpos.right = p.left
                for _ in range(20):
                    boom.append(particles(pygame.Rect((self.rect.center),(4,4)),side))
                bounce_sound.play()
        
        self.rect = newpos
        
    def return_pos(self):
        return self.rect.center
        
    def draw(self,surface):
        self.trailarr.append(particles(pygame.Rect((self.rect.centerx-2,self.rect.centery-2),(5,5))))
        for e in self.trailarr:
            if not e.fade(surface):
                self.trailarr.remove(e)
        pygame.draw.circle(surface,(225,225,225),(self.rect.centerx,self.rect.centery),10)


class btn:
    def __init__(self,text,v,percent=100):
        self.text = text
        self.rect = pygame.Rect(0,0,0,0)
        self.surf = pygame.Surface((10,10))
        self.wave = v
        self.clicked = False
        self.percent = percent
        self.dropped = False
        
    def display(self,surface,pos =(0,0)):
        self.tsurf = test_font.render(self.text,True,WHITE,BLACK)
        self.rect = self.tsurf.get_rect(center = pos)
        #self.hover()
        pygame.draw.rect(surface,WHITE,self.rect.inflate(10,10),5)
        surface.blit(self.tsurf,self.rect)

    def hover(self):
        self.rect.y += self.wave[1]
        self.wave = self.wave.rotate(5)

    def run(self,type):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            mouse_pressed = pygame.mouse.get_pressed()[0]
            if mouse_pressed and not self.clicked:
                click_sound.play()
                self.clicked = True
            elif self.clicked:
                global view, players
                if type == "start1":
                    players = 1
                    view = "game"
                    pygame.mixer.music.stop()
                elif type == "start2":
                    players = 2
                    view = "game"
                    pygame.mixer.music.stop()
                elif type == "set":
                    view = "settings"
                elif type == "end":
                    view = "start"
                    pygame.mixer.music.play(-1)
                self.clicked = False

    def slider(self,surface,pos =(0,0)):
        #self.tsurf = test_font.render(self.text+" "+str(math.floor(self.percent*100))+": ",True,WHITE,BLACK)
        self.tsurf = test_font.render(self.text,True,WHITE,BLACK)
        self.txtb = pygame.Rect((pos[0]-250,pos[1]),(250,self.tsurf.get_height()))
        self.rect = pygame.Rect(pos,(250,self.tsurf.get_height()))
        pygame.draw.line(surface,(150,150,150),(self.rect.left,self.rect.centery),(self.rect.right,self.rect.centery),8)
        pygame.draw.line(surface,WHITE,(self.rect.left,self.rect.centery),(self.rect.left+250*self.percent,self.rect.centery),4)
        pygame.draw.circle(surface,(200,200,200),(self.rect.left+250*self.percent,self.rect.centery+1),8)
        pygame.draw.circle(surface,WHITE,pos,3)
        #pygame.draw.rect(surface,WHITE,rect=self.rect,width=5)
        surface.blit(self.tsurf,self.txtb)
        #pygame.draw.rect(surface,WHITE,rect=self.txtb,width=5)

    def slide(self):
        mouse_pos = list(pygame.mouse.get_pos())
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if mouse_pressed and self.rect.collidepoint(mouse_pos):
            self.clicked = True
        if self.clicked:
            self.percent = max(0,min(1,(mouse_pos[0]-self.rect.left)/250))
            pygame.mixer.music.set_volume(self.percent)

        if not mouse_pressed and self.clicked:
            self.clicked = False

    def dropdown(self,pos):
        self.tsurf = test_font.render(self.text,True,WHITE,BLACK)
        self.rect = pygame.Rect(pos,(250,self.tsurf.get_height()))
        self.txtb = pygame.Rect((pos[0]-250,pos[1]),(250,self.tsurf.get_height()))
        pygame.draw.rect(surface,WHITE,self.rect,width=5)
        pygame.draw.circle(surface,WHITE,pos,3)
        surface.blit(self.tsurf,self.txtb)
        #pygame.draw.rect(surface,WHITE,rect=self.txtb,width=5)
        self.drop(surface)
    
    def drop(self,surface):
        mouse_pos = list(pygame.mouse.get_pos())
        mouse_pos[0] -= 10
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if mouse_pressed and self.rect.collidepoint(mouse_pos):
            self.clicked = True
        if not mouse_pressed and self.clicked:
            self.dropped = not self.dropped
            self.clicked = False
        if self.dropped:
            for i in range(len(new_display_modes)):
                temp = self.rect.move(0,i*50)
                color = GRAY if temp.collidepoint(*mouse_pos) else BLACK
                if color == GRAY  and mouse_pressed:
                    global screen_height, screen_width
                    pygame.display.set_mode(new_display_modes[i][0])
                    screen_width, screen_height = new_display_modes[i][0]
                    set_game()
                    self.dropped = False
                pygame.draw.rect(surface,color,temp)
                new_display_modes[i][1].set_colorkey(BLACK)
                surface.blit(new_display_modes[i][1],(self.rect.x,self.rect.y+i*50),)

def display_text(text: str,surface,pos=(0,0),color = WHITE,bgcolor = BLACK):
    text_surf = test_font.render(text,True,color)
    text_rect = text_surf.get_rect(center = pos)
    surface.blit(text_surf,text_rect)

def set_game():
    global Ball,surface,p_1,p_2,players
    Ball = ball(-1)
    surface = pygame.Surface((screen_width,screen_height))
    surface = surface.convert()
    p_1 = paddle([pygame.K_DOWN,pygame.K_UP],True)
    players = 1
    p_2 = paddle([pygame.K_s,pygame.K_w],False,False)

set_game()
s1,s2 = 0,0
b1 = btn("1 player",pygame.Vector2((0,5)))
b2 = btn("2 player",pygame.Vector2((0,-5)))
b3 = btn("settings",pygame.Vector2((0,-5)))
b4 = btn("main menu",pygame.Vector2((0,-5)))
pygame.mixer.music.set_volume(0.1)
slider = btn("volume:",pygame.Vector2((0,-5)),pygame.mixer.music.get_volume())
ddown = btn("screen size:",pygame.Vector2((0,-5)))
wall = particles(pygame.Rect(400,0,20,150))
boom= []
remove= []
while True:
    pygame.event.pump()
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
        Ball.move([p_1.rect,p_2.rect,wall.rect])

        for i in range(math.floor(screen_height/20)):
            pygame.draw.line(surface,(255,225,225),(screen_width/2,screen_height*i/20),(screen_width/2,screen_height*i/20+10),4)
       
        p_2.draw(surface)
        p_1.draw(surface)
        Ball.draw(surface)
        for particle in boom:
            if not particle.explode(surface):
                #boom.remove(particle)
                remove.append(particle)
        for par in remove:
            boom.remove(par)
        remove.clear()

        if not wall.rain(surface):
            if not waiting:
                waiting = True
                wait_start = pygame.time.get_ticks()

        if waiting and pygame.time.get_ticks() - wait_start >= cooldown*1000:
            waiting = False
            wall.reset()
            cooldown = random.randint(1,3)

        display_text(str(s1),surface,(screen_width/4,20))
        display_text(str(s2),surface,(3*screen_width/4,20))

    elif view == "start":
        s1,s2 = 0,0
        surface.fill(BLACK)
        display_text("Pong",surface,(screen_width/2,screen_height/2 -100))
        
        b1.display(surface,(screen_width/2,screen_height/2))
        b1.run("start1")
        b2.display(surface,(screen_width/2,screen_height/2+50))
        b2.run("start2")
        b3.display(surface,(screen_width/2,screen_height/2+100))
        b3.run("set")
    elif view == "settings":
        surface.fill(BLACK)
        display_text("Settings",surface,(screen_width/2,screen_height/4 -100))
        slider.slider(surface,(screen_width/2,screen_height/4))
        slider.slide()
        ddown.dropdown((screen_width/2,screen_height/4 +50))
        b4.display(surface,(screen_width/2,screen_height-50))
        b4.run("end")
    elif view == "end":
        p_1.setplayer([pygame.K_DOWN,pygame.K_UP])
        p_2.player = False
        surface.fill(BLACK)
        display_text("p1 won" if s1==5 else "p2 won",surface,(screen_width/2,screen_height/2 -100))
        b4.display(surface,(screen_width/2,screen_height/2))
        b4.run("end")
    screen.blit(surface,(0,0))
    pygame.display.update()
    clock.tick(60)
pygame.quit()