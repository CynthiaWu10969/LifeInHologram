import pygame
import createThings

def instructions(): #换行
    instruction1 = 'Welcome to Life In Hologram'
    instruction2 = 'Imagine yourself as a recent college grad with fluctuating amount of salary.'
    instruction3 = "While maintaining basic needs, you'll have to pay student loan and rental fees."
    instruction4 = 'What would you do to avoid the situation where your balance becomes 0???'
    instruction5 = 'Well, try to invest in the stock market and save up your money!'
    instruction6 = 'In Life In Hologram, you can invest in real stocks with real time data.'
    instruction7 = 'Wisely choose stocks based on their performances.'
    instruction8 = 'You can also deposit your money to earn some interest.'
    instruction9 = '    **Note: stock page can be lagging because we are using real time data!**'
    instruction10 = 'Press ENTER to start!'

    return [instruction1, instruction2, instruction3, instruction4, instruction5, instruction6, instruction7, instruction8, instruction9, instruction10]

def createHelp():
    help1 = 'Your goal in this game is to keep your balance above 0.'
    help2 = 'In this game, 15 seconds represent 1 month.'
    help3 = 'Your monthly expense, $2500, includes rental fees and student loan.'
    help4 = 'To keep your balance above 0, there are following things that you can do:'
    help5 = '1. Invest in stocks: You can buy stocks in this game with real time data.'
    help6 = '   Feel free to invest in any that you think will make a good profit.'
    help7 = '2. Deposit your money: You can choose the amount of money and time to deposit. '
    help8 = '   Interest rate is randomly picked between 0.5% - 0.9%, compounded monthly.'
    help9 = '   **NOTE: monthly expense will be deducted from wallet. '
    help10 = '  So be aware the amount of money you have with you.**'
    help11 = '3. Complete tasks: By completing tasks assigned, you can earn salaries!'
    help12 = 'You can check your monthly expense and student loan in the study at your home.'
    help13 = 'If your balance goes to 0, you lose the game.'
    help14 = "Press 'h' to see this help screen anytime during game & press ENTER to go back."
    help15 = 'GOOD LUCK!!!'

    return [help1, help2, help3, help4, help5, help6, help7, help8, help9, help10, help11, help12, help13, help14, help15]

def drawInstruction(surface, width, height):
    instructionBg = createThings.Background('instructionBg.png', 'instruction')
    instructionBg.drawBg(surface)

    instrus = instructions()
    rowDis = 30

    font = pygame.font.SysFont('arial', 35, True)
    text = font.render(instrus[0], 1, (255, 255, 255)) #white
    surface.blit(text, (width//10, height//8))

    font = pygame.font.SysFont('arial', 15, True)
    for i in range(len(instrus[1:])):
        text = font.render(instrus[i+1], 1, (255, 255, 255)) #white
        surface.blit(text, (width//12, height//4 + rowDis*i))

def drawHelpScreen(surface, width, height):
    helpBg = createThings.Background('helpBg.png', 'help')
    helpBg.drawBg(surface)

    helps = createHelp()
    rowDis = 20

    font = pygame.font.SysFont('arial', 35, True)
    text = font.render('HELP & HINTS', 1, (0, 0, 0)) #white
    surface.blit(text, (width//4, height//20))

    font = pygame.font.SysFont('arial', 15, True)
    for i in range(len(helps)):
        text = font.render(helps[i], 1, (0, 0, 0)) #white
        surface.blit(text, (width//25, height//7 + rowDis*i))
