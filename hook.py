#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 06 2018

@author: AMS, FMC
"""

import pygame, sys, random, csv
import pygame.event as GAME_EVENTS
import pygame.locals as GAME_GLOBALS
import pygame.time as GAME_TIME

import fish, worm

# VARIABLES

state = 'welcomeScreen'
gameMode = 0 # 0: 'ONLY ME', 1: 'TWO FRIENDS', 2: 'TWO ENEMIES'

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
maxScoreSingle = 0
maxScoreTeam = 0
greatestHitsSingle = []
greatestHitsTeam = []
winner = 0

name = [65, 65, 65, 65, 65, 65]
indexName = 0

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
DIFFICULTY = 0.97 # The near to 1 the easier. It will multiply to time_between_fishes every time a new fish is created
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
textFont = pygame.font.Font("assets/fonts/Jelly Crazies.ttf", 20)

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

imagesTitle = [
                pygame.image.load("assets/images/background/title1.png"),
                pygame.image.load("assets/images/background/title2.png"),
                pygame.image.load("assets/images/background/title3.png"),
                pygame.image.load("assets/images/background/title4.png"),
                pygame.image.load("assets/images/background/title5.png"),
                pygame.image.load("assets/images/background/title4.png"),
                pygame.image.load("assets/images/background/title3.png"),
                pygame.image.load("assets/images/background/title2.png")
            ]

stageToDraw = imagesTitle

# LOAD SOUNDS

#FUNCTIONS

def indexScore():
    if gameMode == 0:
        listScore = greatestHitsSingle
        index = 1
    else:
        listScore = greatestHitsTeam
        index = 2
    for k, comp in enumerate(listScore):
        toReturn = len(listScore) # It will return a 5 if score is too low to be in the hall of fame
        if int(comp[index])<= score:
            toReturn = k
            break   
    return toReturn
        
def enterScore():
    global greatestHitsSingle, greatestHitsTeam, score
    newPos = indexScore()
    tam = len(greatestHitsTeam)          
    for k in range(tam-newPos-1):
        if gameMode == 0:
            greatestHitsSingle[tam-1-k] = greatestHitsSingle[tam-2-k]
        else:
            greatestHitsTeam[tam-1-k] = greatestHitsTeam[tam-2-k]
    if gameMode == 0:
        greatestHitsSingle[newPos]= [chr(name[0])+chr(name[1])+chr(name[2]), str(score)]
    else:
        greatestHitsTeam[newPos] = [chr(name[0])+chr(name[1])+chr(name[2]), chr(name[3])+chr(name[4])+chr(name[5]), str(score)]


def newGame():
    global players, fishes, score, greatestHitsSingle, greatestHitsTeam, winner, indexName
    players = []
    fishes = []
    score = 0
    winner = 0
    with open('scoreSigle.csv', 'r') as csvfile:
        greatestHitsSingle = list(csv.reader(csvfile, delimiter=';'))
    with open('scoreTeam.csv', 'r') as csvfile:
        greatestHitsTeam = list(csv.reader(csvfile, delimiter=';'))
    indexName = 0
def quitGame():
    pygame.quit()
    sys.exit()

def drawStage():
    global surface, numberBackgroundImage, lastBackgroundChange, stageToDraw
    if GAME_TIME.get_ticks() - timeToChangeBackground > lastBackgroundChange:
        lastBackgroundChange = GAME_TIME.get_ticks()
        numberBackgroundImage += 1
        numberBackgroundImage = numberBackgroundImage % len(stageToDraw)
    imageToDraw = stageToDraw[numberBackgroundImage]
    rect = imageToDraw.get_rect()
    rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    surface.blit(imageToDraw, rect)

def welcomeScreen():
    global surface
    renderedText = textFont.render("PRESS SPACE", 1, (162, 179, 254))
    rect = renderedText.get_rect()
    rect.center = (int(WINDOW_WIDTH/2),int(WINDOW_HEIGHT/3))
    surface.blit(renderedText,rect)

def twoEnemiesScreen():
    global surface
    renderedText = textFont.render("WINNER PLAYER " + str(winner), 1, (255, 255, 255))
    rect = renderedText.get_rect()
    rect.center = (int(WINDOW_WIDTH/2),int(WINDOW_HEIGHT/2))
    surface.blit(renderedText,rect)

def hallOfFameScreen():
    global surface, greatestHitsSingle, greatestHitsTeam
    renderedText = textFont.render('HALL OF FAME', 1, (255, 255, 255))
    rect = renderedText.get_rect()
    rect.center = (int(WINDOW_WIDTH/2),int(1*WINDOW_HEIGHT/8))
    surface.blit(renderedText,rect)
    renderedText = textFont.render('ONE PLAYER', 1, (255, 255, 0))
    rect = renderedText.get_rect()
    rect.center = (int(1*WINDOW_WIDTH/4),int(2*WINDOW_HEIGHT/8))
    surface.blit(renderedText,rect)
    for k, line in enumerate(greatestHitsSingle):
        renderedText = textFont.render(line[0] + '   ' + line[1], 1, (255, 0, 0))
        rect = renderedText.get_rect()
        rect.center = (int(1*WINDOW_WIDTH/4),int((3+k)*WINDOW_HEIGHT/8))
        surface.blit(renderedText,rect)
    renderedText = textFont.render('TWO PLAYER', 1, (255, 255, 0))
    rect = renderedText.get_rect()
    rect.center = (int(3*WINDOW_WIDTH/4),int(2*WINDOW_HEIGHT/8))
    surface.blit(renderedText,rect)
    for k, line in enumerate(greatestHitsTeam):
        renderedText = textFont.render(line[0] + ', ' + line[1] + '   ' + line[2], 1, (255, 0, 0))
        rect = renderedText.get_rect()
        rect.center = (int(3*WINDOW_WIDTH/4),int((3+k)*WINDOW_HEIGHT/8))
        surface.blit(renderedText,rect)

def enterName():
    global surface, indexName, upPressed, downPressed, spacePressed, state
    renderedText = textFont.render('COGRATULATIONS', 1, (255, 255, 255))
    rect = renderedText.get_rect()
    rect.center = (int(WINDOW_WIDTH/2),int(1*WINDOW_HEIGHT/4))
    surface.blit(renderedText,rect)
    renderedText = textFont.render('YOU ARE IN THE HALL OF FAME', 1, (255, 255, 255))
    rect = renderedText.get_rect()
    rect.center = (int(WINDOW_WIDTH/2),int(2*WINDOW_HEIGHT/4))
    surface.blit(renderedText,rect)
    if gameMode == 0:
        lastIndex = 3
        listPoss = [6,7,8]
    else:
        lastIndex = 6
        listPoss = [4, 5, 6, 10, 11, 12]
    for k in range(lastIndex):
        if k == indexName:
            renderedText = textFont.render(chr(name[k]), 1, (255, 255, 255))
        else:
            renderedText = textFont.render(chr(name[k]), 1, (255, 255, 0))
        rect = renderedText.get_rect()
        rect.center = (int(listPoss[k]*WINDOW_WIDTH/15),int(3*WINDOW_HEIGHT/4))
        surface.blit(renderedText,rect)

    if upPressed:
        upPressed = False
        if name[indexName] < 90:
            name[indexName] += 1
    elif downPressed:
        downPressed = False
        if name[indexName] > 65:
            name[indexName] -= 1
    elif spacePressed:
        spacePressed = False
        indexName += 1
        if indexName == lastIndex:
            enterScore()
            state = 'hallOfFameScreen'

       
def menuScreen():
    global surface, gameMode, downPressed, upPressed, wormSelect
    messagesMenu = ['ONLY ME', 'TWO FRIENDS', 'TWO ENEMIES']
    for i, message in enumerate(messagesMenu):
        if i == gameMode:
            renderedText = textFont.render(message, 1, (255,255,255))
        else:
            renderedText = textFont.render(message, 1, (162, 179, 254))
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
    renderedText = textFont.render(str(score), 1, (206, 213, 255))
    rect = renderedText.get_rect()
    rect.center = (POSX_SCORE,POSY_SCORE)
    surface.blit(renderedText,rect)
    
def inGame():
    global surface, spacePressed, upPressed, time_between_fishes, last_fish, time_between_fishes, fishes, score, state, stageToDraw, winner
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
        enemy.draw(surface, GAME_TIME.get_ticks())
        enemy.move()
        for k, player in enumerate(players):
            if enemy.eat(player.returnSquares()):
                player.changeToDead()
                enemy.changeToEating()
                if gameMode == 2 : # mode two enemies, winner can be used in the next state
                    if winner == 0 :
                        if k == 0 : 
                            winner = 2
                        else:
                            winner = 1
        if enemy.isDead(WINDOW_WIDTH):
            if enemy.isEating():
                if gameMode == 2 :
                    state = 'twoEnemiesScreen'
                else: 
                    if indexScore() == 5:
                        state = 'hallOfFameScreen'
                    else:
                        state = 'enterName'
            else:
                score += 1
            fishes.remove(enemy)          
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
            stageToDraw = imagesBackground
            state = 'menuScreen'
    elif state == 'menuScreen':
        menuScreen()
        if spacePressed:
            newGame()
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
    elif state == 'twoEnemiesScreen':
        twoEnemiesScreen()
        if spacePressed:
            spacePressed = False
            stageToDraw = imagesTitle
            state = 'welcomeScreen'
    elif state == 'hallOfFameScreen':
        hallOfFameScreen()
        if spacePressed:
            spacePressed = False
            stageToDraw = imagesTitle
            state = 'welcomeScreen'
    elif state == 'enterName':
        enterName()
        if spacePressed:
            spacePressed = False
            stageToDraw = imagesTitle
            state = 'welcomeScreen'

    clock.tick(FPS)
    pygame.display.update()