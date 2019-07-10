import pygame
import os
import random
import math

class Wand(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Wand,self).__init__()
        self.x = x
        self.y = y
        self.baseimage = pygame.image.load(os.path.join("spriteAssets","weapon_green_magic_staff.png"))
        self.baseimage =  pygame.transform.rotate(self.baseimage,-90)
        self.rect = pygame.Rect(self.x,self.y,4,4)
        self.image = self.baseimage
    def getRect(self):
        self.rect = pygame.Rect(self.x,self.y,4,4)
    def rotateImage(self,newAngle):
        self.image = pygame.transform.rotate(self.baseimage,newAngle)
    def update(self,x,y):
        self.x = x
        self.y = y
        self.getRect()
    def rotateUpdate(self,mouseX,mouseY,playerX,playerY):
        dirx = mouseX - playerX
        diry = mouseY - playerY
        l = math.sqrt(dirx**2 + diry**2)
        if l != 0:
            direction = [dirx/l,diry/l]
        else:
            direction = [dirx/1,diry/1]
        angle = 0
        if direction[0] != 0 and direction[0] > 0 and direction[1] < 0:
            angle = ((-180/math.pi)*math.atan(direction[1]/direction[0]))
        elif direction[0] != 0 and direction[0] < 0 and direction[1] < 0:
            angle = ((-180/math.pi)*math.atan(direction[1]/direction[0])+180)
        elif direction[0] < 0 and direction[1] > 0:
            angle = ((-180/math.pi)*math.atan(direction[1]/direction[0])+180)
        elif direction[0] != 0 and direction[1] != 0:
            angle = ((-180/math.pi)*math.atan(direction[1]/direction[0])+360)
        elif math.isclose(direction[0],0):
            if direction[1] > 0:
                angle = 270
            else:
                angle = 90
        elif math.isclose(direction[1],0):
            if direction[0] < 0:
                angle = 180
        self.rotateImage(angle)
        if angle < 360 and angle >= 270:
            self.update(playerX-4,playerY+4)
        elif angle<=90 and angle>=0:
            self.update(playerX-4,playerY-24*math.sin(math.radians(angle))+4)
        elif angle>90 and angle<180:
            self.update(playerX+26*math.cos(math.radians(angle))-4,\
            playerY-24*math.sin(math.radians(angle))+4)
        else:
            self.update(playerX-26*math.cos(math.radians(angle-180))-4,playerY+4)