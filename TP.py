import pygame
#from webScraping.py import *

class Character(object):
    def __init__(self, x, y, walkRight, walkLeft, walkFront, walkBack, stand, 
    width, height, walkCount, speed, left=False, right=False, front=False, 
    back=False):
        self.x, self.y = x, y
        self.walkRight, self.walkLeft = walkRight, walkLeft
        self.walkFront, self.walkBack = walkFront, walkBack
        self.width, self.height = width, height
        self.right, self.left = right, left 
        self.front, self.back = front, back
        self.walkCount = walkCount
        self.speed = speed
        self.stand = stand

class Background(object):
    def __init__(self, image, name):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (600, 400))
        self.name = name

class Item(object):
    def __init__(self, image, x, y, width, height, name):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.name = name
        self.x, self.y = x, y

class PlayGame(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.protagonist = self.createCharacter()
        self.item1 = None
        self.streetBackground = Background('street.png', 'street')
        self.home = self.createItems()

    def createCharacter(self):
        walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), 
                    pygame.image.load('R3.png'), pygame.image.load('R4.png')]
        walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), 
                    pygame.image.load('L3.png'), pygame.image.load('L4.png')]
        walkFront = [pygame.image.load('F1.png'), pygame.image.load('F2.png'), 
                    pygame.image.load('F3.png'), pygame.image.load('F4.png')]
        walkBack = [pygame.image.load('B1.png'), pygame.image.load('B2.png'), 
                    pygame.image.load('B3.png'), pygame.image.load('B4.png')]

        #rescale every single spritesheet            
        for item in [walkRight, walkLeft, walkFront, walkBack]:
            for i in range(len(item)):
                item[i] = pygame.transform.scale(item[i], (30, 45))

        stand = pygame.transform.scale(pygame.image.load('stand.png'),
                                            (30, 45))
        walkCount = 0
        return Character(250, 250, walkRight, walkLeft, walkFront, walkBack, 
                        stand, 30, 30, walkCount, 10)

    def createItems(self):
        return Item('home.png', 100, 100, 150, 50, 'home')
    
    def drawProtagonist(self, surface, moveL, moveR, moveB, moveF):
        if self.protagonist.walkCount == 4:
            self.protagonist.walkCount = 0

        if self.protagonist.left and moveL:
            surface.blit(self.protagonist.walkLeft[self.protagonist.walkCount], 
                    (self.protagonist.x, self.protagonist.y))
            self.protagonist.walkCount += 1
        elif self.protagonist.right and moveR:
            surface.blit(self.protagonist.walkRight[self.protagonist.walkCount], 
                    (self.protagonist.x, self.protagonist.y))
            self.protagonist.walkCount +=1
        elif self.protagonist.front and moveF:
            surface.blit(self.protagonist.walkFront[self.protagonist.walkCount], 
                    (self.protagonist.x, self.protagonist.y))
            self.protagonist.walkCount +=1
        elif self.protagonist.back and moveB:
            surface.blit(self.protagonist.walkBack[self.protagonist.walkCount], 
                    (self.protagonist.x, self.protagonist.y))
            self.protagonist.walkCount +=1
        else:
            surface.blit(self.protagonist.stand,
                    (self.protagonist.x, self.protagonist.y))

    def drawItem(self, surface):
        surface.blit(self.home.image, (self.home.x, self.home.y))

    def redrawGameWindow(self, surface, moveL, moveR, moveF, moveB):
        surface.blit(self.streetBackground.image, 
                    (0, 0))

        self.drawItem(surface)
        self.drawProtagonist(surface, moveL, moveR, moveF, moveB)
        
        pygame.display.update()

    def detectKeyPressed(self, keys):
        if (keys[pygame.K_LEFT] and 
            self.protagonist.x > self.protagonist.speed):
            self.protagonist.x -= self.protagonist.speed
            self.protagonist.left = True
            self.protagonist.right = False
            moveL = True
            moveR, moveF, moveB = False, False, False
        elif (keys[pygame.K_RIGHT] and self.protagonist.x < 
            (self.width - self.protagonist.width - self.protagonist.speed)):
            self.protagonist.x += self.protagonist.speed
            self.protagonist.right = True
            self.protagonist.left = False
            moveR = True
            moveL, moveF, moveB = False, False, False
        elif (keys[pygame.K_UP] and 
            self.protagonist.y > self.protagonist.speed):
            self.protagonist.y -= self.protagonist.speed
            self.protagonist.back, self.protagonist.front = True, False
            moveB = True
            moveL, moveR, moveF = False, False, False
        elif (keys[pygame.K_DOWN] and self.protagonist.y <
            (self.height - self.protagonist.height - self.protagonist.speed)):
            self.protagonist.y += self.protagonist.speed
            self.protagonist.front, self.protagonist.back = True, False
            moveF = True
            moveL, moveR, moveB = False, False, False
        else:
            moveL, moveR, moveF, moveB = False, False, False, False
            self.protagonist.walkCount = 0   

        return moveL, moveR, moveF, moveB

    def runGame(self):

        pygame.init()
        surface = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("First Game")
        clock = pygame.time.Clock()

        #mainloop
        run = True
        while run:
            clock.tick(15)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()
            (moveL, moveR, moveF, moveB) = self.detectKeyPressed(keys)
                    
            self.redrawGameWindow(surface, moveL, moveR, moveF, moveB)

        pygame.quit()

PlayGame(600, 400).runGame()