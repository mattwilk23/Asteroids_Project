#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 00:27:12 2018

@author: matt
"""
import pygame

screen_w = 800
screen_h = 600

black = (0,0,0)
white = (255,255,255)

spaceshipIMG = pygame.image.load('rock-big.bmp')

def ship(x,y,angle):
    turn = pygame.transform.rotate(spaceshipIMG, angle)
    gameDisplay.blit(turn,(x,y))
    

    
x = (screen_w *.45)
y = (screen_h * .5)

angle = 0
cangle = 0

pygame.init()
gameDisplay = pygame.display.set_mode((screen_w,screen_h))
pygame.display.set_caption('Asteroids')
clock = pygame.time.Clock()

crashed = False

while not crashed:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                cangle = 2
            elif event.key == pygame.K_RIGHT:
                cangle = -2
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                cangle = 0
                
    print(event)
    angle += cangle
    gameDisplay.fill(black)        
    ship(x,y,angle)   
    pygame.display.update()
    clock.tick(60)
    
pygame.quit()
