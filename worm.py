#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 06 2018

@author: AMS, FMC
"""

class worm:
    
    def __init__(self, type, pos, pygame):
        self.type = type # Type 'player1', 'player2', 'sel'
        self.x = pos[0]
        self.y = pos[1]
        self.vy = 0
        self.VMAX = 10
        self.AC = 0.5
        self.pygame = pygame
        self.nimage = 0 # Index of the list to draw the image
        self.lastChange = 0
        self.timeToChange = 250 # Time between animated images in miliseconds
        self.lineDisplacement = 6 # Los píxeles que se moverá la línea a la derecha
        self.WINDOW_HEIGHT = 700
        self.SQUARES = ( (-20,-5,20,65) , (0,40,30,20) ) # Squares that define the vulnable part of the worm referred to the center. Format: (left, top, width, height)
        
        if self.type=='player1':
            self.imageList = [pygame.image.load("assets/images/worm/SMALLbigworm.png"),
                pygame.image.load("assets/images/worm/SMALLmediumworm.png"),
                pygame.image.load("assets/images/worm/SMALLsmallworm.png"),
                pygame.image.load("assets/images/worm/SMALLmediumworm.png")              
                ] 
        elif self.type=='player2':
            self.imageList = [pygame.image.load("assets/images/worm/SMALLbigworm2.png"),
                pygame.image.load("assets/images/worm/SMALLmediumworm2.png"),
                pygame.image.load("assets/images/worm/SMALLsmallworm2.png"),
                pygame.image.load("assets/images/worm/SMALLmediumworm2.png")              
                ] 
        else :
            self.imageList = [pygame.image.load("assets/images/worm/BIGbigworm.png"),
                pygame.image.load("assets/images/worm/BIGmediumworm.png"),
                pygame.image.load("assets/images/worm/BIGsmallworm.png"),
                pygame.image.load("assets/images/worm/BIGmediumworm.png")              
                ]
            self.lineDisplacement = 8 # El desplazamiento de la línea a la derecha en el Type: 'sel'
        
        self.imageDead = pygame.image.load("assets/images/worm/emptyHook.png")
        self.state = 'living'
        

    def move(self, dir, pos = 0): # 'up' one step up, 'down' one step down, 'pos' one step towards pos (a possition at y exe)
        if dir == 'up' and self.vy > -self.VMAX:
            self.vy -= self.AC
        elif dir == 'down' and self.vy < self.VMAX:
            self.vy += self.AC
        elif dir == 'pos':  # when dir is selected to 'sel'
            self.vy = -(self.y-pos)/10
        # TODO: check the size of the screen
        if (self.vy > 0 and self.y<(self.WINDOW_HEIGHT-100)) or (self.vy < 0 and self.y>(100)):
            self.y += self.vy
        else:
            self.vy = 0

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
        self.pygame.draw.line(surface, (0,50,20), [self.x + self.lineDisplacement, 0], [self.x + self.lineDisplacement, rect.top], 2)
        #self.pygame.draw.rect(surface, (255, 0, 0), [self.x + self.SQUARES[0][0], self.y + self.SQUARES[0][1], self.SQUARES[0][2], self.SQUARES[0][3]])
        #self.pygame.draw.rect(surface, (255, 255, 0), [self.x + self.SQUARES[1][0], self.y + self.SQUARES[1][1], self.SQUARES[1][2], self.SQUARES[1][3]])
    
    def returnSquares(self):
        toReturn = []
        if self.state == 'living':
            for sq in self.SQUARES:
                toReturn.append((self.x + sq[0], self.y + sq[1], sq[2], sq[3]))
        return toReturn           
        
    def changeToDead(self):
        self.state = 'dead'
