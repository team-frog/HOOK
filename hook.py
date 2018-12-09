#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 06 2018

@author: AMS, FMC
"""

import pygame, sys, random
import pygame.event as GAME_EVENTS
import pygame.locals as GAME_GLOBALS
import pygame.time as GAME_TIME

import fish, worm

# VARIABLES

state = 'welcomeScreen'
gameMode = 0

spacePressed = False
upPressed = False
downPressed = False


# CONSTANTS

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60
YO_SEL = int(WINDOW_HEIGHT/2)
XO_SEL = int(WINDOW_WIDTH/4)

# OBJECTS
wormSelect = worm.worm('sel', XO_SEL, YO_SEL, pygame)

# PYGAME OBJECTS

pygame.display.init()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption('HOOK')
clock = GAME_TIME.Clock()
pygame.font.init()
textFont = pygame.font.SysFont("monospace", 50)

# LOAD IMAGES

# LOAD SOUNDS

#FUNCTIONS

def quitGame():
    pygame.quit()
    sys.exit()

def drawStage():
    global surface
    surface.fill((75, 44, 252))

def welcomeScreen():
    global surface
    renderedText = textFont.render("Press space", 1, (255,255,255))
    rect = renderedText.get_rect()
    rect.center = (int(WINDOW_WIDTH/2),int(WINDOW_HEIGHT/2))
    surface.blit(renderedText,rect)


def menuScreen():
    global surface, gameMode, downPressed, upPressed, wormSelect
    messagesMenu = ['Only me', 'Two friends', 'Two enemies']
    for i, message in enumerate(messagesMenu):
        if i == gameMode:
            renderedText = textFont.render(message, 1, (255,0,255))
        else:
            renderedText = textFont.render(message, 1, (255,255,255))
        rect = renderedText.get_rect()
        rect.center = (int(WINDOW_WIDTH/2),int((i+1)*WINDOW_HEIGHT/(len(messagesMenu)+1)))
        surface.blit(renderedText,rect)

    if upPressed:
        upPressed = False
        if gameMode > 0:
            gameMode -= 1
    elif downPressed:
        downPressed = False
        if gameMode < len(messagesMenu)-1:
            gameMode += 1

    wormSelect.draw(surface, GAME_TIME.get_ticks())
    wormSelect.move('pos', int((gameMode+1)*WINDOW_HEIGHT/(len(messagesMenu)+1)))



def inGame():
    global surface
    renderedText = textFont.render("Jugando", 1, (255,255,255))
    rect = renderedText.get_rect()
    rect.center = (int(WINDOW_WIDTH/2),int(WINDOW_HEIGHT/2))
    surface.blit(renderedText,rect)


# MAIN LOOP

while True:
    drawStage()
    # Handle user and system events
    for event in GAME_EVENTS.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitGame()
            if event.key == pygame.K_SPACE :
                spacePressed = True
            if event.key == pygame.K_UP:
                upPressed = True
            if event.key == pygame.K_DOWN:
                downPressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE :
                spacePressed = False
            if event.key == pygame.K_UP:
                upPressed = False
            if event.key == pygame.K_DOWN:
                downPressed = False
        if event.type == GAME_GLOBALS.QUIT:
            quitGame()
        

    if state == 'welcomeScreen':
        welcomeScreen()
        if spacePressed:
            spacePressed = False
            state = 'menuScreen'
    elif state == 'menuScreen':
        menuScreen()
        if spacePressed:
            spacePressed = False
            state = 'inGame'
    elif state == 'inGame':
        inGame()


    clock.tick(FPS)
    pygame.display.update()