import pygame
from sys import exit

pygame.init()

screen_width = 600
screen_hight = 500
screen = pygame.display.set_mode((screen_width,screen_hight))
pygame.display.set_caption('Pong')
test_font = pygame.font.Font(None,50)
clock = pygame.time.Clock()

class paddle():
    def __init__(self, player = False):
        
        self.y_offset = screen_hight/10
        self.pos = [580*(not player),screen_hight/2 - self.y_offset]
        self.rect = pygame.Rect(self.pos,(20,screen_hight/5))
        self.speed = 5
        self.player = player


    def move(self,ball_pos = []):
        if self.player:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN] and self.rect.bottom <= screen_hight:
                self.pos[1] += self.speed
            elif keys[pygame.K_UP] and self.rect.top >= 0:
                self.pos[1] -= self.speed
        
        else:
            if ball_pos [1] - self.y_offset >= 0 and ball_pos[1] + self.y_offset + 20 <= screen_hight and ball_pos[0] >= screen_width/2:
                self.pos[1] += (ball_pos[1] - self.pos[1] - self.y_offset)*0.06


    def draw(self,surface):
        r = pygame.Rect(self.pos,(20,screen_hight/4))
        self.rect = r
        pygame.draw.rect(surface,(225,225,225),r)

class ball():
    def __init__(self):
        self.pos = [screen_width/2,screen_hight/2]
        self.rect = pygame.Rect(self.pos,(20,20))
        self.speed_x = -4
        self.speed_y = 4

    def move(self):
 
        self.bounce()
        self.pos[0] += self.speed_x
        self.pos[1] += self.speed_y


    def bounce(self):
        global score

        if self.rect.left <=0:
            score = 0
            self.pos = [screen_width/2,screen_hight/2]
            
        if self.rect.right >= screen_width:
            score += 1
            self.pos = [screen_width/2,screen_hight/2]
        
        if self.rect.top <= 0 or self.rect.bottom >= screen_hight:
            self.speed_y *= -1

    def return_pos(self):
        return self.pos
        
    def draw(self,surface):
        r = pygame.Rect(self.pos,(20,20))
        self.rect = r
        pygame.draw.rect(surface,(225,225,225),r)

    

Ball = ball()
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
player = paddle(True)
enemy_paddle = paddle() 
score = 0
def display_score(scr):
    score_surface = test_font.render('score: ' + str(scr),False,(225,225,225))
    score_rect = score_surface.get_rect(center = (screen_width/2,50))
    screen.blit(score_surface,score_rect)

def collision(paddles,ball):
    for paddle in paddles:
        if paddle.colliderect(ball.rect):
            if paddle.right == ball.rect.left + 4 or paddle.left == ball.rect.right - 4:       #change according to speed
                ball.speed_x *= -1
            else:
                ball.speed_y *= -1
        else:
            pass

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    surface.fill('black')

    enemy_paddle.move(Ball.return_pos())
    player.move()
    collision([player.rect,enemy_paddle.rect],Ball)
    Ball.move()


    pygame.draw.line(surface,(225,225,225),(screen_width/2,0),(screen_width/2,screen_hight),2)
    
    enemy_paddle.draw(surface)
    player.draw(surface)
    Ball.draw(surface)
    screen.blit(surface,(0,0))
    display_score(score)
    pygame.display.update()

    clock.tick(60)
        
    