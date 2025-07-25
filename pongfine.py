import pygame, random,math


screen_width=700
screen_height=400
flags = pygame.OPENGL | pygame.SCALED
pygame.init()
screen=pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("my game")
clock = pygame.time.Clock()
running = True
white= (255,255,255)
test_font = pygame.font.Font(None,50)
s1,s2 = 0,0
screen_type = "menu"


class pbar:
    def __init__(self,speed,x):
        self.speed = speed
        self.surf = pygame.Surface((20,100)).convert()
        self.surf.fill(white)
        self.rect= self.surf.get_rect().move(x,(screen_height-100)/2)

    def move(self,up):
        if (self.rect.top>=0 and self.rect.bottom <= screen_height):

            if up:
                self.rect.y -= self.speed
            else:
                self.rect.y += self.speed
        
class button():
    def __init__(self,text,pos):
        self.surf = test_font.render(text,True,white,(0,50,50))
        self.rect = self.surf.get_rect(center = pos)
        print((screen_height-self.rect.h)/2)
        self.wave = pygame.math.Vector2((0,5))

    def hover(self):
        #if not self.pressed():
        self.rect.y = math.floor(screen_height-self.rect.h)/2 +self.wave[1]
        self.wave = self.wave.rotate(5)
        #else:
            #self.rect.y += (((screen_height-self.rect.h)/2)-self.rect.y)*.2
            #print(self.rect.y)

    def pressed(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def update(self,screen):
        self.hover()
        screen.blit(self.surf,self.rect)



        
p = pbar(5,0)
cpu = pbar(5,screen_width-20)
ball = pygame.Rect((screen_width/2,screen_height//2,20,20))
b = button("play",(screen_width/2,screen_height/2))

b_xv,b_yv= 0,0
def reset_ball():                       #try not to use global variable in function, use return/class
    global b_xv,b_yv
    b_xv= random.randint(1,4)
    b_yv= random.randint(1,4)
    ball.x = screen_width/2
    ball.y = random.randint(20,screen_height-20) 

def ball_collision(ball,p,cpu):
    global s1,s2
    global b_xv,b_yv

    ball.y +=b_yv
    if not (0 <= ball.top and ball.bottom <= screen_height):
        b_yv = -b_yv
    if ball.colliderect(p) :
        ball.y = p.rect.bottom if ball.top >= (p.rect.centery) else p.rect.y-ball.h
        b_yv = -b_yv
    if ball.colliderect(cpu) :
        ball.y = cpu.rect.bottom if ball.top >= (p.rect.centery) else cpu.rect.y-ball.h
        b_yv = -b_yv
        
    
    ball.x +=b_xv
    if ball.colliderect(p) :
        ball.left = p.rect.right
        b_xv = -b_xv*1.1
    if ball.colliderect(cpu) :
        ball.right = cpu.rect.left
        b_xv = -b_xv*1.1
    if abs(b_xv)>10:
        b_xv = 10* (-1 if b_xv<0 else 1)
    if ball.left <=0:
        s2+=1
        reset_ball()
    if ball.right >= screen_width:
        s1+=1
        reset_ball()
    

def move(p,cpu,ball):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        p.move(True)
    if keys[pygame.K_DOWN]:
        p.move(False)

    if  p.rect.top <= 0:
        p.rect.top = 0
    if p.rect.bottom>=screen_height:
        p.rect.bottom = screen_height

    if 50<ball.y < screen_height-50 and ball.x >screen_width/2-20 :
        cpu.rect.y += (ball.centery-cpu.rect.centery)* .02

reset_ball()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and b.pressed() and screen_type == "menu":
            screen_type = "game"
    
    screen.fill((0,0,0))

    if screen_type == "menu":
        b.update(screen)

    elif screen_type == "game":

        pygame.draw.line(screen,white,(screen_width//2,0),(screen_width//2,screen_height),5)
        
        move(p,cpu,ball)
        ball_collision(ball,p,cpu)
        s1t = test_font.render(f"{s1}",True,white)
        s2t = test_font.render(f"{s2}",True,white)

        screen.blit(s1t,(screen_width//4,20))
        screen.blit(s2t,(3*screen_width//4,20))
        pygame.draw.circle(screen,white,(ball.centerx,ball.centery),10)
        screen.blit(p.surf,p.rect)
        screen.blit(cpu.surf,cpu.rect)

    
    pygame.display.update()
    clock.tick(60)
pygame.quit()