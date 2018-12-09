#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 21:24:01 2018

@author: matt
"""
''' To run this game, in your console enter Asteroids_Game().run() or attach this command
to the end of the code and you can run it from the command line'''

import pygame
import numpy as np

class game_object():
    
    def __init__(self, image, position, accel = 0,vel = [0,0]):
        
        self.image = image
        self.position = position[:]
        self.accel = accel
        self.vel = vel[:]
    
    def draw(self,screen):
        screen.blit(self.image,(self.position[0],self.position[1]))
        
class Ship(game_object):
    
    def __init__(self,position):
        #initialize ship in the first position
        super().__init__(pygame.image.load('spaceship-off.bmp'),position)
        self.angle = 0
        self.direction = [0.0 , -1.0]
        self.max_speed = 10
        
    def move(self):
        
        self.direction[0] = np.cos((self.angle+90)*np.pi/180)
        self.direction[1] = -np.sin((self.angle+90)*np.pi/180)
        
        #Conditions applying a max speed to ship and updating velocity
        if self.direction[0] < 0:
            if self.vel[0] < -self.max_speed:
                self.vel[0] += 0
            else:
                self.vel[0] += self.direction[0] * self.accel
                
        if self.direction[0] > 0:
            if self.vel[0] < self.max_speed:
                self.vel[0] += self.direction[0] * self.accel
            else:
                self.vel[0] += 0
         
        if self.direction[1] < 0:
            if self.vel[1] < -self.max_speed:
                self.vel[1] += 0
            else:
                self.vel[1] += self.direction[1] * self.accel
                
        if self.direction[1] > 0:
            if self.vel[1] < self.max_speed:
                self.vel[1] += self.direction[1] * self.accel
            else:
                self.vel[1] += 0
        
        #update position
        self.position[0] += self.vel[0]
        self.position[1] += self.vel[1]
        
            
        
    def draw(self, screen):
        
        self.ship_rot = pygame.transform.rotate(self.image,self.angle)
        
        screen.blit(self.ship_rot,(self.position[0],self.position[1]))
    
    

class missile(game_object):
    
    pass

class asteroid(game_object):
    
    pass

class Asteroids_Game():
    
    def __init__(self):
        
        pygame.init()
        
        #Initialize Screen
        self.width = 1500
        self.height = 1000
        self.screen = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption('Asteroids')
        
        #Colors
        self.Black = (0,0,0)
        self.White = (255,255,255)
               
        #FPS
        self.FPS = 60
       
        
        #timer
        self.clock = pygame.time.Clock()
        
        #Initialize Ship Position and angle
        
        self.ship = Ship([self.width*.46,self.height*.5])
        self.ship_ang = 0
   
    def run(self):
        
        running = True
        
        while running:
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        
                        self.ship_ang = 3
                        
                    if event.key == pygame.K_RIGHT:
                        self.ship_ang  =  -3
                        
                    if event.key == pygame.K_UP:
                        self.ship.accel = .2
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:                      
                        self.ship_ang = 0
                        
                    if event.key == pygame.K_UP:
                            self.ship.accel = 0

            
            self.game_boundaries()
            self.ship.move()
            
            self.update_all()
                
    
        pygame.quit()

    def update_all(self):
        #update ship
        self.ship.angle += self.ship_ang
        self.screen.fill(self.Black)  
        self.ship.draw(self.screen)
        
        #update all
        pygame.display.update()
        self.clock.tick(self.FPS)
        
    def physics(self):
        
        self.ship.move()
        
    def game_boundaries(self):
        
        if self.ship.position[0] > self.width:
            self.ship.position[0] = -46
        if self.ship.position[0] < -46:
            self.ship.position[0] = self.width
        if self.ship.position[1] > self.height:
            self.ship.position[1] = -90
        if self.ship.position[1] < -90:
            self.ship.position[1] = self.height
        