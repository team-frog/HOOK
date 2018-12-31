#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 06 2018

@author: AMS, FMC
"""

class fish:

    def __init__(self, type, dir, yo, WINDOW_WIDTH, pygame):
        self.type = type  # Pez rápido (small) y pez lento (big)
        self.state = 'hungry' # Estará en el state 'hungry' cuando no esté comiendo al gusano y en el state 'eating' cuando sí
        if dir == 'right':
            self.x = -100
        else:
            self.x = WINDOW_WIDTH + 100
        self.dir = dir
        self.y = yo
        self.numberImage = 0
        self.lastChange = 0
        self.timeToChange = 100
        self.pygame = pygame
        

        if self.type=='big':
            self.imageList = [
                pygame.image.load("assets/images/fishes/bigFish1.png"),
                pygame.image.load("assets/images/fishes/bigFish2.png"),
                pygame.image.load("assets/images/fishes/bigFish3.png"),
                pygame.image.load("assets/images/fishes/bigFish2.png")
            ]
            self.imageListEating = [
                pygame.image.load("assets/images/worm/expl1.png"),
                pygame.image.load("assets/images/worm/expl2.png"),
                pygame.image.load("assets/images/worm/expl3.png"),
                pygame.image.load("assets/images/worm/expl4.png")
            ]
            self.vx = 5
            if self.dir == 'right':
                self.MOUTH = (-40,-32,80,65) # Squares that define mouth referred to the center. Format: (left, top, width, height)
            else:
                self.MOUTH = (-40,-32,80,65)
        else:
            self.imageList = [
                pygame.image.load("assets/images/fishes/smallFish1.png"),
                pygame.image.load("assets/images/fishes/smallFish2.png"),
                pygame.image.load("assets/images/fishes/smallFish3.png"),
                pygame.image.load("assets/images/fishes/smallFish2.png")
            ]
            self.imageListEating = [
                pygame.image.load("assets/images/worm/expl1.png"),
                pygame.image.load("assets/images/worm/expl2.png"),
                pygame.image.load("assets/images/worm/expl3.png"),
                pygame.image.load("assets/images/worm/expl4.png")
            ]
            self.vx = 10
            if self.dir == 'right':
                self.MOUTH = (-35,-26,70,52) # Squares that define mouth referred to the center. Format: (left, top, width, height)
            else:
                self.MOUTH = (-35,-26,70,52)

    def draw(self, surface, actualTime):
        if self.dir == 'right' :
            if self.state == 'hungry':
                imageToDraw = self.imageList[self.numberImage]
            else:
                imageToDraw = self.imageListEating[self.numberImage]
        else:
            if self.state == 'hungry':
                imageToDraw = self.pygame.transform.flip(self.imageList[self.numberImage],True,False)
            else:
                imageToDraw = self.pygame.transform.flip(self.imageListEating[self.numberImage],True,False)
        rect = imageToDraw.get_rect()
        rect.center = (self.x, self.y)
        surface.blit(imageToDraw, rect)
        #self.pygame.draw.rect(surface, (255, 0, 0), [self.x + self.MOUTH[0], self.y + self.MOUTH[1], self.MOUTH[2], self.MOUTH[3]])
    
        if actualTime - self.timeToChange > self.lastChange:
            self.lastChange = actualTime
            self.numberImage += 1
            self.numberImage = self.numberImage % len(self.imageList)
            

    def move(self):
        if self.dir == 'right':
            self.x += self.vx
        else:
            self.x -= self.vx

    def changeToEating(self):
        self.state = 'eating'

    def isDead(self, WINDOW_WIDTH):
        if self.x >= WINDOW_WIDTH + 150 or self.x < -150:
            return True
        else:
            return False
    
    def isEating(self):
        return self.state=='eating'
    
    def eat(self, squares):
        toReturn = False
        if self.state == 'hungry':
            for sq in squares:
                if (self.MOUTH[0] + self.x - sq[0] >= 0 and self.MOUTH[0] + self.x - sq[0] < sq[2]) or (self.MOUTH[0] + self.x - sq[0] < 0 and -(self.MOUTH[0] + self.x - sq[0]) < self.MOUTH[2]):
                    # Inside in the x axis
                    if (self.MOUTH[1] + self.y - sq[1] >= 0 and self.MOUTH[1] + self.y - sq[1] < sq[3]) or (self.MOUTH[1] + self.y - sq[1] < 0 and -(self.MOUTH[1] + self.y - sq[1]) < self.MOUTH[3]):
                        # inside the y axis
                        toReturn = True
        return toReturn
        
        