#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 21:24:01 2018

@author: matt
"""

import pygame
import numpy as np

class game_object():
    
    def __init__(self, image, position, velocity = 0):
        
        self.image = image
        self.position = position[:]
        self.velocity = velocity
    
    def draw(self,screen):
        screen.blit(self.image,(self.position[0],self.position[1]))
        
class Ship(game_object):
    
    def __init__(self,position):
        #initialize ship in the first position
        super().__init__(pygame.image.load('spaceship-off.bmp'),position)
        self.angle = 0
        
        self.direction = [0.0 , -1.0]
        
    def move(self):
        #init_x = self.position[0]
        #init_y = self.position[1]
        
        self.direction[0] = np.sin(self.angle)
        self.direction[1] = -np.cos(self.angle)
        
        self.position[0] += self.direction[0]*self.velocity
        self.position[1] += self.direction[1]*self.velocity

        
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
        
        self.ship = Ship([self.width*.45,self.height*.5])
        self.ship_ang = 0
   
    def run(self):
        
        running = True
        
        while running:
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        
                        self.ship_ang = 2
                        
                    if event.key == pygame.K_RIGHT:
                        self.ship_ang  =  -2
                        
                    if event.key == pygame.K_UP:
                        self.ship.velocity += 1
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        
                        self.ship_ang = 0
                        
            #Game Boundaries
 #           if self.x_change == 5:
  #              if self.x == self.width:
   #                 self.x = -45
    #            else:
     #               self.x += self.x_change
      #      if self.x_change == -5:
       #         if self.x == -30:
        #            self.x = self.width
         #       else:
          #          self.x += self.x_change
            self.ship.move()
            print(self.ship.direction)
            self.update_all()
                
    
        pygame.quit()

    def update_all(self):
        self.ship.angle += self.ship_ang
        self.screen.fill(self.Black)  
        self.ship.draw(self.screen)
        pygame.display.update()
        self.clock.tick(self.FPS)
        
    def physics(self):
        
        self.ship.move()
        
        