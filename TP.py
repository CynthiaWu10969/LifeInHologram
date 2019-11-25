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
        self.isCollide = False
        self.inMarket = False

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
        self.buyDesk, self.sellDesk = None, None
        self.sellIcon, self.buyIcon, self.marketIcon = None, None, None
        self.createMarketItems()
        self.marketItems = [self.buyDesk, self.sellDesk, self.buyIcon, 
                            self.sellIcon, self.marketIcon]

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
        self.home = Item('home.png', self.width//6, self.height//4+7, 150, 50, 
                        'home')
        self.bank = Item('bank.png', 5*self.width//6, 5*self.height//24+10, 80, 
                        64,'bank')
        self.market = Item('market.png', 7*self.width//24, 23*self.height//40+7, 
                            100, 100, 'market')
        self.park = Item('park.png', 19*self.width//32, 7*self.height//12+5, 
                            100, 100, 'park')
        self.workplace = Item('workplace.png', 5*self.width//6, 
                                7*self.height//12+5, 75, 100, 'workplace')

    def createMarketItems(self):
        self.buyDesk = Item('buyDesk.png', 4*self.width//6, self.height//5, 
                            150, 150, 'buy desk')
        self.sellDesk = Item('sellDesk.png', self.width//10, self.height//5, 
                            150, 100, 'sell desk')
        self.buyIcon = Item('buyIcon.png', 5*self.width//6, self.height//10, 
                            50, 50, 'buy icon')
        self.sellIcon = Item('sellIcon.png', self.width//6, self.height//10, 
                            50, 50, 'sell icon')
        self.marketIcon = Item('marketIcon.png', self.width//2, self.height//5, 
                                50, 50, 'market icon')

    def detectCollision(self): #hitbox: (left top)x, y, width, height 
        if ((self.protagonist.hitbox[0] + self.protagonist.hitbox[2] > self.market.hitbox[0] and self.protagonist.hitbox[0] + self.protagonist.hitbox[2] < self.market.hitbox[0] + self.market.hitbox[2])
            and (self.protagonist.hitbox[1] + self.protagonist.hitbox[3] > self.market.hitbox[1] and self.protagonist.hitbox[1] + self.protagonist.hitbox[3] < self.market.hitbox[1] + self.market.hitbox[3])):
            self.protagonist.isCollide = True
        else:
            self.protagonist.isCollide = False

    def drawProtagonist(self, stSurface, moveL, moveR, moveB, moveF):
        if self.protagonist.isCollide:
            stSurface.blit(self.protagonist.stand, 
                        (self.protagonist.x, self.protagonist.y))
        else:
            if self.protagonist.walkCount == 4:
                self.protagonist.walkCount = 0
            if self.protagonist.left and moveL:
                stSurface.blit(self.protagonist.walkLeft[self.protagonist.walkCount], 
                        (self.protagonist.x, self.protagonist.y))
                self.protagonist.walkCount += 1
            elif self.protagonist.right and moveR:
                stSurface.blit(self.protagonist.walkRight[self.protagonist.walkCount], 
                        (self.protagonist.x, self.protagonist.y))
                self.protagonist.walkCount +=1
            elif self.protagonist.front and moveF:
                stSurface.blit(self.protagonist.walkFront[self.protagonist.walkCount], 
                        (self.protagonist.x, self.protagonist.y))
                self.protagonist.walkCount +=1
            elif self.protagonist.back and moveB:
                stSurface.blit(self.protagonist.walkBack[self.protagonist.walkCount], 
                        (self.protagonist.x, self.protagonist.y))
                self.protagonist.walkCount +=1
            else:
                stSurface.blit(self.protagonist.stand,
                        (self.protagonist.x, self.protagonist.y))
        self.protagonist.hitbox=(self.protagonist.x, self.protagonist.y, 
                                self.protagonist.width, 
                                self.protagonist.height)
        pygame.draw.rect(stSurface, (255, 0, 0), self.protagonist.hitbox, 2)

    def drawStItem(self, stSurface):
        for item in self.itemList:
            stSurface.blit(item.image, (item.x, item.y))
            pygame.draw.rect(stSurface, (255, 0, 0), item.hitbox, 2)

    def redrawStreetWindow(self, stSurface, moveL, moveR, moveF, moveB):
        stSurface.blit(self.streetBackground.image, (0, 0))

        self.drawStItem(stSurface)
        self.drawProtagonist(stSurface, moveL, moveR, moveF, moveB)
        
        pygame.display.update()

    def moveProtagonist(self, keys):
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

    def cancelMove(self, direction):
        if direction == 'left':
            self.protagonist.x += 1
        if direction == 'right':
            self.protagonist.x -= 1
        if direction == 'front':
            self.protagonist.y -= 1
        if direction == 'back':
            self.protagonist.y += 1

    def detectKeyPressed(self, keys):
        moveL, moveR, moveF, moveB = self.moveProtagonist(keys)
        direction = None

        return moveL, moveR, moveF, moveB

    def checkDirectForCollision(self, moveL, moveR, moveF, moveB):
        if moveL == True:
            direction = 'left'
        elif moveR == True:
            direction = 'right'
        elif moveF == True:
            direction = 'front'
        elif moveB == True:
            direction = 'back'
        else:
            direction = None
        print("current moving direction: ", direction)

        if self.protagonist.isCollide:
            self.cancelMove(direction)

    def drawMarketItem(self, marketSurface):
        for item in self.marketItems:
            marketSurface.blit(item.image, (item.x, item.y))
            pygame.draw.rect(marketSurface, (255, 0, 0), item.hitbox, 2)

    def redrawMarketWindow(self, marketSurface, moveL, moveR, moveF, moveB):
        marketBgImage = pygame.image.load('marketBg.png')
        marketBgImage = pygame.transform.scale(marketBgImage, (self.width, 
                                                                self.height))
        marketSurface.blit(marketBgImage, (0, 0))

        self.drawMarketItem(marketSurface)
        self.drawProtagonist(marketSurface, moveL, moveR, moveF, moveB)

        pygame.display.update()

    def marketDetectCollision(self):
        self.protagonist.isCollide = False

    def inMarketRunGame(self):
        marketSurface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Stock Market")
        clock = pygame.time.Clock()

        run = True
        while run:
            print("protagonist's in market")
            clock.tick(15)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()
            (moveL, moveR, moveF, moveB) = self.detectKeyPressed(keys)

            self.marketDetectCollision()
            print('is it colliding: ', self.protagonist.isCollide)
            self.checkDirectForCollision(moveL, moveR, moveF, moveB)

            self.redrawMarketWindow(marketSurface, moveL, moveR, moveF, moveB)

        pygame.quit()

    def runGame(self):
        pygame.init()
        stSurface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Main Street")
        clock = pygame.time.Clock()

        #mainloop
        run = True
        while run:
            clock.tick(15)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if self.protagonist.isCollide:
                self.inMarketRunGame()
            
            keys = pygame.key.get_pressed()
            (moveL, moveR, moveF, moveB) = self.detectKeyPressed(keys)
            self.detectCollision()
            print('is it colliding: ', self.protagonist.isCollide)
            self.checkDirectForCollision(moveL, moveR, moveF, moveB)
                    
            self.redrawStreetWindow(stSurface, moveL, moveR, moveF, moveB)

        pygame.quit()

PlayGame(600, 400).runGame()