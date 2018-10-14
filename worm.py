#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 06 2018

@author: AMS, FMC
"""

class worm:
    
    def __init__(self, type, xo, yo, pygame):
        self.type = type # Type 'player1', 'player2', 'sel'
        self.x = xo
        self.y = yo
        self.vy = 0
        self.VMAX = 10
        self.AC = 1
        self.kill = False
        self.pygame = pygame
        self.nimage = 0 # Index of the list to draw the image
        self.lastChange = 0
        self.timeToChange = 400 # Time between animated images in miliseconds
        
        if self.type=='player1':
            self.imageList = [pygame.image.load("assets/images/worm/expl1.png"),
                pygame.image.load("assets/images/worm/expl2.png"),
                pygame.image.load("assets/images/worm/expl3.png"),
                pygame.image.load("assets/images/worm/expl4.png"),
                pygame.image.load("assets/images/worm/expl5.png"),
                ] 
        elif self.type=='player2':
            self.imageList = [pygame.image.load("assets/images/worm/expl6.png"),
                pygame.image.load("assets/images/worm/expl6.png"),
                pygame.image.load("assets/images/worm/expl6.png"),
                pygame.image.load("assets/images/worm/expl7.png"),
                pygame.image.load("assets/images/worm/expl7.png"),
                ] 
        else :
            self.imageList = [pygame.image.load("assets/images/worm/expl8.png"),
                pygame.image.load("assets/images/worm/expl8.png"),
                pygame.image.load("assets/images/worm/expl8.png"),
                pygame.image.load("assets/images/worm/expl9.png"),
                pygame.image.load("assets/images/worm/expl9.png"),
                ] 
        
        self.imageDead = pygame.image.load("assets/images/worm/expl8.png")
        self.state = 'living'
        

    def move(self, dir, pos = 0):
        if dir == 'up' and self.vy > -self.VMAX:
            self.vy -= self.AC
        elif dir == 'down' and self.vy<self.VMAX:
            self.vy += self.AC
        else:  # when dir is selected to 'sel'
            if pos < self.y:
                self.vy -= self.AC
            else:
                self.vy += self.AC
        # TODO: check the size of the screen
        self.y += self.vy                

    def draw(self, surface, time):
        if time - self.lastChange > self.timeToChange:
            self.nimage += 1
            self.nimage = self.nimage % len(self.imageList)
            self.lastChange = time
        if self.state == 'living':
            imageToDraw = self.imageList[self.nimage]
        else:
            imageToDraw = self.imageDead
        rect = imageToDraw.get_rect()
        rect.center = (self.x,self.y)
        surface.blit(imageToDraw,rect)
        self.pygame.draw.line(surface, (20,239,12), [self.x, 0], [self.x, rect.top], 5)
        
        
        
        
        


