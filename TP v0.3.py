'''
pygamegame.py
framework created by Lukas Peraza
spritesheet.py taken from stackOverflow, link in file
sprites taken from itch.io

'''
import pygame, sys
import os
import random
import math
import time
from highscore import *
from classFiles.Walls import *
from classFiles.Weapons import *
from classFiles.Player import *
from classFiles.Misc import *
from classFiles.Map_Creator import *
from classFiles.spritesheet import *
from tkinter import *
from classFiles.spritesheet import *
from data import *
import random
import numpy as np

class Button(pygame.sprite.Sprite):
    def __init__(self,x,y,sizeX,sizeY,imageName,scale = 1):
        super(Button,self).__init__()
        self.x = x
        self.y = y
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.imageName = imageName
        self.image = pygame.image.load(os.path.join("spriteAssets",imageName))
        self.size = self.image.get_size()
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*scale), int(self.size[1]*scale)))
        self.image = self.bigger_img
        self.rect = pygame.Rect(self.x-self.sizeX/2,self.y-self.sizeY/2,self.sizeX,self.sizeY)
    def getRect(self):
        self.rect = pygame.Rect(self.x-self.sizeX/2,self.y-self.sizeY/2,self.sizeX,self.sizeY)

def createList(n):
    result = []
    for i in range(n):
        result += [0]
    return result

