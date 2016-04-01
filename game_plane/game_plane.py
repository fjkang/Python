import pygame
from sys import exit
import random
import pickle
# -*- coding: utf-8 -*-
#D:\Python27\k\game_plane\  路径
class Bullet:
    def __init__(self):
        self.x = 0
        self.y = -1
        self.image = pygame.image.load(r'bullet.png').convert_alpha()
        self.active = False
        
    def move(self):
        if self.active:
            self.y -= 3
        if self.y < 0:
            self.active = False
            
    def restart(self):
        mouseX,mouseY = pygame.mouse.get_pos()
        self.x = mouseX - self.image.get_width() /2
        self.y = mouseY - self.image.get_height() /2
        self.active = True

class Enemy:
    def restart(self):
        self.x = random.randint(50,400)
        self.y = random.randint(-200,-50)
        self.speed = random.random()/2 + 0.1
        
    def __init__(self):		
        self.restart()
        self.image = pygame.image.load(r'enemy.png').convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def move(self):
        if self.y < 600:
            self.y += self.speed
        else:
            self.restart()
        
class Plane:
    def restart(self):
        self.x = 200
        self.y = 500
        
    def __init__(self):
        self.restart()
        self.image = pygame.image.load(r'plane.png').convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def move(self):
        mouseX,mouseY = pygame.mouse.get_pos()
        width = self.width /2
        height = self.height /2
        #plane限制范围
        if mouseY >= 600 - height:
            self.y = 600 - 2*height
            if mouseX < width:
                self.x = 0
            elif mouseX > 450 - width:
                self.x = 450 - 2*width
            else:
                self.x = mouseX - width
        elif mouseY < height:
            self.y = 0
            if mouseX < width:
                self.x = 0
            elif mouseX > 450 - width:
                self.x = 450 - 2*width
            else:
                self.x = mouseX - width
        else:
            self.y = mouseY - height
            if mouseX < width:
                self.x = 0
            elif mouseX > 450 - width:
                self.x = 450 - 2*width
            else:
                self.x = mouseX - width
        
def checkCrash(enemy,plane):
    if(plane.x + 0.7*plane.width > enemy.x) \
    and (plane.x + 0.3*plane.width < enemy.x + enemy.width)\
    and (plane.y + 0.7*plane.height > enemy.y)\
    and (plane.y + 0.3*plane.height < enemy.y + enemy.height):
        return True
    return False
    
    
def checkHit(enemy, bullet):
    if enemy.x < bullet.x and bullet.x < (enemy.x + enemy.width) \
    and enemy.y < bullet.y and bullet.y < (enemy.y + enemy.height):
        enemy.restart()
        bullet.active = False
        return True
    return False


print u'请输入你的名字：'
name = raw_input()

try:
    f = open('user.txt')
    users = pickle.load(f)
    f.close()
    user = users.get(name)
    if user == None:
        high = 0
    else:
        high = int(user[0])

except:
    high = 0
    users = {}


pygame.init()
screen = pygame.display.set_mode((450,600))
pygame.display.set_caption('Hello, World!')
background = pygame.image.load(r'back.jpg').convert()
score = 0
life = 5
font = pygame.font.Font(None, 32)
gameOver = False

bullets = []
for i in range(4):
    bullets.append(Bullet())
count_b = len(bullets)
index_b = 0
interval_b = 0

enemies = []
for i in range(5):
    enemies.append(Enemy())

plane = Plane()

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
        
        if life == 0 and event.type == pygame.MOUSEBUTTONUP:
            pygame.quit()
            exit()
        
        if gameOver and event.type == pygame.MOUSEBUTTONUP:
            plane.restart()
            for e in enemies:
                e.restart()
            for b in bullets:
                b.active = False
            score = 0
            gameOver = False
    
    screen.blit(background,(0,0))

	#子弹
    interval_b -= 1
    if interval_b < 0:
        bullets[index_b].restart()
        interval_b = 100
        index_b = (index_b + 1) % count_b
    for b in bullets:
        #print b.active
        #print interval_b
        if b.active:
            #print b.x,b.y
            b.move()
            #print b.x,b.y
            screen.blit(b.image, (b.x, b.y))

    if not gameOver:
        for e in enemies:
            if checkCrash(e, plane):
                gameOver = True
                life -= 1
            e.move()
            screen.blit(e.image, (e.x, e.y))
        plane.move()
        screen.blit(plane.image, (plane.x, plane.y))
        text_s =  font.render('Score:%d' % score, 1, (0, 0, 0))
        screen.blit(text_s, (0, 0))
        l = ''
        #font1 = pygame.font.Font(None, 50)
        for i in range(life):
            l = l + u'♥'
        text_l =  font.render(l, 1, (0, 0, 0))
        screen.blit(text_l, (300, 0))
        
    else:
        for b in bullets:
            b.active = False
        if score > high:
            high = score
            users[name] = [str(high),]
            f = open('user.txt', 'w')
            pickle.dump(users, f)
            f.close()
        text_s =  font.render('Score:%d' % score, 1, (0, 0, 0))
        screen.blit(text_s, (190, 300))

    #是否打中
    for b in bullets:
        if b.active:
            for e in enemies:
                if checkHit(e, b):
                    score += 100
            b.move()
            screen.blit(b.image, (b.x, b.y))
    text_h =  font.render('high:%d' % high, 1, (0, 0, 0))
    screen.blit(text_h, (130, 0))

    pygame.display.update()
