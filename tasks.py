import pygame
import random

def createTasks():
    task1 = 'flowerTask'
    task2 = 'fileTask'
    tasks = [task1, task2]
    return tasks

def chooseTask():
    tasks = createTasks()
    randNum = random.randint(0, 1) #includes both
    return tasks[randNum]

#print(chooseTask())