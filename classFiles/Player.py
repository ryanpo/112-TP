import pygame
import os
import random
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player,self).__init__()
        self.x = x
        self.y = y
        self.startX = x
        self.startY = y
        self.xSpeed = 0
        self.ySpeed = 0
        self.count = 0
        self.image = pygame.image.load(os.path.join("spriteAssets","player_idle_"+str(self.count%24//6)+"R.png"))
        self.size = self.image.get_size()
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*2.5), int(self.size[1]*2.5)))
        self.rect = pygame.Rect(self.x-20,self.y-15,25,45)
        self.image = self.bigger_img
        self.playerHealthFull = 6
        self.playerHealth = 6
        self.damageCount = 30
    def getRect(self):  # GET REKT
        self.rect = pygame.Rect(self.x-20,self.y-15,25,45)
    def isMoving(self):
        if self.xSpeed == 0 and self.ySpeed == 0:
            return False
        return True
    def update(self):
        self.x += self.xSpeed
        self.y += self.ySpeed
        self.getRect()
    def unupdate(self):
        self.x -= self.xSpeed
        self.y -= self.ySpeed
        self.getRect()
    def imageUpdate(self,dir):
        self.count += 1
        if not self.isMoving():
            if dir == "Left":
                self.image = pygame.image.load(os.path.join("spriteAssets","player_idle_"\
                +str(self.count%24//6)+"L.png"))
            elif dir == "Right":
                self.image = pygame.image.load(os.path.join("spriteAssets","player_idle_"\
                +str(self.count%24//6)+"R.png"))
        else:
            if dir == "Left":
                self.image = pygame.image.load(os.path.join("spriteAssets","player_run_"\
                +str(self.count%24//3)+"L.png"))
            elif dir == "Right":
                self.image = pygame.image.load(os.path.join("spriteAssets","player_run_"\
                +str(self.count%24//3)+"R.png"))
        if self.damageCount < 30 and self.damageCount%6<3:
            self.image = pygame.image.load(os.path.join("spriteAssets","text_default.png"))
        self.size = self.image.get_size()
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*2.5), int(self.size[1]*2.5)))
        self.rect = pygame.Rect(self.x-20,self.y-15,25,45)
        self.image = self.bigger_img
    def collisionUpdate(self,dx,dy):
        self.x += dx
        self.y += dy
        self.getRect()

