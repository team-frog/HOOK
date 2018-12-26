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

moveList = ['down', 'down']

lastBackgroundChange = 0
numberBackgroundImage = 0
timeToChangeBackground = 100

players = []
fishes = []
last_fish = 0
score = 0

# CONSTANTS

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
LIMITS_GENERATION_FISHES = 100 # Para saber de donde a donde en la posición en y se pueden generar los peces
FPS = 60
POS_SEL = (int(WINDOW_WIDTH/4), int(WINDOW_HEIGHT/2))
POS_ONLYME = (int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2))
POS_P1 = (int(2*WINDOW_WIDTH/5), int(WINDOW_HEIGHT/2))
POS_P2 = (int(3*WINDOW_WIDTH/5), int(WINDOW_HEIGHT/2))
TIME_BETWEEN_FISHES_O = 5000
DIFFICULTY = 0.95 # The near to 1 the easier. It will multiply to time_between_fishes every time a new fish is created
MIN_TIME_BETWEEN_FISHES = 1000
POSX_SCORE = 100
POSY_SCORE = 100

# OBJECTS
wormSelect = worm.worm('sel', POS_SEL, pygame)


# PYGAME OBJECTS

pygame.display.init()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption('HOOK')
clock = GAME_TIME.Clock()
pygame.font.init()
textFont = pygame.font.SysFont("monospace", 50)

# LOAD IMAGES

imagesBackground = [
                pygame.image.load("assets/images/background/background1.png"),
                pygame.image.load("assets/images/background/background2.png"),
                pygame.image.load("assets/images/background/background3.png"),
                pygame.image.load("assets/images/background/background4.png"),
                pygame.image.load("assets/images/background/background5.png"),
                pygame.image.load("assets/images/background/background4.png"),
                pygame.image.load("assets/images/background/background3.png"),
                pygame.image.load("assets/images/background/background2.png")
            ]

# LOAD SOUNDS

#FUNCTIONS

def quitGame():
    pygame.quit()
    sys.exit()

def drawStage():
    global surface, numberBackgroundImage, lastBackgroundChange
    if GAME_TIME.get_ticks() - timeToChangeBackground > lastBackgroundChange:
        lastBackgroundChange = GAME_TIME.get_ticks()
        numberBackgroundImage += 1
        numberBackgroundImage = numberBackgroundImage % len(imagesBackground)
    imageToDraw = imagesBackground[numberBackgroundImage]
    rect = imageToDraw.get_rect()
    rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    surface.blit(imageToDraw, rect)

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

def random_dir():
    posibility = ['right','left']
    return random.choice(posibility)

def random_type():
    posibility = ['big','small']
    return random.choice(posibility)

def random_pos(window_height):
    return random.randint(LIMITS_GENERATION_FISHES, window_height - LIMITS_GENERATION_FISHES)

def draw_score():
    global score, surface
    renderedText = textFont.render(str(score), 1, (255,0,255))
    rect = renderedText.get_rect()
    rect.center = (POSX_SCORE,POSY_SCORE)
    surface.blit(renderedText,rect)
    
def inGame():
    global surface, spacePressed, upPressed, time_between_fishes, last_fish, time_between_fishes, fishes, score
    if GAME_TIME.get_ticks() - last_fish > time_between_fishes:
        fishes.append(fish.fish(random_type(),random_dir(),random_pos(WINDOW_HEIGHT),WINDOW_WIDTH,pygame))
        last_fish = GAME_TIME.get_ticks()
        if time_between_fishes > MIN_TIME_BETWEEN_FISHES:
            time_between_fishes *= DIFFICULTY
        
    pressedList = [spacePressed, upPressed]       
    for i, player in enumerate(players):
        if pressedList[i]:
            moveList[i] = 'up'
        else:
            moveList[i] = 'down'
        player.draw(surface, GAME_TIME.get_ticks())
        player.move(moveList[i])
    for i, enemy in enumerate(fishes):
        enemy.draw(surface, GAME_TIME.get_ticks(),pygame)
        enemy.move()
        if enemy.isDead(WINDOW_WIDTH):
            fishes.remove(enemy)
            score += 1
    draw_score()


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
            if gameMode == 0: #only me
                players.append(worm.worm('player1', POS_ONLYME, pygame))
            else:
                players.append(worm.worm('player1', POS_P1, pygame))
                players.append(worm.worm('player2', POS_P2, pygame))
            spacePressed = False
            time_between_fishes = TIME_BETWEEN_FISHES_O # Init of time between fishes. It will be decreased progresivelly
            last_fish = GAME_TIME.get_ticks()
            fishes.append(fish.fish('big',random_dir(),random_pos(WINDOW_HEIGHT),WINDOW_WIDTH,pygame))
            state = 'inGame'
    elif state == 'inGame':
        inGame()
        


    clock.tick(FPS)
    pygame.display.update()