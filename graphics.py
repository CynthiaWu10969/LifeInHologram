import createThings

def createPeople(width, height):
    ppl1 = createThings.Item('ppl1.png', 19*width//32, height//4+7, 
                            20, 50, 'woman')
    ppl2 = createThings.Item('ppl2.png', 5*width//6, 21*height//24, 
                            40, 40, 'boy')
    ppl3 = createThings.Item('ppl3.png', width//6, 21*height//24, 
                            35, 40, 'couple')
    pplList = [ppl1, ppl2, ppl3]
    return pplList

def drawPeople(surface, width, height):
    pplList = createPeople(width, height)
    for ppl in pplList:
        ppl.drawItem(surface)