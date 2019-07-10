import pygame
import os
import random
import math
from classFiles.spritesheet import *

class textBox(pygame.sprite.Sprite):
    def __init__(self,x,y,fileName,dimX,dimY):
        super(textBox,self).__init__()
        self.x = x
        self.y = y
        self.startX = x
        self.startY = y
        self.dimX = dimX
        self.dimY = dimY
        self.image = pygame.image.load(os.path.join("spriteAssets","text_default.png"))
        self.emptyImage = pygame.image.load(os.path.join("spriteAssets","text_default.png"))
        self.showImage = pygame.image.load(os.path.join("spriteAssets",fileName))
        self.size = self.image.get_size()
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*0.5), int(self.size[1]*0.5)))
        self.image = self.bigger_img
        self.rect = pygame.Rect(self.x-self.dimX/2,self.y-self.dimY,dimX,dimY)
    def getRect(self):
        self.rect = pygame.Rect(self.x-self.dimX/2,self.y-self.dimY,self.dimX,self.dimY)
    def update(self,dx,dy):
        self.x = self.startX + dx
        self.y = self.startY + dy
        self.getRect()
    def imageUpdate(self,collideBool):
        if collideBool:
            self.image = self.showImage
        else:
            self.image = self.emptyImage
        self.size = self.image.get_size()
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*0.5), int(self.size[1]*0.5)))
        self.image = self.bigger_img
        

class Exp(pygame.sprite.Sprite):
    def __init__(self,x,y,marginDiffX = 0, marginDiffY = 0):
        super(Exp,self).__init__()
        self.x = x
        self.y = y
        self.startX = x
        self.startY = y
        self.speed = 7
        self.image = pygame.image.load(os.path.join("spriteAssets","bullet.png"))
        self.size = self.image.get_size()
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*2), int(self.size[1]*2)))
        self.image = self.bigger_img
        self.rect = pygame.Rect(self.x-4,self.y-4,8,8)
        self.marginDiffX = marginDiffX
        self.marginDiffY = marginDiffY
        self.movedX = 0
        self.movedY = 0
    def getRect(self):
        self.rect = pygame.Rect(self.x-6,self.y-6,12,12)
    def imageUpdate(self,dirX,dirY):
        if self.state == 0:
            pass
        elif self.state == 1:
            self.movedX += self.speed*dirX
            self.movedY += self.speed*dirY
        self.getRect()
    def update(self,dx,dy):
        self.x = self.startX + self.movedX + dx - self.marginDiffX
        self.y = self.startY + self.movedY + dy - self.marginDiffY
        self.getRect()  



class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y,marginDiffX = 0, marginDiffY = 0):
        super(Coin,self).__init__()
        self.x = x
        self.y = y
        self.startX = x
        self.startY = y
        self.frame = 0
        self.image = pygame.image.load(os.path.join("spriteAssets","coin_anim_f0.png"))
        self.size = self.image.get_size()
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*1.5), int(self.size[1]*1.5)))
        self.image = self.bigger_img
        self.rect = pygame.Rect(self.x-6,self.y-6,12,12)
        self.marginDiffX = marginDiffX
        self.marginDiffY = marginDiffY
    def getRect(self):
        self.rect = pygame.Rect(self.x-6,self.y-6,12,12)
    def update(self,dx,dy):
        self.frame += 1
        self.image = pygame.image.load(os.path.join("spriteAssets","coin_anim_f"+str((self.frame//6)%4)+".png"))
        self.size = self.image.get_size()
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*1.5), int(self.size[1]*1.5)))
        self.image = self.bigger_img
        self.x = self.startX + dx - self.marginDiffX
        self.y = self.startY + dy - self.marginDiffY
        self.getRect()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, size, x, y, speed, direction):
        super(Bullet,self).__init__()
        self.x = x
        self.y = y
        self.baseX = x
        self.baseY = y
        self.bulletsize = size
        self.speed = speed
        self.direction = direction
        self.image = pygame.image.load(os.path.join("spriteAssets","sprHeavySlug.png"))
        self.rect = pygame.Rect(self.x-size/2,self.y-size/2,size,size)
        self.size = self.image.get_size()
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*self.bulletsize/32), int(self.size[1]*self.bulletsize/32)))
        self.image = self.bigger_img
    def getRect(self):
        self.rect = pygame.Rect(self.x-self.bulletsize/2,self.y-self.bulletsize-2,self.bulletsize,self.bulletsize)
    def update(self,dx,dy):
        self.baseX += self.speed*self.direction[0]
        self.baseY += self.speed*self.direction[1]
        self.x = self.baseX + dx
        self.y = self.baseY + dy
        self.getRect()