def cell(x,y):
    return ((y//50)*10 + x//60)

def printList(lst):
    count = 0
    for i in lst:
        count+=1
        if count%10 == 0:
            print('\n')
        print(i, end = " ")
            
        


class PygameGame(object):

    def init(self):
        ### Game States ###
        pygame.mouse.set_visible(False)
        self.gameState = "start"
        self.level = 1
        self.loadCount = 0
        self.spellCast = False
        self.currentSpell = []
        self.dragBoxDrawList = []
        self.data = []
        self.shootCount = 30
        self.timeSpent = 0
        self.monsterAmount = 0
        self.branchingCoeff = 0
        self.reflectChance = 5
        self.gameScore = 0
        # for backRow in range(l)
        ### Spell Cast ###
        self.multiSpellList = createList(100)
        ##Player##
        self.p = Player(300,200)
        self.dir = "Right"
        self.playerGroup = pygame.sprite.Group()
        self.playerGroup.add(self.p)
        self.playerCenterX = 20
        self.playerCenterY = 20
        self.emptyHeartGroup = pygame.sprite.Group()
        self.fullHeartGroup = pygame.sprite.Group()
        self.playerLevel = 1
        self.playerXP = 0
        self.playerMaxXP = 100 + self.playerLevel*50
        self.upgradesAvailable = 0
        ### ClickBox ###
        self.ClickBoxGroup = pygame.sprite.Group()
        ##Wand##
        self.wand = Wand(self.p.x,self.p.y)
        self.wandGroup = pygame.sprite.Group()
        self.wandGroup.add(self.wand)
        ##Pointer##
        self.Pointer = Pointer(0,0)
        self.PointerGroup = pygame.sprite.Group()
        self.PointerGroup.add(self.Pointer)
        ##Bullets##
        self.bulletGroup = pygame.sprite.Group()
        self.bulletSize = 10
        self.bulletSpeed = 10
        self.bulletReflectChance = 0
        self.bulletCount = 0
        ##Monster##
        self.monsterGroup = pygame.sprite.Group()
        ##Coins##
        self.coinsGroup = pygame.sprite.Group()
        self.coinsTextGroup = pygame.sprite.Group()
        ##Map##
        self.leftWallGroup = pygame.sprite.Group()
        self.rightWallGroup = pygame.sprite.Group()
        self.midWallTopGroup = pygame.sprite.Group()
        self.midWallBotGroup = pygame.sprite.Group()
        self.floorGroup = pygame.sprite.Group()
        self.exitGroup = pygame.sprite.Group()
        self.mapTuple = drunkWalk(createList2(50),100,25,25)
        self.map = tiling(magnify(removeIslands(self.mapTuple[0])))
        map = self.map
        self.mapSteps = self.mapTuple[1]
        self.mapStepCount = 0
        self.mapCount = 0
        
        for row in range(len(map)):
            for col in range(len(map[0])):
                if row == 76 and col == 76:
                    self.coinsGroup.add(Coin(24+(col-73)*24+200,(row-68)*24))
                if map[row][col] == "LEFT WALL":
                    self.leftWallGroup.add(LeftWall(24+(col-73)*24+200,(row-68)*24,96,56))
                elif map[row][col] == "RIGHT WALL":
                    self.rightWallGroup.add(RightWall(24+(col-73)*24+200,(row-68)*24,128,56))
                elif map[row][col] == "TOP WALL":
                    self.midWallTopGroup.add(MidWall(24+(col-73)*24+200,(row-68)*24,104,48))
                elif map[row][col] == "BOT WALL":
                    self.midWallBotGroup.add(MidWall(24+(col-73)*24+200,(row-68)*24,96,80))
                elif map[row][col] == "TOP RIGHT C":
                    self.rightWallGroup.add(RightWall(24+(col-73)*24+200,(row-68)*24,128,48))
                elif map[row][col] == "TOP LEFT C":
                    self.leftWallGroup.add(LeftWall(24+(col-73)*24+200,(row-68)*24,96,48))
                elif map[row][col] == "BOT RIGHT C":
                    self.rightWallGroup.add(RightWall(24+(col-73)*24+200,(row-68)*24,136,80))
                elif map[row][col] == "BOT LEFT C":
                    self.leftWallGroup.add(LeftWall(24+(col-73)*24+200,(row-68)*24,88,80))
                elif map[row][col] == "TOP RIGHT IN C":
                    self.leftWallGroup.add(LeftWall(24+(col-73)*24+200,(row-68)*24,104,80))
                    self.midWallBotGroup.add(MidWall(24+(col-73)*24+200,(row-68)*24,0,0))
                elif map[row][col] == "TOP LEFT IN C":
                    self.rightWallGroup.add(RightWall(24+(col-73)*24+200,(row-68)*24,120,80))
                    self.midWallBotGroup.add(MidWall(24+(col-73)*24+200,(row-68)*24,0,0))
                elif map[row][col] == "BOT LEFT IN C":
                    self.rightWallGroup.add(RightWall(24+(col-73)*24+200,(row-68)*24,128,64))
                    self.midWallTopGroup.add(MidWall(24+(col-73)*24+200,(row-68)*24,0,0))
                elif map[row][col] == "BOT RIGHT IN C":
                    self.leftWallGroup.add(LeftWall(24+(col-73)*24+200,(row-68)*24,96,64))
                    self.midWallTopGroup.add(MidWall(24+(col-73)*24+200,(row-68)*24,0,0))
                elif map[row][col] == "TOP FLAT":
                    self.floorGroup.add(Floor(24+(col-73)*24+200,(row-68)*24,112,56))
                elif map[row][col] == "TOP FLAT S":
                    self.floorGroup.add(Floor(24+(col-73)*24+200,(row-68)*24,104,56))
                elif map[row][col] == "BOT WALL S":
                    self.floorGroup.add(Floor(24+(col-73)*24+200,(row-68)*24,96,88))
                elif map[row][col] == "A":
                    if random.randint(1,30) == 1 and tileHash(map,row,col) == set() and abs(row-75)>6 and abs(col-75)>6:
                        self.monsterGroup.add(Monster(24+(col-73)*24+200-24,(row-68)*24-27,2)) 
                    self.floorGroup.add(Floor(24+(col-73)*24+200,(row-68)*24,79,27))
                if row == 76 and col == 76:
                    self.exitGroup.add(Exit(24+(col-73)*24+200,(row-68)*24,78,206,0,"industrial"))
        self.monsterAmount = len(self.monsterGroup)
        ##MISC.##
        self.dirx = 1
        self.diry = 1
        self.mouseX = 0
        self.mouseY = 0
        self.mouseAngle = 0
        self.xMargin = 0
        self.yMargin = 0
        self.NTx, self.NTy = 0, 0
        self.backGroundCount = 0
        self.backGroundSquares = []
        self.lvlGroup = pygame.sprite.Group()
        self.lvlGroup.add(LevelDisplay(135,100,0,(self.playerLevel-1)*48))
        self.dragBoxGroup = pygame.sprite.Group()
        self.dragBoxList = []
        ### Exp ###
        self.expGroup = pygame.sprite.Group()
        pygame.font.init()
        myfont = pygame.font.SysFont('Helvetica', 30)
        my2font = pygame.font.SysFont('Helvetica', 10)
        self.textsurface = my2font.render('Lvl.'+str(self.playerLevel), False, (0, 0, 0))
        self.upgradesText = myfont.render("Upgrades Available: " + str(self.upgradesAvailable), False, (0,0,0))
        self.overText = myfont.render("GAME OVER", False, (255,255,255))
        self.loadingText = myfont.render("LOADING...",False,(255,255,255))
        
        ### Start Screen ###
        self.buttonGroup = pygame.sprite.Group()

    def mousePressed(self, x, y):
        dirx = x-self.p.x
        diry = y-self.p.y
        l = math.sqrt(dirx**2 + diry**2)
        direction = [(x-self.p.x)/l,(y-self.p.y)/l]
        if self.gameState == "level" and self.shootCount > 10:
            self.bulletGroup.add(Bullet(self.bulletSize,self.p.x-self.xMargin,self.p.y-self.yMargin,self.bulletSpeed,direction))
            self.bulletGroup.update(self.xMargin,self.yMargin)
            self.shootCount = 0
        pass

    def mouseReleased(self, x, y):
        self.dragBoxGroup.empty()
        ### ClickBox ###
        self.ClickBoxGroup.add(ClickBox(x,y))
        self.currentSpell = self.dragBoxList
        self.currentSpell = []
        self.dragBoxList = []
        self.dragBoxDrawList = []
        self.data.append(self.multiSpellList)
        
        if classify(self.multiSpellList,data)["Vert"] < 500 and classify(self.multiSpellList,data)["Blossom"] < 500:
            pass
        elif classify(self.multiSpellList,data)["Blossom"] > 800 and classify(self.multiSpellList,data)["Vert"] > 1500 and classify(self.multiSpellList,data)["Ho"] < 1.5:
            self.bulletGroup.add(Bullet(50,self.p.x-self.xMargin+20,self.p.y-self.yMargin+40,self.bulletSpeed,[0,1]))
            self.bulletGroup.add(Bullet(50,self.p.x-self.xMargin+20,self.p.y-self.yMargin+40,self.bulletSpeed,[0,-1]))
            self.bulletGroup.add(Bullet(50,self.p.x-self.xMargin+20,self.p.y-self.yMargin+65,self.bulletSpeed,[0,1]))
            self.bulletGroup.add(Bullet(50,self.p.x-self.xMargin+20,self.p.y-self.yMargin+15,self.bulletSpeed,[0,-1]))
            self.bulletGroup.add(Bullet(50,self.p.x-self.xMargin+20,self.p.y-self.yMargin+90,self.bulletSpeed,[0,1]))
            self.bulletGroup.add(Bullet(50,self.p.x-self.xMargin+20,self.p.y-self.yMargin-10,self.bulletSpeed,[0,-1]))
            self.gameScore += 500
        elif classify(self.multiSpellList,data)["Vert"] < 500 and classify(self.multiSpellList,data)["Blossom"] > 1200:
            self.bulletGroup.add(Bullet(50,self.p.x-self.xMargin,self.p.y-self.yMargin+40,self.bulletSpeed,[1,0]))
            self.bulletGroup.add(Bullet(50,self.p.x-self.xMargin,self.p.y-self.yMargin+40,self.bulletSpeed,[-1,0]))
            self.bulletGroup.add(Bullet(50,self.p.x-self.xMargin+25,self.p.y-self.yMargin+40,self.bulletSpeed,[1,0]))
            self.bulletGroup.add(Bullet(50,self.p.x-self.xMargin-25,self.p.y-self.yMargin+40,self.bulletSpeed,[-1,0]))
            self.bulletGroup.add(Bullet(50,self.p.x-self.xMargin+50,self.p.y-self.yMargin+40,self.bulletSpeed,[1,0]))
            self.bulletGroup.add(Bullet(50,self.p.x-self.xMargin-50,self.p.y-self.yMargin+40,self.bulletSpeed,[-1,0]))
            self.gameScore += 500
        elif classify(self.multiSpellList,data)["Blossom"] < 1500 and classify(self.multiSpellList,data)["Vert"] > 3500:
            for i in range(36):
                self.bulletGroup.add(Bullet(self.bulletSize,self.p.x-self.xMargin,self.p.y-self.yMargin,self.bulletSpeed,[math.cos(math.pi*i/18),math.sin(math.pi*i/18)]))
            self.gameScore += 1000
            
        self.multiSpellList = createList(100)
        pass

    def mouseMotion(self, x, y):
        self.mouseX = x
        self.mouseY = y
        self.NTx = x-self.p.startX
        self.NTy = y-self.p.startY
        dirx = self.dirx
        diry = self.diry
        l = math.sqrt(dirx**2 + diry**2)
        direction = [(x-self.p.x)/l,(y-self.p.y)/l]
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
        self.wand.rotateImage(angle)
        self.mouseAngle = angle

        self.Pointer.x = x-8
        self.Pointer.y = y-8
        if x>self.p.x:
            self.dir = "Right"
        else:
            self.dir = "Left"
        

        pass

    def mouseDrag(self, x, y):
        self.bulletCount += 1
        self.mouseX = x
        self.mouseY = y
        self.NTx = x-self.p.startX
        self.NTy = y-self.p.startY
        dirx = self.dirx
        diry = self.diry
        l = math.sqrt(dirx**2 + diry**2)
        direction = [(x-self.p.x)/l,(y-self.p.y)/l]
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
        self.wand.rotateImage(angle)
        self.mouseAngle = angle

        self.Pointer.x = x-8
        self.Pointer.y = y-8
        if x>self.p.x:
            self.dir = "Right"
        else:
            self.dir = "Left"
        # 
        # if self.bulletCount%10 < 3:
        #     dirx = x-self.p.x
        #     diry = y-self.p.y
        #     l = math.sqrt(dirx**2 + diry**2)
        #     direction = [(x-self.p.x)/l,(y-self.p.y)/l]
        #     self.bulletGroup.add(Bullet(self.bulletSize,self.p.x-self.xMargin,self.p.y-self.yMargin,self.bulletSpeed,direction))
        #     self.bulletGroup.update(self.xMargin,self.yMargin)
        
        if self.spellCast == True:
            self.dragBoxGroup.add(DragBox(x,y))
            self.dragBoxDrawList.append((x,y))
            if len(self.dragBoxList) == 0 or quadrant(x,y) != self.dragBoxList[-1]:
                self.dragBoxList.append(quadrant(x,y))
            
            tmp = cell(x,y)
            if tmp < 100:
                self.multiSpellList[tmp] = 1
            
        pass

    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_a:
            self.p.xSpeed = -6
        if keyCode == pygame.K_d:
            self.p.xSpeed = 6
        if keyCode == pygame.K_w:
            self.p.ySpeed = -6
        if keyCode == pygame.K_s:
            self.p.ySpeed = 6
        if keyCode == pygame.K_LSHIFT :
            self.spellCast = True
        if keyCode == pygame.K_p:
            self.monsterGroup.empty()
        if self.gameState == "intro":
            if keyCode == pygame.K_k:
                self.gameState = "level"
                
        pass

    def keyReleased(self, keyCode, modifier):
        if keyCode == pygame.K_a:
            if self.p.xSpeed != 6:
                self.p.xSpeed = 0
        if keyCode == pygame.K_d:
            if self.p.xSpeed != -6:
                self.p.xSpeed = 0
        if keyCode == pygame.K_w:
            if self.p.ySpeed != 6:
                self.p.ySpeed = 0
        if keyCode == pygame.K_s:
            if self.p.ySpeed != -6:
                self.p.ySpeed = 0
        if keyCode == pygame.K_LSHIFT:
            self.spellCast = False
        pass

    def timerFired(self, dt):
        self.shootCount += 1
        if self.gameState == "map":
            self.mapCount +=1
            self.mapStepCount = min([self.mapCount,len(self.mapSteps)-1])
            if self.mapCount == (len(self.mapSteps)-1) + 120:
                self.mapStepCount = 0
                self.mapCount = 0
                self.gameState = "level"
        ### Death ###
        if self.p.playerHealth == 0:
            self.gameState = "GAME OVER"
        ### Level Load
        if self.gameState == "load":
            self.loadCount += 1
            if self.loadCount > 60:
                self.loadCount = 0
                self.gameState = "loading"
        if self.gameState == "loading":
            self.branchingCoeff = max([self.branchingCoeff,self.timeSpent/self.monsterAmount])
            self.timeSpent = 0
            self.exitGroup.empty()
            self.leftWallGroup.empty()
            self.rightWallGroup.empty()
            self.midWallBotGroup.empty()
            self.midWallTopGroup.empty()
            self.floorGroup.empty()
            self.mapTuple = drunkWalk(createList2(50),min([100+self.level*20,800]),25,25,max([10000-self.level*500-int(self.branchingCoeff),2000]))
            self.map = tiling(magnify(removeIslands(self.mapTuple[0])))
            map = self.map
            self.mapSteps = self.mapTuple[1]
            self.mapStepCount = 0
            self.level += 1
            
            for row in range(len(map)):
                for col in range(len(map[0])):
                    if map[row][col] == "LEFT WALL":
                        self.leftWallGroup.add(LeftWall(24+(col-73)*24+200,(row-68)*24,96,56))
                    elif map[row][col] == "RIGHT WALL":
                        self.rightWallGroup.add(RightWall(24+(col-73)*24+200,(row-68)*24,128,56))
                    elif map[row][col] == "TOP WALL":
                        self.midWallTopGroup.add(MidWall(24+(col-73)*24+200,(row-68)*24,104,48))
                    elif map[row][col] == "BOT WALL":
                        self.midWallBotGroup.add(MidWall(24+(col-73)*24+200,(row-68)*24,96,80))
                    elif map[row][col] == "TOP RIGHT C":
                        self.rightWallGroup.add(RightWall(24+(col-73)*24+200,(row-68)*24,128,48))
                    elif map[row][col] == "TOP LEFT C":
                        self.leftWallGroup.add(LeftWall(24+(col-73)*24+200,(row-68)*24,96,48))
                    elif map[row][col] == "BOT RIGHT C":
                        self.rightWallGroup.add(RightWall(24+(col-73)*24+200,(row-68)*24,136,80))
                    elif map[row][col] == "BOT LEFT C":
                        self.leftWallGroup.add(LeftWall(24+(col-73)*24+200,(row-68)*24,88,80))
                    elif map[row][col] == "TOP RIGHT IN C":
                        self.leftWallGroup.add(LeftWall(24+(col-73)*24+200,(row-68)*24,104,80))
                        self.midWallBotGroup.add(MidWall(24+(col-73)*24+200,(row-68)*24,0,0))
                    elif map[row][col] == "TOP LEFT IN C":
                        self.rightWallGroup.add(RightWall(24+(col-73)*24+200,(row-68)*24,120,80))
                        self.midWallBotGroup.add(MidWall(24+(col-73)*24+200,(row-68)*24,0,0))
                    elif map[row][col] == "BOT LEFT IN C":
                        self.rightWallGroup.add(RightWall(24+(col-73)*24+200,(row-68)*24,128,64))
                        self.midWallTopGroup.add(MidWall(24+(col-73)*24+200,(row-68)*24,0,0))
                    elif map[row][col] == "BOT RIGHT IN C":
                        self.leftWallGroup.add(LeftWall(24+(col-73)*24+200,(row-68)*24,96,64))
                        self.midWallTopGroup.add(MidWall(24+(col-73)*24+200,(row-68)*24,0,0))
                    elif map[row][col] == "TOP FLAT":
                        self.floorGroup.add(Floor(24+(col-73)*24+200,(row-68)*24,112,56))
                    elif map[row][col] == "TOP FLAT S":
                        self.floorGroup.add(Floor(24+(col-73)*24+200,(row-68)*24,104,56))
                    elif map[row][col] == "BOT WALL S":
                        self.floorGroup.add(Floor(24+(col-73)*24+200,(row-68)*24,96,88))
                    elif map[row][col] == "A":
                        self.floorGroup.add(Floor(24+(col-73)*24+200,(row-68)*24,79,27))
                        if random.randint(1,max([30-2*self.level,10])) == 3 and tileHash(map,row,col) == set() and abs(row-75)>6 and\
                        abs(col-75)>6:
                            self.monsterGroup.add(Monster(24+(col-73)*24+200-24,(row-68)*24-27,2)) 
                        self.floorGroup.add(Floor(24+(col-73)*24+200,(row-68)*24,79,27))
                    if row == 76 and col == 76:
                        self.exitGroup.add(Exit(24+(col-73)*24+200,(row-68)*24,78,206,0,"industrial"))
                    self.monsterAmount = len(self.monsterGroup)
                    if self.upgradesAvailable > 0:
                        self.gameState = "upgrades"
                    else:
                        self.gameState = "map"
                
        
        ### LEVEL ###
        if self.gameState == "level":
            self.timeSpent += 1
            ##Player Position##
            self.p.imageUpdate(self.dir)
            ##Player Collision##
            if pygame.sprite.groupcollide(self.leftWallGroup,self.playerGroup,False,False) != {} and self.p.xSpeed != 0:
                self.xMargin -= abs(self.p.xSpeed) + 0.9
            if pygame.sprite.groupcollide(self.rightWallGroup,self.playerGroup,False,False) != {} and self.p.xSpeed != 0:
                self.xMargin += abs(self.p.xSpeed) + 0.9
            if pygame.sprite.groupcollide(self.midWallTopGroup,self.playerGroup,False,False) != {} and self.p.ySpeed != 0:
                self.yMargin -= abs(self.p.ySpeed) + 0.9
            if pygame.sprite.groupcollide(self.midWallBotGroup,self.playerGroup,False,False) != {} and self.p.ySpeed != 0:
                self.yMargin += abs(self.p.ySpeed) + 0.9
            ##EXP Update##
            self.playerMaxXP = 100 + self.playerLevel*50
            if self.playerXP > self.playerMaxXP:
                self.playerXP -= self.playerMaxXP
                self.playerLevel += 1
                self.upgradesAvailable += 1
            ##Margin Update##
            self.xMargin -= self.p.xSpeed
            self.yMargin -= self.p.ySpeed
            NTx, NTy = 0.1*self.NTx, 0.1*self.NTy
            self.leftWallGroup.update(self.xMargin-NTx,self.yMargin-NTy)
            self.rightWallGroup.update(self.xMargin-NTx,self.yMargin-NTy)
            self.midWallTopGroup.update(self.xMargin-NTx,self.yMargin-NTy)
            self.midWallBotGroup.update(self.xMargin-NTx,self.yMargin-NTy)
            self.floorGroup.update(self.xMargin-NTx,self.yMargin-NTy)
            self.bulletGroup.update(self.xMargin-NTx,self.yMargin-NTy)
            self.coinsGroup.update(self.xMargin-NTx,self.yMargin-NTy)
            self.coinsTextGroup.update(self.xMargin-NTx,self.yMargin-NTy)
            self.expGroup.update(self.xMargin-NTx,self.yMargin-NTy)
            self.exitGroup.update(self.xMargin-NTx,self.yMargin-NTy)
            self.p.x = self.p.startX - NTx
            self.p.y = self.p.startY - NTy
            self.p.getRect()
            ##Wand Rotation##
            self.wand.rotateUpdate(self.mouseX, self.mouseY, self.p.x, self.p.y)
            ##Bullet Collisions##
            for bullet in pygame.sprite.groupcollide(self.bulletGroup,self.leftWallGroup,False,False):
                if random.randint(1,self.reflectChance) == 1:
                    bullet.direction[0] *= -1
                else:
                    self.bulletGroup.remove(bullet)
            for bullet in pygame.sprite.groupcollide(self.bulletGroup,self.rightWallGroup,False,False):
                if random.randint(1,self.reflectChance) == 1:
                    bullet.direction[0] *= -1
                else:
                    self.bulletGroup.remove(bullet)
            for bullet in pygame.sprite.groupcollide(self.bulletGroup,self.midWallTopGroup,False,False):
                if random.randint(1,self.reflectChance) == 1:
                    bullet.direction[1] *= -1
                else:
                    self.bulletGroup.remove(bullet)
            for bullet in pygame.sprite.groupcollide(self.bulletGroup,self.midWallBotGroup,False,False):
                if random.randint(1,self.reflectChance) == 1:
                    bullet.direction[1] *= -1
                else:
                    self.bulletGroup.remove(bullet)
            ##Coins Collision##
            for coin in pygame.sprite.groupcollide(self.coinsGroup,self.playerGroup,True,False):
                for coinText in self.coinsTextGroup:
                    if coin.x == coinText.x and coin.y == coinText.y:
                        self.coinsTextGroup.remove(coinText)
            for coinText in self.coinsTextGroup:
                if coinText in pygame.sprite.groupcollide(self.coinsTextGroup,self.playerGroup,False,False):
                    coinText.imageUpdate(True)
                else:
                    coinText.imageUpdate(False)
            ##Monster##
            self.monsterGroup.update(self.xMargin-NTx,self.yMargin-NTy)
            for monster in self.monsterGroup:
                directionX = (self.p.x - monster.x)
                directionY = (self.p.y - monster.y)
                h = math.sqrt(directionX**2 + directionY**2)
                directionX /= h
                directionY /= h
                if h <= 300:
                    monster.state = 1
                    monster.imageUpdateMove(directionX,directionY)
                else:
                    monster.state = 0
                    monster.imageUpdateMove(directionX,directionY)
            for monster in pygame.sprite.groupcollide(self.monsterGroup,self.leftWallGroup,False,False):
                monster.imageUpdateMove(2,0)
            for monster in pygame.sprite.groupcollide(self.monsterGroup,self.rightWallGroup,False,False):
                monster.imageUpdateMove(-2,0)
            for monster in pygame.sprite.groupcollide(self.monsterGroup,self.midWallTopGroup,False,False):
                monster.imageUpdateMove(0,2)
            for monster in pygame.sprite.groupcollide(self.monsterGroup,self.midWallBotGroup,False,False):
                monster.imageUpdateMove(0,-2)

            for monster in pygame.sprite.groupcollide(self.monsterGroup,self.bulletGroup,False,True):
                directionX = (self.p.x - monster.x)
                directionY = (self.p.y - monster.y)
                h = math.sqrt(directionX**2 + directionY**2)
                directionX /= h
                directionY /= h
                monster.hit(directionX,directionY)
                if monster.health <= 0:
                    self.expGroup.add(Exp(monster.x,monster.y,self.xMargin,self.yMargin))
                    self.monsterGroup.remove(monster)
                    self.gameScore += 500

            self.p.damageCount += 1
            if self.p.damageCount >= 45 and pygame.sprite.groupcollide(self.playerGroup,self.monsterGroup,False,False) != {}:
                self.p.damageCount = 0
                self.p.playerHealth -= 1
                angle = (random.randint(1,360)/180)*math.pi
                self.xMargin -= 20*math.cos(angle)
                self.yMargin -= 20*math.sin(angle)
            if len(self.monsterGroup) == 0:
                for exit in self.exitGroup:
                    if exit.state == 0:
                        exit.state = 1
                
            ### Exp ###
            for exp in self.expGroup:
                directionX = (self.p.x - exp.x)
                directionY = (self.p.y - exp.y)
                h = math.sqrt(directionX**2 + directionY**2)
                directionX /= h
                directionY /= h
                if h <= 100:
                    exp.state = 1
                    exp.imageUpdate(directionX,directionY)
                else:
                    exp.state = 0
                    exp.imageUpdate(directionX,directionY)
            
            for gained in pygame.sprite.groupcollide(self.playerGroup,self.expGroup,False,True):
                self.playerXP += 40

            pygame.font.init()
            my2font = pygame.font.SysFont('Helvetica', 15)
            self.textsurface = my2font.render('LVL.'+str(self.playerLevel), False, (0, 0, 0))


            ### Exit ###
            for exit in self.exitGroup:
                if exit.state == 1:
                    if pygame.sprite.groupcollide(self.playerGroup,self.exitGroup,False,False) == {}:
                        exit.framecount = 0
                        exit.stateUpdate()
                    else:
                        exit.stateUpdate()
                if exit.state == 2:
                    if pygame.sprite.groupcollide(self.playerGroup,self.exitGroup,False,False) != {}:
                        self.gameState = "load"
            
            
                    
            ### Health Display ###
            self.emptyHeartGroup.empty()
            self.fullHeartGroup.empty()
            for i in range(self.p.playerHealthFull//2):
                self.emptyHeartGroup.add(Button(40+25*i,40,24,24,"ui_heart_empty.png",1.5))
            for j in range(self.p.playerHealth//2):
                self.fullHeartGroup.add(Button(40+25*j,40,24,24,"ui_heart_full.png",1.5))
            if int(self.p.playerHealth)%2 != 0:
                self.fullHeartGroup.add(Button(40+25*(self.p.playerHealth//2),40,24,24,"ui_heart_half.png",1.5))
            
            ### Background ###
            self.backGroundCount += 1
            if self.backGroundCount%2 == 1:
                self.backGroundSquares.append([random.randint(1,600),600,random.randint(200,300),0])
            for square in self.backGroundSquares:
                square[1] -= 100
                square[3] += 1
                if square[3] == 100:
                    self.backGroundSquares.remove(square)
        

        
        
        if self.gameState == "start":
            self.buttonGroup.empty()
            self.buttonGroup.add(Button(300,400,180,99,"play_button.png"))
            if pygame.sprite.groupcollide(self.ClickBoxGroup,self.buttonGroup,False,False) != {}:
                self.gameState = "intro"
                
        if self.gameState == "upgrades":
            pygame.font.init()
            myfont = pygame.font.SysFont('Helvetica', 30)
            self.upgradesText = myfont.render("Upgrades Available: " + str(self.upgradesAvailable), False, (0,0,0))
            self.backGroundCount += 1
            if self.backGroundCount%2 == 1:
                self.backGroundSquares.append([random.randint(1,600),600,random.randint(200,300),0])
            for square in self.backGroundSquares:
                square[1] -= 100
                square[3] += 1
                if square[3] == 100:
                    self.backGroundSquares.remove(square)
            self.buttonGroup.empty()
            self.buttonGroup.add(Button(300,105,306,150,"bullSizeUp.png"))
            self.buttonGroup.add(Button(300,255,306,150,"bullSpeedUp.png"))
            self.buttonGroup.add(Button(300,405,306,150,"bullReflectUp.png"))
            for button in pygame.sprite.groupcollide(self.buttonGroup,self.ClickBoxGroup,False,False):
                if button.imageName == "bullSizeUp.png":
                    self.bulletSize *= 1.2
                    self.upgradesAvailable -= 1
                elif button.imageName == "bullSpeedUp.png":
                    self.bulletSpeed += 2
                    self.upgradesAvailable -= 1
                elif button.imageName == "bullReflectUp.png":
                    self.bulletReflectChance = max([self.reflectChance-1,1])
                    self.upgradesAvailable -= 1
                if self.upgradesAvailable == 0:
                    self.gameState = "map"

        self.ClickBoxGroup.empty()
        
        
        ##Pointer##
        self.Pointer.update()
        pass

    def redrawAll(self, screen):
        screen.fill((61,61,61))
        ############################################################
        # pygame.draw.rect(screen, (200,200,200), self.p.rect)
        # pygame.draw.rect(screen, (200,200,200), self.Pointer.rect)
        ############################################################
        if self.gameState == "start":
            self.buttonGroup.draw(screen)
            titleGroup = pygame.sprite.Group()
            titleGroup.add(Button(300,202,490,144,"NEON.png",2))
            titleGroup.draw(screen)
            pass
        elif self.gameState == "upgrades":
            screen.blit(self.upgradesText,(0,0))
            for square in self.backGroundSquares:
                pygame.draw.rect(screen, (103,103,103), [square[0],square[1],10,square[2]])
            self.buttonGroup.draw(screen)
            pass
        elif self.gameState == "load":
            screen.blit(self.loadingText,(205,239))
            pass
        elif self.gameState == "intro":
            introGroup = pygame.sprite.Group()
            introGroup.add(Button(300,252,540,240,"instructions.png",0.4))
            introGroup.add(Button(300,400,210,72,"kStart.png",0.4))
            introGroup.draw(screen)
            
        elif self.gameState == "level":    
            for square in self.backGroundSquares:
                pygame.draw.rect(screen, (103,103,103), [square[0],square[1],10,square[2]])
            self.floorGroup.draw(screen)
            self.exitGroup.draw(screen)
            self.midWallTopGroup.draw(screen)
            self.midWallBotGroup.draw(screen)
            self.leftWallGroup.draw(screen)
            self.rightWallGroup.draw(screen)
            self.bulletGroup.draw(screen)
            self.coinsGroup.draw(screen)
            self.monsterGroup.draw(screen)
            self.coinsTextGroup.draw(screen)
            pygame.draw.rect(screen,(43, 255, 78), [30,60,100*(self.playerXP/self.playerMaxXP),10])
            pygame.draw.rect(screen,(255, 255, 255), [30,60,100,10],3)
            if self.mouseAngle < 180:
                self.wandGroup.draw(screen)
            self.playerGroup.draw(screen)
            if self.mouseAngle > 180:
                self.wandGroup.draw(screen)
            self.emptyHeartGroup.draw(screen)
            self.fullHeartGroup.draw(screen)
            self.expGroup.draw(screen)
            # self.lvlGroup.draw(screen)
            screen.blit(self.textsurface,(140,58))
            my4font = pygame.font.SysFont('Helvetica', 15)
            self.scoretext = my4font.render('SCORE: '+str(self.gameScore),False, (0,0,0))
            screen.blit(self.scoretext,(30, 80))
            self.dragBoxGroup.draw(screen)
            if self.spellCast == True:
                pygame.draw.circle(screen, (103,103,103), [300,252], 140, 4)
                pygame.draw.line(screen, (103,103,103), [300,50], [300,454], 4)
                pygame.draw.line(screen, (103,103,103), [50,252], [550,252], 4)
            if len(self.dragBoxDrawList) > 1:
                pygame.draw.lines(screen,(103,103,103),False,self.dragBoxDrawList,5)
            
        elif self.gameState == "map":
            my3font = pygame.font.SysFont('Helvetica', 10)
            self.maploadingText1 = my3font.render("GENERATING MAP...",True,(255,255,255))
            self.maploadingText2 = my3font.render("LEVEL : "+str(self.level),True,(255,255,255))
            self.maploadingText3 = my3font.render("BRANCHING VAR. : "+str(round(100/(max([10000-self.level*500-self.branchingCoeff,2000])),6)),True,(255,255,255))
            for row in range(len(self.mapSteps[0])):
                for col in range(len(self.mapSteps[0][0])):
                    if self.mapSteps[self.mapStepCount][row][col] == "A" or row == 49 or row == 0 or col == 49 or col == 0:
                        pygame.draw.rect(screen, (255,255,255), [row*10+50,col*10+2,10,10])
            screen.blit(self.maploadingText1, (70,25))
            screen.blit(self.maploadingText2, (70,40))
            screen.blit(self.maploadingText3, (70,55))
        
        elif self.gameState == "GAME OVER":
            screen.blit(self.overText,(205,159))
            global highscore
            tmp = highscore + [self.gameScore]
            tmp = sorted(tmp)[::-1]
            tmp = tmp[:3]
            name = open("highscore.py", "w") #opens file usernames.txt and gets ready to write to it
            name.write("highscore = " + str(tmp)) #writes contents in file to usernames.txt
            name.close() #closes file
            my5font = pygame.font.SysFont('Helvetica', 20)
            self.highscoreText = my5font.render("HIGH SCORES", True, (255,255,255))
            self.highscoreText1 = my5font.render("1: " + str(tmp[0]), True, (255,255,255))
            self.highscoreText2 = my5font.render("2: " + str(tmp[1]), True, (255,255,255))
            self.highscoreText3 = my5font.render("3: " + str(tmp[2]), True, (255,255,255))
            screen.blit(self.highscoreText, (205,220))
            screen.blit(self.highscoreText1, (205,240))
            screen.blit(self.highscoreText2, (205,260))
            screen.blit(self.highscoreText3, (205,280))
        self.PointerGroup.draw(screen)

        pass

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=600, height=504, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

    def run(self):
        # pygame.mixer.music.load("loop.mp3")
        # pygame.mixer.music.play(-1,0.0)
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False

            
            pygame.display.flip()

        pygame.quit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()