'''
import pygame
pygame.init()

win = pygame.display.set_mode((500,480))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()


class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)
                


class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)

    def draw(self,win):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0

        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
            self.walkCount += 1
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        print('hit')

        

def redrawGameWindow():
    win.blit(bg, (0,0))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    
    pygame.display.update()

#mainloop
man = player(200, 410, 64,64)
goblin = enemy(100, 410, 64, 64, 450)
shootLoop = 0
bullets = []
run = True
while run:
    clock.tick(27)

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                bullets.pop(bullets.index(bullet))
                
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1
            
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 6, (0,0,0), facing))

        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
        
    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
            
    redrawGameWindow()

pygame.quit()


x, y, z = 1, 2, 3
print(x)
print(y)
print(z)

import pygame
import pygame_gui


pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((800, 600))

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                             text='Say Hello',
                                             manager=manager)

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == 'ui_button_pressed':
                if event.ui_element == hello_button:
                    print('Hello World!')
        print(type(hello_button))
        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()

import pygame
from pygame.locals import *

# the following line is not needed if pgu is installed
import sys; sys.path.insert(0, "..")

from pgu import gui

##::
app = gui.App()

e = gui.Button("Hello World")

app.connect(gui.QUIT, app.quit)

app.run(e)

# happyTG.py
# Run this for a holiday message.
# Carpe diem! (And carve turkeyem!)
# David

from tkinter import *
def happyTG():

  msg = """
   0OO ooO                                         0OOOO0o   0Ooo
    O   @                                          O  o  o  O    o
    O   0                                             O    o
    O   o   o@OO   O0OOoO  @OO0Oo  oo@ OOo            o    0
    Oo0OO       o   O    @  O    O  o   O             0    O
    o   O   @OOOX   X    X  X    X  X   X             X    X   XXX
    X   X  X    X   X    X  X    X   X X              X    X     X
    X   X  X    X   X    X  X    X   X X              X     X    X
   XXX XXX  XXXX X  XXXXX   XXXXX     X              XXX     XXXX
                    X       X         X
                   XXX     XXX      XX
  """

  def f(t):
      s = ""
      for c in t:
          if (not c.isspace() and (c != "X")): s += c
      (r,c,a,t) = ([],0,1,[72])
      for d in (reversed(s)):
          if (d.isalpha()): (c,a) = (c+d.isupper()*a, a+a)
          else:
              r+=[(1-ord(d)//50*2)*c]
              (c,a) = (0,1)
      for v in r[::-1]: t += [t[-1]+v]
      return "".join(map(chr,t)).replace("T"," T")+"!!!"
  s = f(msg)

  def tf():
      canvas.delete(ALL)
      for dx in [5,35]:
          f,x[0] = "Arial %d bold"%((x[0]+dx)%60),x[0]+dx//8
          canvas.create_text(300,150,text=s,fill="orange",font=f)
      canvas.after(250, tf)
  root,x = Tk(),[0]
  canvas = Canvas(root, width=600, height=300)
  canvas.pack()
  tf()
  root.mainloop()

happyTG()

import pygame

pygame.init()

FONT = pygame.font.SysFont("Sans", 20)
TEXT_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)

loop = True
start_time = None
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start_time = pygame.time.get_ticks()

    screen.fill(BG_COLOR)

    if start_time:
        time_since_enter = pygame.time.get_ticks() - start_time
        message = 'Milliseconds since enter: ' + str(time_since_enter)
        screen.blit(FONT.render(message, True, TEXT_COLOR), (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

import random

num = random.uniform(2, 4)
print(num)
num = round(num, 2)
print(num)


d = {'a':1, 'b':2, 'c':3}
l = list(d.keys())
print(l)

d = {}
print('a' in d)
'''
s = 'abc'
print(s[0])