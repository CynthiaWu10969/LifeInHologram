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
        self.hitbox = (self.x, self.y, width, height)

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
        self.hitbox = (self.x , self.y , width, height)

class PlayGame(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.protagonist = self.createCharacter()
        self.streetBackground = Background('street.png', 'street')
        self.home, self.bank, self.market = None, None, None
        self.workplace, self.park = None, None
        self.createItems()
        self.itemList = [self.home, self.bank, self.market, 
                        self.workplace, self.park]

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
        return Character(self.width//2, self.height//2, walkRight, walkLeft, 
                        walkFront, walkBack, stand, 30, 45, walkCount, 10)
    
    def createItems(self):
        self.home = Item('home.png', self.width//6, self.height//4, 150, 50, 
                        'home')
        self.bank = Item('bank.png', 5*self.width//6, 5*self.height//24, 80, 
                        64,'bank')
        self.market = Item('market.png', 7*self.width//24, 23*self.height//40, 
                            100, 100, 'market')
        self.park = Item('park.png', 19*self.width//32, 7*self.height//12, 
                            100, 100, 'park')
        self.workplace = Item('workplace.png', 5*self.width//6, 
                                7*self.height//12, 75, 100, 'workplace')

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
        self.protagonist.hitbox=(self.protagonist.x, self.protagonist.y, 
                                self.protagonist.width, 
                                self.protagonist.height)
        pygame.draw.rect(surface, (255, 0, 0), self.protagonist.hitbox, 2)

    def drawItem(self, surface):
        for item in self.itemList:
            surface.blit(item.image, (item.x, item.y))
            pygame.draw.rect(surface, (255, 0, 0), item.hitbox, 2)

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
        surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Main Street")
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