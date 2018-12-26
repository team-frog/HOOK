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

        if self.type=='big':
            self.imageList = [
                pygame.image.load("assets/images/fishes/bigFish1.png"),
                pygame.image.load("assets/images/fishes/bigFish2.png"),
                pygame.image.load("assets/images/fishes/bigFish3.png"),
                pygame.image.load("assets/images/fishes/bigFish2.png")
            ]
            self.vx = 5
        else:
            self.imageList = [
                pygame.image.load("assets/images/fishes/smallFish1.png"),
                pygame.image.load("assets/images/fishes/smallFish2.png"),
                pygame.image.load("assets/images/fishes/smallFish3.png"),
                pygame.image.load("assets/images/fishes/smallFish2.png")
            ]
            self.vx = 10

    def draw(self, surface, actualTime):
        if self.state == 'hungry':
            imageToDraw = self.imageList[self.numberImage]
            rect = imageToDraw.get_rect()
            rect.center = (self.x, self.y)
            surface.blit(imageToDraw, rect)
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