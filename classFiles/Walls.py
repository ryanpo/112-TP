import pygame
import os
import random
import math
from classFiles.spritesheet import *

class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Wall,self).__init__()
        self.startX = x
        self.startY = y
        self.x = x
        self.y = y
        self.rect = None
        self.image = None
    def getRect(self):
        self.rect = pygame.Rect(self.x-8,self.y-8,16,16)
    def update(self,dx,dy):
        self.x = self.startX + dx
        self.y = self.startY + dy
        self.getRect()

class LeftWall(Wall):
    def __init__(self,x,y,sp1,sp2):
        super(Wall,self).__init__()
        self.startX = x
        self.startY = y
        self.x = x
        self.y = y
        ss = spritesheet('spriteAssets/CB-Temple-E.png')
        self.image = image = ss.image_at((sp1, sp2, 8, 8))
        self.size = self.image.get_size()
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*3), int(self.size[1]*3)))
        self.image = self.bigger_img
        self.rect = pygame.Rect(self.x,self.y,7.5,24)

class RightWall(Wall):
    def __init__(self,x,y,sp1,sp2):
        super(Wall,self).__init__()
        self.startX = x
        self.startY = y
        self.x = x
        self.y = y
        ss = spritesheet('spriteAssets/CB-Temple-E.png')
        self.image = image = ss.image_at((sp1, sp2, 8, 8))
        self.size = self.image.get_size()
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*3), int(self.size[1]*3)))
        self.image = self.bigger_img
        self.rect = pygame.Rect(self.x,self.y,24,24)

class MidWall(Wall):
    def __init__(self,x,y,sp1,sp2):
        super(Wall,self).__init__()
        self.startX = x
        self.startY = y
        self.x = x
        self.y = y
        ss = spritesheet('spriteAssets/CB-Temple-E.png')
        self.image = image = ss.image_at((sp1, sp2, 8, 8))
        self.size = self.image.get_size()
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*3), int(self.size[1]*3)))
        self.rect = pygame.Rect(self.x-12,self.y-21,25,45)
        self.image = self.bigger_img
        self.rect = pygame.Rect(self.x,self.y,24,24)

class Floor(Wall):
    def __init__(self,x,y,sp1,sp2,sheet = None):
        super(Wall,self).__init__()
        self.startX = x
        self.startY = y
        self.x = x
        self.y = y
        if sheet == "industrial":
            ss = spritesheet("spriteAssets/industrial.v2.png")
            self.image = ss.image_at((sp1, sp2, 36, 36))
            self.size = self.image.get_size()
            self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*1), int(self.size[1]*1)))
            self.image = self.bigger_img
            self.rect = pygame.Rect(self.x,self.y,36,36)
        else:
            ss = spritesheet('spriteAssets/CB-Temple-E.png')
            self.image =  ss.image_at((sp1, sp2, 8, 8))
            self.size = self.image.get_size()
            self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*3), int(self.size[1]*3)))
            self.image = self.bigger_img
            self.rect = pygame.Rect(self.x,self.y,24,24)
    
class Exit(Wall):
    def __init__(self,x,y,sp1,sp2,state,sheet = None,):
        super(Wall,self).__init__()
        self.startX = x
        self.startY = y
        self.x = x
        self.y = y
        self.framecount = 0
        self.state = state
        if sheet == "industrial":
            ss = spritesheet("spriteAssets/industrial.v2.png")
            self.image = ss.image_at((sp1, sp2, 36, 36))
            self.size = self.image.get_size()
            self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*3), int(self.size[1]*3)))
            self.image = self.bigger_img
            self.rect = pygame.Rect(self.x,self.y,108,108)
        else:
            ss = spritesheet('spriteAssets/industrial.v2.png')
            self.image =  ss.image_at((random.randint(16,32), random.randint(32,48), 8, 8))
            self.size = self.image.get_size()
            self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*3), int(self.size[1]*3)))
            self.image = self.bigger_img
            self.rect = pygame.Rect(self.x,self.y,108,108)
    def getRect(self):
        self.rect = pygame.Rect(self.x,self.y,108,108)
    def stateUpdate(self):
        self.framecount += 1
        if self.framecount//30 == 0:
            self.image = pygame.image.load(os.path.join("spriteAssets","exit_1.png"))
            self.size = self.image.get_size()
            self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*3), int(self.size[1]*3)))
            self.image = self.bigger_img
            self.getRect()
        elif self.framecount//30 == 1:
            self.image = pygame.image.load(os.path.join("spriteAssets","exit_2.png"))
            self.size = self.image.get_size()
            self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*3), int(self.size[1]*3)))
            self.image = self.bigger_img
        elif self.framecount//30 == 2:
            self.image = pygame.image.load(os.path.join("spriteAssets","exit_3.png"))
            self.size = self.image.get_size()
            self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*3), int(self.size[1]*3)))
            self.image = self.bigger_img
        elif self.framecount//30 == 3:
            self.image = pygame.image.load(os.path.join("spriteAssets","exit_4.png"))
            self.size = self.image.get_size()
            self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*3), int(self.size[1]*3)))
            self.image = self.bigger_img
        elif self.framecount//30 == 4:
            self.image = pygame.image.load(os.path.join("spriteAssets","exit_5.png"))
            self.size = self.image.get_size()
            self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*3), int(self.size[1]*3)))
            self.image = self.bigger_img
        elif self.framecount//30 == 5:
            self.image = pygame.image.load(os.path.join("spriteAssets","exit_5.png"))
            self.size = self.image.get_size()
            self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*3), int(self.size[1]*3)))
            self.image = self.bigger_img
            self.state = 2
            self.getRect()








