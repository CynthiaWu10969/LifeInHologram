import pygame
import random

def chooseTask():
    tasks = ['flowerTask', 'fileTask']
    randNum = random.randint(0, 1) #includes both
    return tasks[randNum]
