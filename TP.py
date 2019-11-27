import pygame
import pygame_gui
import webScraping
import createThings
from tkinter import *
import string

class PlayGame(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.protagonist = self.createCharacter()
        self.streetBackground = createThings.Background('street.png', 'street')
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
        self.exitBuy, self.exitSell = False, False
        self.buyButtons, self.sellButtons = dict(), dict()
        self.stockData = webScraping.scraping() #a list of dictionaries
        self.manager = pygame_gui.UIManager((self.width, self.height))

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
        return createThings.Character(self.width//2, self.height//2, walkRight, walkLeft, 
                        walkFront, walkBack, stand, 30, 45, walkCount, 10)
    
    def createItems(self):
        self.home = createThings.Item('home.png', self.width//6, self.height//4+7, 150, 50, 
                        'home')
        self.bank = createThings.Item('bank.png', 5*self.width//6, 5*self.height//24+10, 80, 
                        64,'bank')
        self.market = createThings.Item('market.png', 7*self.width//24, 23*self.height//40+7, 
                            100, 100, 'market')
        self.park = createThings.Item('park.png', 19*self.width//32, 7*self.height//12+5, 
                            100, 100, 'park')
        self.workplace = createThings.Item('workplace.png', 5*self.width//6, 
                                7*self.height//12+5, 75, 100, 'workplace')

    def createMarketItems(self):
        self.buyDesk = createThings.Item('buyDesk.png', 4*self.width//6, self.height//5, 
                            150, 150, 'buy desk')
        self.sellDesk = createThings.Item('sellDesk.png', self.width//10, self.height//5, 
                            150, 100, 'sell desk')
        self.buyIcon = createThings.Item('buyIcon.png', 5*self.width//6, self.height//10, 
                            50, 50, 'buy icon')
        self.sellIcon = createThings.Item('sellIcon.png', self.width//6, self.height//10, 
                            50, 50, 'sell icon')
        self.marketIcon = createThings.Item('marketIcon.png', self.width//2, self.height//5, 
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
        
        self.drawWallet(stSurface)
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

    def drawStockBuy(self, marketSurface):
        colDis = (5 * self.width // 6 - self.width // 12) // 6
        rowDis = (2 * self.height // 3 - self.height // 8) // 6

        imageX = self.width // 12 + 2 * (5 * self.width//6 - self.width//12) // 5
        imageY = self.height//8
        marketImage = pygame.image.load('buy.png')
        marketImage = pygame.transform.scale(marketImage, (100, 50))
        marketSurface.blit(marketImage, (imageX, imageY))

        font = pygame.font.SysFont('arial', 15, True)
        stockInfo = ['Symbol', 'Price', 'Change', '% Change', 
                    'Market Cap']
        
        for j in range(len(stockInfo)): # draws the table for stocks
            for i in range(6):
                if i == 0:
                    text = font.render(stockInfo[j], 1, (0, 0, 0))
                else:
                    text = font.render(self.stockData[i-1][stockInfo[j]], 1, 
                                    (0, 0, 0))
                marketSurface.blit(text, (3*self.width//24 + colDis * j, 
                                    2*self.height//8 + rowDis * i))
        self.createBuyButtons(marketSurface, colDis, rowDis)

    def createBuyButtons(self, surface, colDis, rowDis):
        buttonW, buttonH = colDis, rowDis
        x = 3 * self.width // 24 + colDis * 5

        image = pygame.image.load('buyButton.png')
        image = pygame.transform.scale(image, (buttonW, buttonH))

        for i in range(len(self.stockData)-1):
            button = createThings.Button(image, x, self.height//4+rowDis*(i+1), 
                                        buttonW, buttonH, 
                                        self.stockData[i]['Symbol'])
            self.buyButtons[self.stockData[i]['Symbol']] = button
            button.drawButton(surface)
        '''
        for i in range(len(self.stockData)):
            button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((3*self.width//24 + colDis * 4, 2*self.height//8 + rowDis * i), 
                                                                            (colDis, rowDis)), text='BUY', manager=self.manager)
            self.buyButtons[self.stockData[i]['Symbol']] = button #key=symbol
        '''

    def drawBuyWindow(self, marketSurface):
        rectangle = (self.width//12, self.height//8, 
                    5*self.width//6, 2*self.height//3)
        pygame.draw.rect(marketSurface, (0, 0, 0), rectangle, 5)
        marketSurface.fill((255, 255, 255), rectangle)
        self.drawStockBuy(marketSurface)

    def drawStockSell(self, marketSurface):
        colDis = (5 * self.width // 6 - self.width // 12) // 6
        rowDis = (2 * self.height // 3 - self.height // 8) // 6

        imageX = self.width // 12 + 2 * (5 * self.width//6 - self.width//12) // 5
        imageY = self.height//8
        marketImage = pygame.image.load('sell.png')
        marketImage = pygame.transform.scale(marketImage, (100, 50))
        marketSurface.blit(marketImage, (imageX, imageY))

        font = pygame.font.SysFont('arial', 15, True)
        stockInfo = ['Symbol', 'Price', 'Change', '% Change', 
                    'Market Cap']
        
        for j in range(len(stockInfo)): # draws the table for stocks
            for i in range(6):
                if i == 0:
                    text = font.render(stockInfo[j], 1, (0, 0, 0))
                else:
                    text = font.render(self.stockData[i-1][stockInfo[j]], 1, 
                                    (0, 0, 0))
                marketSurface.blit(text, (3*self.width//24 + colDis * j, 
                                    2*self.height//8 + rowDis * i))

    def createSellButtons(self, rowDis, colDis):
        buttonW, buttonH = colDis, rowDis
        x = 3 * self.width // 24 + colDis * 5

        image = pygame.image.load('sellButton.png')
        image = pygame.transform.scale(image, (buttonW, buttonH))

        for i in range(len(self.stockData)-1):
            button = createThings.Button(image, x, self.height//4+rowDis*(i+1), 
                                        buttonW, buttonH, 
                                        self.stockData[i]['Symbol'])
            self.sellButtons[self.stockData[i]['Symbol']] = button
            button.drawButton(surface)
        '''
        for i in range(len(self.stockData)):
            button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((3*self.width//24 + colDis * 4, 2*self.height//8 + rowDis * i), 
                                                                            (colDis, rowDis)), text='SELL', manager=self.manager)
            self.sellButtons[self.stockData[i]['Symbol']] = button #key=symbol
        '''

    def drawSellWindow(self, marketSurface):
        rectangle = (self.width//12, self.height//8, 
                    5*self.width//6, 2*self.height//3)
        pygame.draw.rect(marketSurface, (0, 0, 0), rectangle, 5)
        marketSurface.fill((255, 255, 255), rectangle)
        self.drawStockSell(marketSurface)

    def drawWallet(self, surface):
        rectangle = (5*self.width//6, 0, self.width, self.height//8)
        pygame.draw.rect(surface, (0, 0, 0), rectangle, 5)
        surface.fill((255, 255, 255), rectangle)
        font = pygame.font.SysFont('arial', 15, True)
        text = font.render("Wallet:" + str(self.protagonist.money), 1,
                            (0, 0, 0))
        surface.blit(text, (5*self.width//6, 0, self.width, self.height//8))
    '''
    def drawInventory(self, surface):
        rectangle = (0, 0, self.width//6, self.height//4)
        pygame.draw.rect(surface, (0, 0, 0), rectangle, 5)
        surface.fill((255, 255, 255), rectangle)
        font = pygame.font.SysFont('arial', 15, True)
        text = font.render("Inventory", 1, (0, 0, 0))
        surface.blit(text, (0, 0, self.width//6, self.height//8))
        print(self.protagonist.inventory)
        if len(self.protagonist.inventory) != 0:
            for stock in self.protagonist.inventory:
                numberString = str(self.protagonist.inventory[stock])
                print(type(numberString))
                symbol = font.render(stock, 1, (0, 0, 0))
                num = font.render(numberString, 1 (0, 0, 0))
                surface.blit(symbol, (0, self.height//8, self.width//12, self.height//4))
                surface.blit(num, (self.width//12, self.height//8, self.width//6, self.height//4))
                '''

    def redrawMarketWindow(self, marketSurface, moveL, moveR, moveF, moveB):
        marketBgImage = pygame.image.load('marketBg.png')
        marketBgImage = pygame.transform.scale(marketBgImage, (self.width, 
                                                                self.height))
        marketSurface.blit(marketBgImage, (0, 0))

        self.drawMarketItem(marketSurface)
        self.drawProtagonist(marketSurface, moveL, moveR, moveF, moveB)

        if not self.exitBuy and self.protagonist.isBuy:
            self.drawBuyWindow(marketSurface)
        elif not self.exitSell and self.protagonist.isSell:
            self.drawSellWindow(marketSurface)

        self.drawWallet(marketSurface)
        #self.drawInventory(marketSurface)
        pygame.display.update()

    def marketDetectCollision(self):
        if ((self.protagonist.hitbox[0] + self.protagonist.hitbox[2] > self.buyDesk.hitbox[0] and self.protagonist.hitbox[0] + self.protagonist.hitbox[2] < self.buyDesk.hitbox[0] + self.buyDesk.hitbox[2])
            and (self.protagonist.hitbox[1] + self.protagonist.hitbox[3] > self.buyDesk.hitbox[1] and self.protagonist.hitbox[1] + self.protagonist.hitbox[3] < self.buyDesk.hitbox[1] + self.buyDesk.hitbox[3])):
            self.protagonist.isBuy, self.protagonist.isCollide = True, True
            self.protagonist.isSell = False
        elif ((self.protagonist.hitbox[0] + self.protagonist.hitbox[2] > self.sellDesk.hitbox[0] and self.protagonist.hitbox[0] + self.protagonist.hitbox[2] < self.sellDesk.hitbox[0] + self.sellDesk.hitbox[2])
            and (self.protagonist.hitbox[1] + self.protagonist.hitbox[3] > self.sellDesk.hitbox[1] and self.protagonist.hitbox[1] + self.protagonist.hitbox[3] < self.sellDesk.hitbox[1] + self.sellDesk.hitbox[3])):
            self.protagonist.isSell, self.protagonist.isCollide = True, True
            self.protagonist.isBuy = False    
        else:
            self.protagonist.isCollide = False

    def buyStocks(self, stockSymbol):
        for stock in self.stockData:
            if stock['Symbol'] == stockSymbol:
                self.protagonist.money -= float(stock['Price'])
        if len(self.protagonist.inventory) == 0:
            self.protagonist.inventory[stockSymbol] = 1
        elif stockSymbol in self.protagonist.inventory:
            self.protagonist.inventory[stockSymbol] += 1
        else:
            self.protagonist.inventory[stockSymbol] = 1

    def sellStocks(self, stock):
        return

    def inMarketRunGame(self):
        marketSurface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Stock Market")
        clock = pygame.time.Clock()

        run = True
        while run:
            print("protagonist's in market")
            clock.tick(30)
            time = clock.tick(30)/1000

            for event in pygame.event.get():
                position = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for stock in self.buyButtons:
                        if self.buyButtons[stock].isClick(position):
                            self.buyStocks(stock)
                    for stock in self.sellButtons:
                        if self.sellButtons[stock].isClick(position):
                            self.sellStocks(stock)
                    
                    '''
                    if event.user_type == 'ui_button_pressed':
                        for stock in self.buyButtons:
                            if event.ui_element == self.buyButtons[stock]:
                                self.buyStocks(stock)

                        for stock in self.sellButtons:
                            if event.ui_element == self.sellButtons[stock]:
                                self.sellStocks(stock)
                    '''
                self.manager.process_events(event)

            self.manager.update(time)
            self.manager.draw_ui(marketSurface)

            keys = pygame.key.get_pressed()
            (moveL, moveR, moveF, moveB) = self.detectKeyPressed(keys)

            self.marketDetectCollision()
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

