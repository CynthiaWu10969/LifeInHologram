'''
Images Citations: 
spritesheet: https://p1.hiclipart.com/preview/53/364/990/julian-assange-sprite-sheet-png-clipart-thumbnail.jpg 
bank: https://www.usnews.com/dims4/USNEWS/f38e0dd/2147483647/thumbnail/640x420/quality/85/?url=http%3A%2F%2Fcom-usnews-beam-media.s3.amazonaws.com%2Fa7%2F6a%2F462f637342bd88cfa75247b89bea%2F190412-bank-stock.jpg 
buyDesk: http://trust-sys.com/trust-sys.com/wp-content/uploads/2016/04/trust-accounting.png
buyIcon: https://www.cobratrading.com/wp-content/uploads/2018/05/buy-300x292.png 
depositIcon: https://static.thenounproject.com/png/878634-200.png 
door: https://cdn2.iconfinder.com/data/icons/firefighting-fire-safety/64/44_fireproof-doors-512.png
grass: https://image.shutterstock.com/image-vector/grass-icon-silhouette-green-plants-260nw-1009568566.jpg
home: https://tinyurl.com/re5kt4j
homeBg.png: http://silveiraneto.net/wp-content/uploads/2008/08/silveira_neto_gpl_pixelart_kitchen_home1.png 
market: https://cdn.iconscout.com/icon/premium/png-512-thumb/bank-280-184759.png
marketIcon: https://cdn1.iconfinder.com/data/icons/stock-market-2/100/Stock_Market_Finance_Money_Banking_Stocks_Shares_Commerce_Business-40-512.png
minusIcon: https://cdn2.iconfinder.com/data/icons/round-mobile-ui-set/512/minus-stop-erase-cut-mobile-function-512.png
plusIcon: https://image.shutterstock.com/image-vector/plus-icon-vector-illustration-add-260nw-1478720975.jpg
sellDesk: https://cdn.iconscout.com/icon/premium/png-256-thumb/receptionist-desk-2-1166448.png 
sellIcon: https://mmbiz.qpic.cn/mmbiz_png/tbyoduyMj0dhA2wCZoYncGjeE06j9Hns1Q16TQVILichOtKGebDjuYIPJVnGUianVdqJOKnJgUXhzCJozCzaeLPw/640?wx_fmt=png
workDesk: https://cdn.dribbble.com/users/944703/screenshots/3354467/____-01-01.jpg
workImage: https://cdn.dribbble.com/users/147557/screenshots/3490991/office-icon.jpg 
workplace: https://png.pngtree.com/png-vector/20190119/ourlarge/pngtree-2-5d-building-2-5d-bungalow-building-bungalow-png-image_474133.jpg 
helpBg: https://www.fg-a.com/wallpapers/white-marble-1-2018.jpg 
'''

import pygame
import webScraping
import createThings
import graphics
import string
import random
import instructionPage

def almostEqual(d1, d2, epsilon=10**-7): #from 15112 hw file
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

