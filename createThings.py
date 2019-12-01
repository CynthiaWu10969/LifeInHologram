import pygame

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
        self.isCollide, self.isBuy, self.isSell = False, False, False
        self.inMarket = False
        self.money = 20000
        self.inventory = dict()
        self.exitBuy, self.exitSell = False, False

class Background(object):
    def __init__(self, image, name):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (600, 400))
        self.name = name

class Button(object):
    def __init__(self, image, x, y, width, height, stock=None):
        self.image = image
        self.image = pygame.transform.scale(self.image, (width, height))
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.stock = stock
    
    def isClick(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

    def drawButton(self, surface):
        surface.blit(self.image, (self.x, self.y))

class Item(object):
    def __init__(self, image, x, y, width, height, name):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.name = name
        self.x, self.y = x, y
        self.hitbox = (self.x , self.y , width, height)