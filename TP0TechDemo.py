import pygame

class Character(object):
    def __init__(self, x, y, walkRight, walkLeft, standLeft, standRight, 
    width, height, left, right, walkCount, velocity):
        self.x, self.y = x, y
        self.walkRight, self.walkLeft = walkRight, walkLeft
        self.width, self.height = width, height
        self.right, self.left = right, left 
        self.walkCount = walkCount
        self.velocity = velocity
        self.standLeft, self.standRight = standLeft, standRight

class Item(object):
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height

class PlayGame(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.protagonist = None
        self.item1 = None

    def createCharacter(self):
        walkRight = [pygame.image.load('right1.png'), pygame.image.load('right2.png'), 
                    pygame.image.load('right3.png'), pygame.image.load('right4.png'), 
                    pygame.image.load('right5.png'), pygame.image.load('right6.png'), 
                    pygame.image.load('right7.png')]
        walkLeft = [pygame.image.load('left1.png'), pygame.image.load('left2.png'), 
                    pygame.image.load('left3.png'), pygame.image.load('left4.png'), 
                    pygame.image.load('left5.png'), pygame.image.load('left6.png'), 
                    pygame.image.load('left7.png')]
        for i in range(len(walkRight)):
            walkRight[i] = pygame.transform.scale(walkRight[i], (30, 60))
        for i in range(len(walkLeft)):
            walkLeft[i] = pygame.transform.scale(walkLeft[i], (30, 60))
        standLeft = pygame.transform.scale(pygame.image.load('standLeft.png'),
                                            (30, 60))
        standRight = pygame.transform.scale(pygame.image.load('standRight.png'), 
                                            (30, 60))

        left = False
        right = False
        walkCount = 0

        self.protagonist = Character(250, 250, walkRight, walkLeft, 
                    standLeft, standRight, 10, 10, left, right, walkCount, 10)

    def redrawGameWindow(self, win, moveLeft=False, moveRight=False):
        if self.protagonist.walkCount == 7:
            self.protagonist.walkCount = 0
        if self.protagonist.left and moveLeft:
            win.blit(self.protagonist.walkLeft[self.protagonist.walkCount], 
                    (self.protagonist.x, self.protagonist.y))
            self.protagonist.walkCount += 1
        elif self.protagonist.right and moveRight:
            win.blit(self.protagonist.walkRight[self.protagonist.walkCount], 
                    (self.protagonist.x, self.protagonist.y))
            self.protagonist.walkCount +=1
        elif self.protagonist.right:
            win.blit(self.protagonist.standRight, 
                    (self.protagonist.x, self.protagonist.y))
        else:
            win.blit(self.protagonist.standLeft,
                    (self.protagonist.x, self.protagonist.y))
        
        pygame.display.flip()

    def runGame(self):

        pygame.init()
        win = pygame.display.set_mode((500,500))
        pygame.display.set_caption("First Game")
        clock = pygame.time.Clock()

        self.createCharacter()

        #mainloop
        run = True
        while run:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()

            if (keys[pygame.K_LEFT] and 
                self.protagonist.x > self.protagonist.velocity):
                self.protagonist.x -= self.protagonist.velocity
                self.protagonist.left = True
                self.protagonist.right = False
                moveLeft = True
            elif keys[pygame.K_RIGHT] and self.protagonist.x < 500 - self.protagonist.width - self.protagonist.velocity:
                self.protagonist.x += self.protagonist.velocity
                self.protagonist.right = True
                self.protagonist.left = False
                moveRight = True
            else:
                moveLeft = False
                moveRight = False
                self.protagonist.walkCount = 0
                    
            self.redrawGameWindow(win, moveLeft, moveRight)

        pygame.quit()

PlayGame(500, 500).runGame()