class PlayGame(object):
    def __init__(self, width, height):
        self.startGame = False
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
        self.buyButtons, self.sellButtons = dict(), dict()
        self.exitBuyButton, self.exitSellButton, exitDepositButton = None, None, None
        self.createDoor()
        self.moneyForDeposit, self.monthForWithdraw = 1000, 0
        self.bankDesk, self.workDesk = None, None
        self.interest = round(random.uniform(0.5, 0.9), 2) #in percentage
        self.depositPlus, self.depositMinus = None, None #these are buttons
        self.withdrawPlus, self.withdrawMinus = None, None
        self.depositButton = None
        self.startDeposit, self.depositTime, self.moneyForWithdraw = 0, 0, 0
        self.enterGame, self.isHelp = False, False
        self.timerForExpense, self.timer, self.startDepositTime = 0, 0, 0
        self.homeDesk = None
        self.currentStock = dict() #a dictionary of dictionaries
        self.stockTimer = 0
        invImage = pygame.image.load('buyButton.png')
        self.invButton = createThings.Button(invImage, 0, 0, self.width//6, self.height//4, 'inv button')
        self.wholeData = webScraping.scraping() #list of dicts
        self.stockData = self.wholeData[:6]
        self.wholeStockDict = dict() # convert the stock data into a dict of dicts
        for stock in self.wholeData:
            self.wholeStockDict[stock['Symbol']] = stock

    def redrawWholeInventory(self, surface):
        invBg = createThings.Background('invBg.png', 'inventory')
        invBg.drawBg(surface)

        colDis = (5 * self.width // 6 - self.width // 12) // 6 + 30
        rowDis = (2 * self.height // 3 - self.height // 8) // 6

        font = pygame.font.SysFont('arial', 35, True)
        text = font.render('INVENTORY', 1, (255, 255, 255)) #white
        surface.blit(text, (self.width//3, self.height//8))

        if len(self.protagonist.inventory) == 0:
            font = pygame.font.SysFont('arial', 25, True)
            text = font.render('Inventory is empty! Invest in some stocks!', 1, (255, 255, 255)) #white
            surface.blit(text, (self.width//10, self.height//3))
        else:
            invInfo = dict()

            for stock in self.protagonist.inventory:
                if stock not in invInfo:
                    if stock in self.wholeStockDict:
                        invInfo[stock] = self.wholeStockDict[stock]
                    else: #如果刷新的stock data里面没有这支stock
                        invInfo[stock] = self.currentStock[stock]
            #print('inventory info: ', invInfo)

            font = pygame.font.SysFont('arial', 15, True)

            stockInfo = ['Symbol', 'Price', 'Change', '% Change', 
                        'Market Cap', 'Shares Hold']

            invKeys = list(self.protagonist.inventory.keys()) # stock symbols
            for j in range(len(stockInfo)): # draws the table for stocks
                for i in range(len(invKeys)):
                    if i == 0:
                        text = font.render(stockInfo[j], 1, (255, 255, 255)) #info row 
                    else:
                        if j == len(stockInfo) - 1:
                            text = font.render(str(self.protagonist.inventory[invKeys[i]]), 1, (255, 255, 255))
                        else:
                            if j == 2 or j == 3:
                                if invInfo[invKeys[i]][stockInfo[j]][0] == '-':
                                    color = (255, 50, 58)
                                else:
                                    color = (0, 153, 51)
                            else:
                                color = (255, 255, 255)
                            text = font.render(invInfo[invKeys[i]][stockInfo[j]], 1, 
                                            color)
                    surface.blit(text, (3*self.width//24 + colDis * j, 
                                        2*self.height//8 + rowDis * i))

        pygame.display.update()

    def runWholeInventory(self, surface):
        invSurface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Inventory")
        clock = pygame.time.Clock()

        run = True
        while run:
            clock.tick(15)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True
                    else:
                        return False
                    
            self.updateWebScraping()
            self.redrawWholeInventory(invSurface)

    def detectClickInvButton(self, position, surface):
        if self.invButton.isClick(position):
            self.runWholeInventory(surface)

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

    def drawFixedItems(self, surface):
        self.drawDoor(surface)
        self.drawWallet(surface)
        self.drawInventory(surface)

    def createMarketItems(self):
        self.buyDesk = createThings.Item('buyDesk.png', 4*self.width//6, self.height//5, 
                            150, 150, 'buy desk')
        self.sellDesk = createThings.Item('sellDesk.png', self.width//8, self.height//5, 
                            120, 150, 'sell desk')
        self.buyIcon = createThings.Item('buyIcon.png', 4*self.width//6, self.height//10, 
                            50, 50, 'buy icon')
        self.sellIcon = createThings.Item('sellIcon.png', self.width//6, self.height//10, 
                            50, 50, 'sell icon')
        self.marketIcon = createThings.Item('marketIcon.png', self.width//2-30, self.height//8, 
                                50, 50, 'market icon')

    def detectCollision(self): #hitbox: (left top)x, y, width, height 
        if ((self.protagonist.hitbox[0] + self.protagonist.hitbox[2] > self.market.hitbox[0] and self.protagonist.hitbox[0] + self.protagonist.hitbox[2] < self.market.hitbox[0] + self.market.hitbox[2])
            and (self.protagonist.hitbox[1] + self.protagonist.hitbox[3] > self.market.hitbox[1] and self.protagonist.hitbox[1] + self.protagonist.hitbox[3] < self.market.hitbox[1] + self.market.hitbox[3])):
            self.protagonist.inMarket, self.protagonist.isCollide = True, True
        elif ((self.protagonist.hitbox[0] + self.protagonist.hitbox[2] > self.bank.hitbox[0] and self.protagonist.hitbox[0] + self.protagonist.hitbox[2] < self.bank.hitbox[0] + self.bank.hitbox[2])
            and (self.protagonist.hitbox[1] + self.protagonist.hitbox[3] > self.bank.hitbox[1] and self.protagonist.hitbox[1] + self.protagonist.hitbox[3] < self.bank.hitbox[1] + self.bank.hitbox[3])):
            self.protagonist.inBank, self.protagonist.isCollide = True, True
        elif ((self.protagonist.hitbox[0] + self.protagonist.hitbox[2] > self.workplace.hitbox[0] and self.protagonist.hitbox[0] + self.protagonist.hitbox[2] < self.workplace.hitbox[0] + self.workplace.hitbox[2])
            and (self.protagonist.hitbox[1] + self.protagonist.hitbox[3] > self.workplace.hitbox[1] and self.protagonist.hitbox[1] + self.protagonist.hitbox[3] < self.workplace.hitbox[1] + self.workplace.hitbox[3])):
            self.protagonist.isCollide, self.protagonist.inWork = True, True
        elif ((self.protagonist.hitbox[0] + self.protagonist.hitbox[2] > self.home.hitbox[0] and self.protagonist.hitbox[0] + self.protagonist.hitbox[2] < self.home.hitbox[0] + self.home.hitbox[2])
            and (self.protagonist.hitbox[1] + self.protagonist.hitbox[3] > self.home.hitbox[1] and self.protagonist.hitbox[1] + self.protagonist.hitbox[3] < self.home.hitbox[1] + self.home.hitbox[3])):
            self.protagonist.isCollide, self.protagonist.inHome = True, True
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

    def drawStItem(self, stSurface):
        for item in self.itemList:
            stSurface.blit(item.image, (item.x, item.y))

    def doExpense(self):
        #currentTime = pygame.time.get_ticks()
        #print('time:', currentTime)
        if self.timerForExpense >= 15:
            self.protagonist.money -= 2500
            self.timerForExpense = 0

    def redrawStreetWindow(self, stSurface, moveL, moveR, moveF, moveB):
        stSurface.blit(self.streetBackground.image, (0, 0))

        self.drawStItem(stSurface)
        graphics.drawPeople(stSurface, self.width, self.height)
        self.drawProtagonist(stSurface, moveL, moveR, moveF, moveB)
        
        self.drawWallet(stSurface)
        self.drawInventory(stSurface)
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
        #print("current moving direction: ", direction)

        if self.protagonist.isCollide:
            self.cancelMove(direction)

    def drawMarketItem(self, marketSurface):
        for item in self.marketItems:
            marketSurface.blit(item.image, (item.x, item.y))
        

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
                    if j == 2 or j == 3:
                        if self.stockData[i-1][stockInfo[j]][0] == '-':
                            color = (255, 50, 58)
                        else:
                            color = (0, 153, 51)
                    else:
                        color = (0, 0, 0)
                    text = font.render(self.stockData[i-1][stockInfo[j]], 1, 
                                    color)
                marketSurface.blit(text, (3*self.width//24 + colDis * j, 
                                    2*self.height//8 + rowDis * i))
        self.createBuyButtons(marketSurface, colDis, rowDis)

    def createBuyButtons(self, surface, colDis, rowDis):
        buttonW, buttonH = colDis, rowDis
        x = 3 * self.width // 24 + colDis * 5

        image = pygame.image.load('buyButton.png')
        image = pygame.transform.scale(image, (buttonW, buttonH))

        for i in range(len(self.stockData)-1):
            button = createThings.Button(image, x, self.height//4+rowDis*(i+1)-5, 
                                        buttonW, buttonH, 
                                        self.stockData[i]['Symbol'])
            self.buyButtons[self.stockData[i]['Symbol']] = button
            button.drawButton(surface)

        image = pygame.image.load('exitButton.png')
        image = pygame.transform.scale(image, (10, 10))
        self.exitBuyButton = createThings.Button(image, 0, 11*self.height//12, 20, 20)
        self.exitBuyButton.drawButton(surface)
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
        self.createSellButtons(marketSurface, rowDis, colDis)

        imageX = self.width // 12 + 2 * (5 * self.width//6 - self.width//12) // 5
        imageY = self.height//8
        marketImage = pygame.image.load('sell.png')
        marketImage = pygame.transform.scale(marketImage, (100, 50))
        marketSurface.blit(marketImage, (imageX, imageY))

        font = pygame.font.SysFont('arial', 15, True)
        stockInfo = ['Symbol', 'Price', 'Change', '% Change', 
                    'Market Cap']
        
        if len(self.protagonist.inventory) == 0:
            font = pygame.font.SysFont('arial', 20, True)
            text = font.render("You haven't purchased any stocks yet!", 1, (0, 0, 0))
            marketSurface.blit(text, (self.width//6, self.height//3))
            for button in self.sellButtons:
                self.sellButtons[button] = None

        invKeys = list(self.protagonist.inventory.keys()) #stock symbols
        for j in range(len(stockInfo)): 
            # draws the table for stocks
            for i in range(len(invKeys)):
                if i == 0:
                    text = font.render(stockInfo[j], 1, (0, 0, 0))
                else:
                    if invKeys[i] in self.wholeStockDict:
                        inUse = self.wholeStockDict
                    else:
                        inUse = self.currentStock
                    if j == 2 or j == 3:
                        if inUse[invKeys[i]][stockInfo[j]][0] == '-':
                            color = (255, 50, 58)
                        else:
                            color = (0, 153, 51)
                    else:
                        color = (0, 0, 0)
                    text = font.render(inUse[invKeys[i]][stockInfo[j]], 
                                        1, color)
                marketSurface.blit(text, (3*self.width//24 + colDis * j, 
                                    2*self.height//8 + rowDis * i))

    def createSellButtons(self, surface, rowDis, colDis):
        buttonW, buttonH = colDis, rowDis
        x = 3 * self.width // 24 + colDis * 5

        image = pygame.image.load('sellButton.png')
        image = pygame.transform.scale(image, (buttonW, buttonH))

        keys = list(self.protagonist.inventory.keys()) #list of stock symbols
        for i in range(len(keys)):
            button = createThings.Button(image, x, self.height//4+rowDis*(i+1)-5, 
                                        buttonW, buttonH, keys[i])
            self.sellButtons[keys[i]] = button
            button.drawButton(surface)

        image = pygame.image.load('exitButton.png')
        image = pygame.transform.scale(image, (10, 10))
        self.exitSellButton = createThings.Button(image, 0, 11*self.height//12, 20, 20)
        self.exitSellButton.drawButton(surface)
        '''
        for i in range(len(self.stockData)):
            button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((3*self.width//24 + colDis * 4, 2*self.height//8 + rowDis * i), 
                                                                            (colDis, rowDis)), text='SELL', manager=self.manager)
            self.sellButtons[self.stockData[i]['Symbol']] = button #key=symbol
        '''

    def drawSellWindow(self, marketSurface):
        for stock in self.buyButtons:
            self.buyButtons[stock] = None
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
        text = font.render("Wallet:" + str(round(self.protagonist.money, 2)), 1,
                            (0, 0, 0))
        surface.blit(text, (5*self.width//6, 0, self.width, self.height//8))
    
    def drawInventory(self, surface):
        rectangle = (0, 0, self.width//6, self.height//4)
        pygame.draw.rect(surface, (0, 0, 0), rectangle, 5)
        surface.fill((255, 255, 255), rectangle)
        font = pygame.font.SysFont('arial', 15, True)
        text = font.render("Inventory", 1, (0, 0, 0))
        surface.blit(text, (0, 0, self.width//6, self.height//8))
        font = pygame.font.SysFont('arial', 10, True)
        if len(self.protagonist.inventory) != 0:
            keys = []
            for key in self.protagonist.inventory.keys():
                keys.append(key)
            for i in range(len(keys)):
                symbol = font.render(keys[i], 1, (0, 0, 0))
                surface.blit(symbol, (0, self.height//16+i*self.height//32, 
                                        self.width//12, 
                                        self.height//16+(i+1)*self.height//32))
                numShares = str(self.protagonist.inventory[keys[i]])
                num = font.render(numShares, 1, (0, 0, 0))
                surface.blit(num, (self.width//12, 
                                    self.height//16+i*self.height//32, 
                                    self.width//6, 
                                    self.height//16+(i+1)*self.height//32))
                
    def createDoor(self):
        self.door = createThings.Item('door.png', self.width//2, 22*self.height//24, 
                                            80, 30, 'door')

    def drawDoor(self, surface):
        surface.blit(self.door.image, (self.door.x, self.door.y))

    def redrawMarketWindow(self, marketSurface, moveL, moveR, moveF, moveB):
        self.exitBuyButton = None
        self.exitSellButton = None
        marketBgImage = pygame.image.load('marketBg.png')
        marketBgImage = pygame.transform.scale(marketBgImage, (self.width, 
                                                                self.height))
        marketSurface.blit(marketBgImage, (0, 0))

        self.drawMarketItem(marketSurface)
        self.drawProtagonist(marketSurface, moveL, moveR, moveF, moveB)

        if not self.protagonist.exitBuy and self.protagonist.isBuy:
            self.drawBuyWindow(marketSurface)
        if not self.protagonist.exitSell and self.protagonist.isSell:
            self.drawSellWindow(marketSurface)

        self.drawFixedItems(marketSurface)
        pygame.display.update()

    def marketDetectCollision(self, run):
        if ((self.protagonist.hitbox[0] + self.protagonist.hitbox[2] > self.buyDesk.hitbox[0] and self.protagonist.hitbox[0] + self.protagonist.hitbox[2] < self.buyDesk.hitbox[0] + self.buyDesk.hitbox[2])
            and (self.protagonist.hitbox[1] + self.protagonist.hitbox[3] > self.buyDesk.hitbox[1] and self.protagonist.hitbox[1] + self.protagonist.hitbox[3] < self.buyDesk.hitbox[1] + self.buyDesk.hitbox[3])):
            self.protagonist.isBuy, self.protagonist.isCollide = True, True
            self.protagonist.isSell = False
        elif ((self.protagonist.hitbox[0] + self.protagonist.hitbox[2] > self.sellDesk.hitbox[0] and self.protagonist.hitbox[0] + self.protagonist.hitbox[2] < self.sellDesk.hitbox[0] + self.sellDesk.hitbox[2])
            and (self.protagonist.hitbox[1] + self.protagonist.hitbox[3] > self.sellDesk.hitbox[1] and self.protagonist.hitbox[1] + self.protagonist.hitbox[3] < self.sellDesk.hitbox[1] + self.sellDesk.hitbox[3])):
            self.protagonist.isSell, self.protagonist.isCollide = True, True
            self.protagonist.isBuy = False
        else:
            self.protagonist.isCollide, self.protagonist.isBuy, self.protagonist.isSell = False, False, False
        if ((self.protagonist.hitbox[0] + self.protagonist.hitbox[2] > self.door.hitbox[0] and self.protagonist.hitbox[0] + self.protagonist.hitbox[2] < self.door.hitbox[0] + self.door.hitbox[2])
            and (self.protagonist.hitbox[1] + self.protagonist.hitbox[3] > self.door.hitbox[1] and self.protagonist.hitbox[1] + self.protagonist.hitbox[3] < self.door.hitbox[1] + self.door.hitbox[3])):
            run = False
        return run

    def buyStocks(self, stockSymbol):
        for stock in self.stockData:
            if stock['Symbol'] == stockSymbol:
                self.protagonist.money -= float(stock['Price'])
                if stockSymbol not in self.currentStock:
                    info = {'Price': stock['Price'], 'Change': stock['Change'], 
                            '% Change': stock['% Change'], 
                            'Market Cap': stock['Market Cap']}
                    self.currentStock[stockSymbol] = info
        if stockSymbol in self.protagonist.inventory:
            self.protagonist.inventory[stockSymbol] += 1
        else:
            self.protagonist.inventory[stockSymbol] = 1
        #print("inventory: ", self.protagonist.inventory)
        #print('current stock:', self.currentStock)
    #def marketErrorScreen(self):

    def sellStocks(self, targetStock):
        for i in range(len(self.wholeData)):
            if self.wholeData[i]['Symbol'] == targetStock:
                if targetStock in self.protagonist.inventory:
                    self.protagonist.money += float(self.wholeData[i]['Price'])
                    if self.protagonist.inventory[targetStock] > 1:
                        self.protagonist.inventory[targetStock] -= 1
                    else:
                        del self.protagonist.inventory[targetStock]
                else:
                    return
                    #self.marketErrorScreen() you dont have this in inventory

    def detectMarketMouseEvents(self, position):
        for stock in self.buyButtons:
            if (self.buyButtons[stock] != None and 
                self.buyButtons[stock].isClick(position)):
                self.buyStocks(stock)
        for stock in self.sellButtons:
            if (self.sellButtons[stock] != None and 
                self.sellButtons[stock].isClick(position)):
                self.sellStocks(stock)
        if self.exitBuyButton != None and self.exitBuyButton.isClick(position):
            self.protagonist.exitBuy = True
            for stock in self.buyButtons:
                self.buyButtons[stock] = None #clear the buttons when exiting
        else:
            self.protagonist.exitBuy = False
        if self.exitSellButton != None and self.exitSellButton.isClick(position):
            self.protagonist.exitSell = True
            for stock in self.sellButtons:
                self.sellButtons[stock] = None #clear the buttons when exiting
        else:
            self.protagonist.exitSell = False

    def createBankItems(self):
        self.bankDesk = createThings.Item('bankDesk.png', 4*self.width//6, 
                                        self.height//5, 150, 150, 'bank desk')

    def drawBankItems(self, surface):
        self.createBankItems()
        self.bankDesk.drawItem(surface)

        rectangle = (self.width//6, self.height//8, 
                    3*self.width//7, self.height//5)
        pygame.draw.rect(surface, (0, 0, 0), rectangle, 5)
        surface.fill((0, 128, 129), rectangle)
        font = pygame.font.SysFont('arial', 25, True)
        text = font.render('WELCOME TO BANK', 1, (0, 0, 0))
        surface.blit(text, (self.width//6, self.height//8))
        
        font = pygame.font.SysFont('arial', 15, True)
        text = font.render(f'The current interest rate is {self.interest}%', 1, 
                            (0, 0, 0))
        surface.blit(text, (self.width//6, self.height//4))

    def redrawBankWindow(self, bankSurface, moveL, moveR, moveF, moveB):
        self.exitDepositButton = None
        bankBg = createThings.Background('bankBg.png', 'bank')
        bankBg.drawBg(bankSurface)

        self.drawBankItems(bankSurface)
        self.drawProtagonist(bankSurface, moveL, moveR, moveF, moveB)

        self.drawFixedItems(bankSurface)

        if self.protagonist.isDeposit:
            self.createBankWindow(bankSurface)

        pygame.display.update()

    def drawDepositWindow(self, surface):
        font = pygame.font.SysFont('arial', 15, True)
        money = round(self.protagonist.money, 2)
        text = font.render(f'Your current balance is {money}.', 1, (0, 0, 0))
        surface.blit(text, (self.width//12, self.height//3))

        image = pygame.image.load('minus.png')
        self.depositMinus = createThings.Button(image, self.width//11, self.height//2,
                                    30, 30)
        self.depositMinus.drawButton(surface)

        image = pygame.image.load('plus.png')
        self.depositPlus = createThings.Button(image, self.width//3, self.height//2, 
                                    30, 30)
        self.depositPlus.drawButton(surface)

        font = pygame.font.SysFont('arial', 20, True)
        text = font.render(f'{self.moneyForDeposit}', 1, (0, 0, 0))
        surface.blit(text, (self.width//5, self.height//2+5))

        image = pygame.image.load('deposit.png')
        self.depositButton = createThings.Button(image, self.width//2, 
                                                2*self.height//3, 40, 40)
        self.depositButton.drawButton(surface)

    def drawWithdrawWindow(self, surface):
        font = pygame.font.SysFont('arial', 15, True)
        text = font.render(f'Your current deposit is {self.protagonist.deposit}.', 1, (0, 0, 0))
        surface.blit(text, (6*self.width//12, self.height//4))

        font = pygame.font.SysFont('arial', 15, True)
        text = font.render(f'Current interest rate is {self.interest}.', 1, (0, 0, 0))
        surface.blit(text, (self.width//2, self.height//3))

        font = pygame.font.SysFont('arial', 15, True)
        text = font.render('When would you like to withdraw?', 1, (0, 0, 0))
        surface.blit(text, (self.width//2, self.height//3+20))

        image = pygame.image.load('minus.png')
        self.withdrawMinus = createThings.Button(image, self.width//2+self.width//11, self.height//2,
                                    30, 30)
        self.withdrawMinus.drawButton(surface)

        image = pygame.image.load('plus.png')
        self.withdrawPlus = createThings.Button(image, self.width//2+self.width//3, self.height//2, 
                                    30, 30)
        self.withdrawPlus.drawButton(surface)

        font = pygame.font.SysFont('arial', 20, True)
        text = font.render(f'{self.monthForWithdraw}', 1, (0, 0, 0))
        surface.blit(text, (self.width//2+self.width//5, self.height//2+5))

        '''
        image = pygame.image.load('withdraw.png')
        self.withdrawButton = createThings.Button(image, self.width//2+self.width//5, 
                                                2*self.height//3, 40, 40)
        self.withdrawButton.drawButton(surface)
        '''

    def createBankWindow(self, surface):
        rectangle = (self.width//12, self.height//8, 
                    5*self.width//6, 2*self.height//3)
        pygame.draw.rect(surface, (0, 0, 0), rectangle, 5)
        surface.fill((255, 255, 255), rectangle)

        font = pygame.font.SysFont('arial', 20, True)
        text = font.render('Would you like to ...', 1, (0, 0, 0))
        surface.blit(text, (self.width//3, self.height//7))

        font = pygame.font.SysFont('arial', 20, True)
        text = font.render('Deposit', 1, (0, 0, 0))
        surface.blit(text, (self.width//12, self.height//4))
        self.drawDepositWindow(surface)
        self.drawWithdrawWindow(surface)

        image = pygame.image.load('exitButton.png')
        image = pygame.transform.scale(image, (10, 10))
        self.exitDepositButton = createThings.Button(image, 0, 11*self.height//12, 20, 20)
        self.exitDepositButton.drawButton(surface)

    def bankDetectCollision(self, run):
        self.protagonist.isCollide = False
        if ((self.protagonist.hitbox[0] + self.protagonist.hitbox[2] > self.bankDesk.hitbox[0] and self.protagonist.hitbox[0] + self.protagonist.hitbox[2] < self.bankDesk.hitbox[0] + self.bankDesk.hitbox[2])
            and (self.protagonist.hitbox[1] + self.protagonist.hitbox[3] > self.bankDesk.hitbox[1] and self.protagonist.hitbox[1] + self.protagonist.hitbox[3] < self.bankDesk.hitbox[1] + self.bankDesk.hitbox[3])):
            self.protagonist.isDeposit, self.protagonist.isCollide = True, True
        else:
            self.protagonist.isDeposit, self.protagonist.isCollide = False, False
        if ((self.protagonist.hitbox[0] + self.protagonist.hitbox[2] > self.door.hitbox[0] and self.protagonist.hitbox[0] + self.protagonist.hitbox[2] < self.door.hitbox[0] + self.door.hitbox[2])
            and (self.protagonist.hitbox[1] + self.protagonist.hitbox[3] > self.door.hitbox[1] and self.protagonist.hitbox[1] + self.protagonist.hitbox[3] < self.door.hitbox[1] + self.door.hitbox[3])):
            run = False
        return run

    def changeInterest(self):
        time = pygame.time.get_ticks()
        if time % 15000 == 0:
            self.interest = round(random.uniform(0.5, 0.9), 2)

    def createDeposit(self):
        self.protagonist.deposit += self.moneyForDeposit

        compoundInterest = 1 + self.interest / 100
        self.moneyForWithdraw = self.protagonist.deposit*compoundInterest**self.monthForWithdraw
        self.depositTime = self.monthForWithdraw * 15 #correct in secs
        #print('secs:', self.depositTime)
        #print(self.moneyForWithdraw) 
        ########################money correct############################

        self.protagonist.money -= self.moneyForDeposit
        self.moneyForDeposit = 1000
        self.monthForWithdraw = 0

    #def bankErrorScreen(self):

    def detectBankMouseEvents(self, position):
        if self.exitDepositButton != None and self.exitDepositButton.isClick(position):
            self.protagonist.isDeposit, self.protagonist.exitDeposit = False, True
            depositButtons = [self.depositMinus, self.depositPlus, self.depositButton, self.withdrawMinus, self.withdrawPlus]
            for i in range(len(depositButtons)):
                depositButtons[i] = None
        else:
            self.protagonist.exitDeposit = False
        if (self.protagonist.isDeposit and self.depositPlus != None and 
            self.depositPlus.isClick(position)):
            if self.moneyForDeposit < self.protagonist.money:
                self.moneyForDeposit += 1000
            else:
                return 
                # self.bankErrorScreen()
        elif (self.protagonist.isDeposit and self.depositMinus != None and 
            self.depositMinus.isClick(position)):
            if self.moneyForDeposit >= 1000:
                self.moneyForDeposit -= 1000
            else:
                return
        
        if self.protagonist.isDeposit and self.withdrawPlus.isClick(position):
            if self.monthForWithdraw < 12:
                self.monthForWithdraw += 1
            else:
                return
                # self.bankErrorScreen()
        elif self.protagonist.isDeposit and self.withdrawMinus.isClick(position):
            if self.monthForWithdraw > 1:
                self.monthForWithdraw -= 1
            else:
                return
        
        if self.protagonist.isDeposit and self.monthForWithdraw >= 1 and self.depositButton.isClick(position):
            self.startDepositTime = self.timer
            self.startDeposit = pygame.time.get_ticks()
            self.createDeposit()
        
        #我他妈debug不出来啊我日

    def withdrawMoney(self):
        if self.depositTime == 0:
            return
        else:
            #print('start deposit time: ', self.startDepositTime)
            #print('timer: ', self.timer)
            #对了
            if self.timer >= self.startDepositTime + self.depositTime:
                self.protagonist.money += self.moneyForWithdraw
                self.moneyForWithdraw = 0
                self.startDepositTime, self.depositTime = 0, 0
                return

    def inBankRunGame(self):
        bankSurface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Bank")
        clock = pygame.time.Clock()

        run = True
        while run:
            #print("protagonist's in bank")
            clock.tick(15)
 
            self.withdrawMoney()

            #self.updateWebScraping()

            self.timerForExpense += 0.06666666666666666
            self.timer += 0.06666666666666666
            self.stockTimer += 0.06666666666666666

            for event in pygame.event.get():
                position = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.detectBankMouseEvents(position)
                    self.detectClickInvButton(position, bankSurface)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        self.isHelp = True

            keys = pygame.key.get_pressed()
            (moveL, moveR, moveF, moveB) = self.detectKeyPressed(keys)

            self.checkDirectForCollision(moveL, moveR, moveF, moveB)

            self.doExpense()
            self.changeInterest()
            self.redrawBankWindow(bankSurface, moveL, moveR, moveF, moveB)
            run = self.bankDetectCollision(run)

            if self.isHelp:
                self.runHelpPage()

            if self.protagonist.money <= 0:
                run = self.gameOver()
                if run:
                    self.protagonist.inBank = False
                    self.protagonist.money = 20000
                    return

        self.protagonist.inBank = False
        self.protagonist.x = self.bank.hitbox[0] + self.bank.hitbox[2] // 2
        self.protagonist.y = self.bank.hitbox[1] + self.bank.hitbox[3]
        return

    def updateWebScraping(self):
        if self.protagonist.isBuy or self.protagonist.isSell:
            if self.stockTimer >= 1:
                self.wholeData = webScraping.scraping()
                self.stockData = self.wholeData[:6]
                self.stockTimer = 0

    def inMarketRunGame(self):
        marketSurface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Stock Market")
        clock = pygame.time.Clock()

        run = True
        while run:
            #print("protagonist's in market")
            clock.tick(30)
            time = clock.tick(30)/1000

            #self.updateWebScraping()

            for event in pygame.event.get():
                position = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.detectMarketMouseEvents(position)
                    self.detectClickInvButton(position, marketSurface)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        self.isHelp = True
                    
            self.timerForExpense += 0.06666666666666666
            self.timer += 0.06666666666666666
            self.stockTimer += 0.06666666666666666

            keys = pygame.key.get_pressed()
            (moveL, moveR, moveF, moveB) = self.detectKeyPressed(keys)

            self.checkDirectForCollision(moveL, moveR, moveF, moveB)

            self.doExpense()
            self.redrawMarketWindow(marketSurface, moveL, moveR, moveF, moveB)
            run = self.marketDetectCollision(run)
        
            if self.isHelp:
                self.runHelpPage()

            if self.protagonist.money <= 0:
                run = self.gameOver()
                if run:
                    self.protagonist.inMarket = False
                    self.protagonist.money = 20000
                    return

        self.protagonist.inMarket = False
        self.protagonist.x = self.market.hitbox[0] + self.market.hitbox[2] // 2
        self.protagonist.y = self.market.hitbox[1] + self.market.hitbox[3]
        return

    def createWorkItems(self):
        self.workDesk = createThings.Item('workDesk.png', self.width//3, 
                                        self.height//4, 180, 120, 'work desk')

    def drawWorkItems(self, surface):
        self.createWorkItems()
        self.workDesk.drawItem(surface)

    def drawReceiveWork(self, surface):
        rectangle = (self.width//6, self.height//8, 
                    self.width//6+400, self.height//8+200)
        receiveWork = createThings.Item('workImage.png', self.width//6, 
                                        self.height//8, 400, 200, 'work image')
        receiveWork.drawItem(surface)

    def redrawWorkWindow(self, workSurface, moveL, moveR, moveF, moveB):
        workBg = createThings.Background('workBg.png', 'workplace')
        #print('work bg:', workBg.name)
        workBg.drawBg(workSurface)

        self.drawWorkItems(workSurface)
        self.drawFixedItems(workSurface)
        self.drawProtagonist(workSurface, moveL, moveR, moveF, moveB)

        if self.protagonist.isReceiveWork:
            self.drawReceiveWork(workSurface)

        pygame.display.update()

    def workDetectCollision(self, run):
        self.protagonist.isCollide = False
        if ((self.protagonist.hitbox[0] + self.protagonist.hitbox[2] > self.workDesk.hitbox[0] and self.protagonist.hitbox[0] + self.protagonist.hitbox[2] < self.workDesk.hitbox[0] + self.workDesk.hitbox[2])
            and (self.protagonist.hitbox[1] + self.protagonist.hitbox[3] > self.workDesk.hitbox[1] and self.protagonist.hitbox[1] + self.protagonist.hitbox[3] < self.workDesk.hitbox[1] + self.workDesk.hitbox[3])):
            self.protagonist.isReceiveWork, self.protagonist.isCollide = True, True
        if ((self.protagonist.hitbox[0] + self.protagonist.hitbox[2] > self.door.hitbox[0] and self.protagonist.hitbox[0] + self.protagonist.hitbox[2] < self.door.hitbox[0] + self.door.hitbox[2])
            and (self.protagonist.hitbox[1] + self.protagonist.hitbox[3] > self.door.hitbox[1] and self.protagonist.hitbox[1] + self.protagonist.hitbox[3] < self.door.hitbox[1] + self.door.hitbox[3])):
            run = False
        return run

    def detectWorkMouseEvents(self, position):
        return

    def inWorkRunGame(self):
        workSurface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Workplace")
        clock = pygame.time.Clock()

        run = True
        while run:
            clock.tick(15)

            self.timerForExpense += 0.06666666666666666
            self.timer += 0.06666666666666666
            self.stockTimer += 0.06666666666666666
 
            for event in pygame.event.get():
                position = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.detectWorkMouseEvents(position)
                    self.detectClickInvButton(position, workSurface)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        self.isHelp = True

            keys = pygame.key.get_pressed()
            (moveL, moveR, moveF, moveB) = self.detectKeyPressed(keys)

            self.checkDirectForCollision(moveL, moveR, moveF, moveB)

            self.redrawWorkWindow(workSurface, moveL, moveR, moveF, moveB)
            run = self.workDetectCollision(run)

            if self.isHelp:
                self.runHelpPage()

            if self.protagonist.money <= 0:
                run = self.gameOver()
                if run:
                    self.protagonist.inWork = False
                    self.protagonist.money = 20000
                    return

        self.protagonist.inWork = False
        self.protagonist.x = self.workplace.hitbox[0] + self.workplace.hitbox[2] // 2
        self.protagonist.y = self.workplace.hitbox[1] + self.workplace.hitbox[3]
        return

    def detectHomeMouseEvents(self, position):
        return

    def createHomeItems(self, surface):
        self.homeDesk = createThings.Item('workDesk.png', 11*self.width//13, 
                                        11*self.height//14, 30, 60, 'home desk')

    def redrawHomeWindow(self, homeSurface, moveL, moveR, moveF, moveB):
        homeBg = createThings.Background('homeBg.png', 'home')
        homeBg.drawBg(homeSurface)

        self.createHomeItems(homeSurface)
        self.drawProtagonist(homeSurface, moveL, moveR, moveF, moveB)
        self.drawWallet(homeSurface)
        self.drawInventory(homeSurface)

        pygame.display.update()

    def homeDetectCollision(self, run):
        self.protagonist.isCollide = False
        '''
        if ((self.protagonist.hitbox[0] + self.protagonist.hitbox[2] > self.workDesk.hitbox[0] and self.protagonist.hitbox[0] + self.protagonist.hitbox[2] < self.workDesk.hitbox[0] + self.workDesk.hitbox[2])
            and (self.protagonist.hitbox[1] + self.protagonist.hitbox[3] > self.workDesk.hitbox[1] and self.protagonist.hitbox[1] + self.protagonist.hitbox[3] < self.workDesk.hitbox[1] + self.workDesk.hitbox[3])):
            self.protagonist.isReceiveWork, self.protagonist.isCollide = True, True
        '''
        door = createThings.Item('door.png', self.width//3, 22*self.height//24, 
                                            80, 30, 'door')
        if ((self.protagonist.hitbox[0] + self.protagonist.hitbox[2] > door.hitbox[0] and self.protagonist.hitbox[0] + self.protagonist.hitbox[2] < door.hitbox[0] + door.hitbox[2])
            and (self.protagonist.hitbox[1] + self.protagonist.hitbox[3] > door.hitbox[1] and self.protagonist.hitbox[1] + self.protagonist.hitbox[3] < door.hitbox[1] + door.hitbox[3])):
            run = False
        return run

    def inHomeRunGame(self):
        homeSurface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Home")
        clock = pygame.time.Clock()

        run = True
        while run:
            clock.tick(15)
 
            self.timerForExpense += 0.06666666666666666
            self.timer += 0.06666666666666666
            self.stockTimer += 0.06666666666666666

            for event in pygame.event.get():
                position = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.detectHomeMouseEvents(position)
                    self.detectClickInvButton(position, homeSurface)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        self.isHelp = True

            #self.updateWebScraping()

            keys = pygame.key.get_pressed()
            (moveL, moveR, moveF, moveB) = self.detectKeyPressed(keys)

            self.checkDirectForCollision(moveL, moveR, moveF, moveB)

            self.redrawHomeWindow(homeSurface, moveL, moveR, moveF, moveB)
            run = self.homeDetectCollision(run)

            if self.isHelp:
                self.runHelpPage()

            if self.protagonist.money <= 0:
                run = self.gameOver()
                if run:
                    self.protagonist.inHome = False
                    self.protagonist.money = 20000
                    return

        self.protagonist.inHome = False
        self.protagonist.x = self.home.hitbox[0] + self.home.hitbox[2] // 2
        self.protagonist.y = self.home.hitbox[1] + self.home.hitbox[3]
        return

    def detectAnotherPlace(self):
        if self.protagonist.inMarket:
            self.protagonist.x, self.protagonist.y = self.width//2, self.height//2
            self.inMarketRunGame()
        elif self.protagonist.inBank:
            self.protagonist.x, self.protagonist.y = self.width//2, self.height//2
            self.inBankRunGame()
        elif self.protagonist.inWork:
            self.protagonist.x, self.protagonist.y = self.width//2, self.height//2
            self.inWorkRunGame()
        elif self.protagonist.inHome:
            self.protagonist.x, self.protagonist.y = self.width//2, self.height//2
            self.inHomeRunGame()

    def gameOver(self):
        overSurface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("GAME OVER")
        clock = pygame.time.Clock()

        run = True
        while run:
            clock.tick(15)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            bg = createThings.Background('gameoverBg.png', 'game over')
            bg.drawBg(overSurface)
            
            font = pygame.font.SysFont('arial', 40, True)
            text = font.render('GAME OVER', 1, (255, 255, 255))
            overSurface.blit(text, (self.width//3-30, self.height//3))

            font = pygame.font.SysFont('arial', 20, True)
            text = font.render('OOPS, looks like your balance has gone to zero...', 1, (255, 255, 255))
            overSurface.blit(text, (self.width//6, 2*self.height//3))

            text = font.render('Try invest wiser next time!', 1, (255, 255, 255))
            overSurface.blit(text, (self.width//4 + 50, 2*self.height//3+30))

            font = pygame.font.SysFont('arial', 10, True)
            text = font.render("Press 'r' to retry or press any other key to quit game", 1, (255, 255, 255))
            overSurface.blit(text, (self.width//3, 7*self.height//8))
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    else:
                        return False
                    
            pygame.display.update()

    def runHelpPage(self):
        helpSurface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Help")
        clock = pygame.time.Clock()

        run = True
        while run:
            clock.tick(15)

            instructionPage.drawHelpScreen(helpSurface, self.width, self.height)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.isHelp = False
                        return 
                    else:
                        pass
                    
            pygame.display.update()

    def runInstructionPage(self):
        instruSurface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Instructions")
        clock = pygame.time.Clock()

        run = True
        while run:
            clock.tick(15)

            instructionPage.drawInstruction(instruSurface, self.width, self.height)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True
                    else:
                        return False
                    
            pygame.display.update()

    def runGame(self):
        pygame.init()
        stSurface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Main Street")
        clock = pygame.time.Clock()

        if not self.startGame:
            self.startGame = self.runInstructionPage() #true == start the game

        #mainloop
        run = True
        while run:
            clock.tick(15)
            #print('protagonist''s in st')

            #update both timer
            self.timerForExpense += 0.06666666666666666
            self.timer += 0.06666666666666666
            self.stockTimer += 0.06666666666666666

            for event in pygame.event.get():
                position = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        self.isHelp = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.detectClickInvButton(position, stSurface)

            self.detectAnotherPlace()
            
            keys = pygame.key.get_pressed()
            (moveL, moveR, moveF, moveB) = self.detectKeyPressed(keys)
            self.detectCollision()
            #print('is it colliding: ', self.protagonist.isCollide)
            self.checkDirectForCollision(moveL, moveR, moveF, moveB)
                    
            self.doExpense()
            self.redrawStreetWindow(stSurface, moveL, moveR, moveF, moveB)

            if self.isHelp:
                self.runHelpPage()

            if self.protagonist.money <= 0:
                run = self.gameOver()
                if run:
                    self.protagonist.money = 20000

        pygame.quit()

PlayGame(600, 400).runGame()