class Pointer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Pointer,self).__init__()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,16,16)
        self.image = pygame.image.load(os.path.join("spriteAssets","pointer.png"))
    def getRect(self):  # GET REKT
        self.rect = pygame.Rect(self.x,self.y,16,16)
    def update(self):
        self.getRect()


class LevelDisplay(pygame.sprite.Sprite):
    def __init__(self,x,y,sp1,sp2,scale = 1):
        super(LevelDisplay,self).__init__()
        self.x = x
        self.y = y
        ss = spritesheet("spriteAssets/industrial.v2.png")
        self.image = ss.image_at((sp1, sp2, 36, 36))
        # self.image = pygame.image.load(os.path.join("spriteAssets","levelssheet.png"))
        self.rect = pygame.Rect(self.x,self.y,240,48)
    def getRect(self):
        self.rect = pygame.Rect(self.x,self.y,240,48)

def spellCast(lst):
    if lst == []:
        return None
    result = ""
    for i in lst:
        result += str(i)
    if (result in "013201320" or result in "023102310") and len(result)>=5:
        return "BLOSSOM"

def quadrant(x,y):
    if x < 300 and y < 252:
        return 0
    elif x<300 and y >= 252:
        return 2
    elif x>=300 and y<252:
        return 1
    elif x>=300 and y>=252:
        return 3



class ClickBox(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(ClickBox,self).__init__()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x-2,self.y-2,4,4)
    def getRect(self):
        self.rect = pygame.Rect(self.x-2,self.y-2,4,4)

class DragBox(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(DragBox,self).__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(os.path.join("spriteAssets","dragBox.png"))
        self.rect = pygame.Rect(self.x-4,self.y-4,8,8)
    def getRect(self):
        self.rect = pygame.Rect(self.x-4,self.y-4,8,8)
    
class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super(Monster,self).__init__()
        self.startX = x
        self.startY = y
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(os.path.join("spriteAssets","text_default.png"))
        self.rect = pygame.Rect(self.x-24,self.y-27,48,54)
        self.size = self.image.get_size()
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*3), int(self.size[1]*3)))
        self.image = self.bigger_img
        self.state = 1
        self.count = 0
        self.movedX = 0
        self.movedY = 0
        self.health = 100
        self.prevMove = None
    def getRect(self):
        self.rect = pygame.Rect(self.x-24,self.y-27,48,54)
    def update(self,dx,dy):
        self.x = self.startX + self.movedX + dx
        self.y = self.startY + self.movedY + dy
        self.getRect()        
    def imageUpdateMove(self,dirX,dirY):
        self.count += 1
        if self.state == 0:
            self.image = pygame.image.load(os.path.join("spriteAssets","big_demon_idle_anim_f"+str(self.count//4%4)+".png"))
            self.rect = pygame.Rect(self.x-24,self.y-27,48,54)
            self.size = self.image.get_size()
            self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*3), int(self.size[1]*3)))
            self.image = self.bigger_img
            pass
        elif self.state == 1:
            self.movedX += self.speed*dirX
            self.movedY += self.speed*dirY
            self.image = pygame.image.load(os.path.join("spriteAssets","big_demon_run_anim_f"+str(self.count//4%4)+".png"))
            self.rect = pygame.Rect(self.x-24,self.y-27,48,54)
            self.size = self.image.get_size()
            self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*3), int(self.size[1]*3)))
            self.image = self.bigger_img
        self.getRect()
    def hit(self,dirX,dirY):
        self.health -= 25
        self.movedX -= 4*self.speed*dirX
        self.movedY -= 4*self.speed*dirY
        self.getRect()
