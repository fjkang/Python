#-*-coding:utf-8-*-
import pygame
import copy
import random

class Snake:
    def __init__(self):
        self.poslist = [[per_size,per_size,per_size,per_size]]
        
    def position(self):
        return self.poslist
        
    def gowhere(self, where):
        #这是蛇身体的移动
        pos = len(self.poslist) - 1
        while pos > 0:
            self.poslist[pos] = copy.deepcopy(self.poslist[pos-1])
            pos -= 1
        #这是蛇头的移动
        head = self.poslist[pos]
        if where == 'U':
            head[1] -= per_size
            if head[1] < 0:
                head[1] = height-per_size
        if where == 'D':
            head[1] += per_size
            if head[1] > height-per_size:
                head[1] = 0
        if where == 'L':
            head[0] -= per_size
            if head[0] < 0:
                head[0] = width-per_size
        if where == 'R':
            head[0] += per_size
            if head[0] > width-per_size:
                head[0] = 0
    
    def eatfood(self, foodpoint):
        self.poslist.append(foodpoint)
        return self.position()
        
class Food:
    def __init__(self):
        self.x = random.randint(1,19)*per_size
        self.y = random.randint(1,19)*per_size
        self.w = per_size
        self.h = per_size
    
    def position(self):
        return [self.x, self.y, self.w, self.h]
    
    def display(self):
        self.x = random.randint(1,19)*per_size
        self.y = random.randint(1,19)*per_size
        return self.position()



moveup = False
movedown = False
moveleft = False
moveright = True
pygame.init()
clock = pygame.time.Clock()
width = 400
height = 400
per_size = 20
screen = pygame.display.set_mode([width,height])
restart = True
while restart:
    snake = Snake()
    food = Food()
    screetitle = pygame.display.set_caption('eat snake')
    
    snake.gowhere('R')
    running = True
    while running:
        screen.fill([255,255,255])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    moveup = True
                    movedown = False
                    moveleft = False
                    moveright = False
                if event.key == pygame.K_DOWN:
                    moveup = False
                    movedown = True
                    moveleft = False
                    moveright = False
                if event.key == pygame.K_LEFT:
                    moveup = False
                    movedown = False
                    moveleft = True
                    moveright = False
                if event.key == pygame.K_RIGHT:
                    moveup = False
                    movedown = False
                    moveleft = False
                    moveright = True

        time_pass = clock.tick(10)
        if moveup:
            snake.gowhere('U')
        if movedown:
            snake.gowhere('D')
        if moveleft:
            snake.gowhere('L')
        if moveright:
            snake.gowhere('R')

        foodpoint = food.position()
        fdrect = pygame.draw.rect(screen, [255,0,0], foodpoint, 0)

        poslist = snake.position()
        snaffect = []
        for pos in poslist:
            snaffect.append(pygame.draw.rect(screen, [0,0,0], pos, 0))
            
            if fdrect.colliderect(pos):
                
                snake.eatfood(foodpoint)
                foodpoint = food.display()
                break

        headrect = snaffect[0]
        count = len(snaffect)
        while count > 1:
            if headrect.colliderect(snaffect[count -1]):
                running = False
            count -= 1             
        pygame.display.update()

    pygame.font.init()
    screen.fill([100,0,0])
    font = pygame.font.Font(None,40)
    text = font.render('Game Over!!!', True, (255,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery
    screen.blit(text,textRect)

    while 1:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart = True
                del snake
                del food
                break
            if event.key == pygame.K_n:
                restart = False
                break
        pygame.display.update()
    
