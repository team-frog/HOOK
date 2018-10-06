#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame, sys, random
import pygame.event as GAME_EVENTS
import pygame.locals as GAME_GLOBALS
import pygame.time as GAME_TIME

import fish, worm

# VARIABLES

state = 'welcomeScreen'

# CONSTANTS

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60

# PYGAME OBJECTS

pygame.display.init()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption('HOOK')
clock = GAME_TIME.Clock()

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
    pass

# MAIN LOOP

while True:
    drawStage()
    # Handle user and system events
    for event in GAME_EVENTS.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitGame()
        if event.type == GAME_GLOBALS.QUIT:
            quitGame()

    if state == 'welcomeScreen':
        welcomeScreen()

    clock.tick(FPS)
    pygame.display.update()