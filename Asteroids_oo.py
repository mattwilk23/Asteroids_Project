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
import random

class game_object():
    
    def __init__(self, image, position, accel = 0,vel = [0,0]):
        
        self.image = image
        self.position = position[:]
        self.accel = accel
        self.vel = vel[:]
    
    def draw(self,screen):
        screen.blit(self.image,(self.position[0],self.position[1]))
        
    def size(self):
        return [self.image.get_width(),self.image.get_height()]
        
class Ship(game_object):
    
    def __init__(self,position):
        #initialize ship in the first position
        super().__init__(pygame.transform.scale(pygame.image.load('logo_ship.bmp'),(60,60)),position)
        self.angle = 0
        self.direction = [0.0 , -1.0]
        self.max_speed = 6
        
        self.missiles = []
        
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
        
        self.ship_rot = pygame.transform.rotate(self.image,self.angle+45)
        
        screen.blit(self.ship_rot,(self.position[0],self.position[1]))
        
    def fire(self):
        adjust = self.size()
        adjust[0] = adjust[0]/2
        adjust[1] = adjust[1]/2
        add_missile = missile([self.position[0]+adjust[0],self.position[1]+adjust[1]],self.angle)
        
        self.missiles.append(add_missile)
    
    

class missile(game_object):
    
    def __init__(self,position,angle,accel=14):
        #accel is actually the velocity
        super().__init__(pygame.transform.scale(pygame.image.load('logo_missile.bmp'),(15,15)),position)
        
        self.angle = angle
        self.direction = [0,0]
        self.accel = accel
        
    
    def move(self):
        
        self.direction[0] = np.cos((self.angle+90)*np.pi/180)
        self.direction[1] = -np.sin((self.angle+90)*np.pi/180)
        
      
        
        #update position
        self.position[0] +=self.direction[0]*self.accel
        self.position[1] +=self.direction[1]*self.accel
        
        
    

class asteroid(game_object):
    
    def __init__(self,position,size,accel= 3):
    
        self.size = size
        if self.size == "big":
            super().__init__(pygame.transform.scale(pygame.image.load('asteroid.bmp'),(200,200)),\
                  position)
            
        
        if self.size == "normal":
            super().__init__(pygame.transform.scale(pygame.image.load('asteroid.bmp'),(120,120)),\
                  position)
            
        
        if self.size == "small":
            super().__init__(pygame.transform.scale(pygame.image.load('asteroid.bmp'),(60,60)),\
                  position)
            
        self.accel = accel
        self.direction = [0,0]
        
        if random.randrange(0,2) == 0:
            self.direction[0] = random.random()*-1
        else:
            self.direction[0] = random.random()
        if random.randrange(0,2) == 0:
            self.direction[1] = random.random()*-1
        else:
            self.direction[1] = random.random()
            
    def move(self):
        
        self.position[0] += self.direction[0]*self.accel
        self.position[1] += self.direction[1]*self.accel

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
        
        #initialize asteroids
        self.asteroids = []
        
        for i in range(4):
            x_int = random.randint(0, self.width)
            y_int = random.randint(0, self.height)
            
            temp_roid = asteroid([x_int,y_int], "big")
            self.asteroids.append(temp_roid)
        
    def run(self):
        
        running = True
        
        while running:
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        
                        self.ship_ang = 5
                        
                    if event.key == pygame.K_RIGHT:
                        self.ship_ang  =  -5
                        
                    if event.key == pygame.K_UP:
                        self.ship.accel = .4
                    
                    if event.key == pygame.K_SPACE:
                        self.ship.fire()
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:                      
                        self.ship_ang = 0
                        
                    if event.key == pygame.K_UP:
                            self.ship.accel = 0

            print(self.ship.size())
            self.game_boundaries()
            self.move_all()
            
            self.update_all()
                
    
        pygame.quit()

    def update_all(self):
        
        #make background black
        self.screen.fill(self.Black) 
        
        #Draw ship
        self.ship.angle += self.ship_ang
        self.ship.draw(self.screen)
        
        #Draw missiles
        if len(self.ship.missiles) > 0:
            for missile in self.ship.missiles:
                missile.draw(self.screen)
                
        #Draw asteroids     
        if len(self.asteroids) > 0:
            for roid in self.asteroids:
                roid.draw(self.screen)
                
        #update all
        pygame.display.update()
        self.clock.tick(self.FPS)
        
    def move_all(self):
        #does movement for missiles
        if len(self.ship.missiles) > 0:
            for missile in self.ship.missiles:
                missile.move()
                
        #does movement for asteroids     
        if len(self.asteroids) > 0:
            for roid in self.asteroids:
                roid.move()
          
        #does movement for ship
        self.ship.move()
        
    def game_boundaries(self):
        
        #This keeps the ship on the screen
        if self.ship.position[0] > self.width:
            self.ship.position[0] = -self.ship.image.get_width()
        if self.ship.position[0] < -self.ship.image.get_width():
            self.ship.position[0] = self.width
        if self.ship.position[1] > self.height:
            self.ship.position[1] = -self.ship.image.get_height()
        if self.ship.position[1] < -self.ship.image.get_height():
            self.ship.position[1] = self.height
            
        #This keeps the asteroids on the screen
        if len(self.asteroids) > 0:
            for roid in self.asteroids:
                if roid.position[0] > self.width:
                    roid.position[0] = -roid.image.get_width()
                if roid.position[0] < -roid.image.get_width():
                    roid.position[0] = self.width
                if roid.position[1] > self.height:
                    roid.position[1] = -roid.image.get_height()
                if roid.position[1] < -roid.image.get_height():
                    roid.position[1] = self.height
                    
    def collisions(self):
        
        pass
        