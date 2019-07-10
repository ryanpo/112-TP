'''
pygamegame.py
created by Lukas Peraza
 for 15-112 F15 Pygame Optional Lecture, 11/11/15
use this code in your term project if you want
- CITE IT
- you can modify it to your liking
  - BUT STILL CITE IT
- you should remove the print calls from any function you aren't using
- you might want to move the pygame.display.flip() to your redrawAll function,
    in case you don't need to update the entire display every frame (then you
    should use pygame.display.update(Rect) instead)
'''
import pygame
import os
import random
import math
from Walls import *
from Weapons import *
from Player import *


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super(Bullet,self).__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.image = None
        self.rect = pygame.Rect(self.x-2,self.y-2,4,4)
        self.size = self.image.get_size()
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*2), int(self.size[1]*2)))
        self.image = self.bigger_img
    def getRect(self):
        self.rect = pygame.Rect(self.x,self.y,4,4)
    def update(self):
        self.x += self.speed*self.direction[0]
        self.y += self.speed*self.direction[1]
        self.getRect()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction):
        super(Bullet,self).__init__()
        self.x = x
        self.y = y
        self.baseX = x
        self.baseY = y
        self.speed = speed
        self.direction = direction
        self.image = pygame.image.load(os.path.join("spriteAssets","bullet.png"))
        self.rect = pygame.Rect(self.x-2,self.y-2,4,4)
        self.size = self.image.get_size()
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*2), int(self.size[1]*2)))
        self.image = self.bigger_img
    def getRect(self):
        self.rect = pygame.Rect(self.x-2,self.y-2,4,4)
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

class PygameGame(object):

    def init(self):
        ##Player##
        self.p = Player(300,200)
        self.dir = "Right"
        self.playerGroup = pygame.sprite.Group()
        self.playerGroup.add(self.p)
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
        ##Left Walls##
        self.leftWallGroup = pygame.sprite.Group()
        self.leftWallGroup.add(LeftWall(24,24,"Top1"))
        self.leftWallGroup.add(LeftWall(24,48,"Top2"))
        for i in range(3,15):
            x, y = 0, i*24
            self.leftWallGroup.add(LeftWall(24,y,"Mid"))
        self.leftWallGroup.add(LeftWall(24,360,"Bot1"))
        self.leftWallGroup.add(LeftWall(24,384,"Bot2"))
        ##Right Walls##
        self.rightWallGroup = pygame.sprite.Group()
        self.rightWallGroup.add(RightWall(552,24,"Top1"))
        self.rightWallGroup.add(RightWall(552,48,"Top2"))
        for i in range(3,15):
            x, y = 0, i*24
            self.rightWallGroup.add(RightWall(552,y,"Mid"))
        self.rightWallGroup.add(RightWall(552,360,"Bot1"))
        self.rightWallGroup.add(RightWall(552,384,"Bot2"))
        ##Mid Walls##
        self.midWallTopGroup = pygame.sprite.Group()
        self.midWallBotGroup = pygame.sprite.Group()
        for i in range(22):
            self.midWallTopGroup.add(MidWall(48+i*24,24,"Top1"))
            self.midWallTopGroup.add(MidWall(48+i*24,48,"Top2"))
        for i in range(22):
            self.midWallBotGroup.add(MidWall(48+i*24,360,"Bot1"))
            self.midWallBotGroup.add(MidWall(48+i*24,384,"Bot2"))
        ##Floors##
        self.floorGroup = pygame.sprite.Group()
        for row in range(23):
            for col in range(3,16):
                self.floorGroup.add(Floor(24+row*24,col*24))
        ##MISC.##
        self.dirx = 1
        self.diry = 1
        self.mouseX = 0
        self.mouseY = 0
        self.mouseAngle = 0
        self.xMargin = 0
        self.yMargin = 0
        pass

    def mousePressed(self, x, y):
        dirx = x-self.p.x
        diry = y-self.p.y
        l = math.sqrt(dirx**2 + diry**2)
        direction = [(x-self.p.x)/l,(y-self.p.y)/l]
        self.bulletGroup.add(Bullet(self.p.x-self.xMargin,self.p.y-self.yMargin,5,direction))
        self.bulletGroup.update(self.xMargin,self.yMargin)
        # self.p.x -= 6*direction[0]
        # self.p.y -= 6*direction[1]
        # if pygame.sprite.groupcollide(self.leftWallGroup,self.playerGroup,False,False) != {}:
        #     self.p.x += 6*direction[0]
        # if pygame.sprite.groupcollide(self.rightWallGroup,self.playerGroup,False,False) != {}:
        #     self.p.x += 6*direction[0]
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        self.mouseX = x
        self.mouseY = y
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
        pass

    def keyPressed(self, keyCode, modifier):
        if keyCode == pygame.K_a:
            self.p.xSpeed = -3
        if keyCode == pygame.K_d:
            self.p.xSpeed = 3
        if keyCode == pygame.K_w:
            self.p.ySpeed = -3
        if keyCode == pygame.K_s:
            self.p.ySpeed = 3
        pass

    def keyReleased(self, keyCode, modifier):
        if keyCode == pygame.K_a:
            if self.p.xSpeed != 3:
                self.p.xSpeed = 0
        if keyCode == pygame.K_d:
            if self.p.xSpeed != -3:
                self.p.xSpeed = 0
        if keyCode == pygame.K_w:
            if self.p.ySpeed != 3:
                self.p.ySpeed = 0
        if keyCode == pygame.K_s:
            if self.p.ySpeed != -3:
                self.p.ySpeed = 0
        pass

    def timerFired(self, dt):
        ##Player Position##
        self.p.update()
        self.p.imageUpdate(self.dir)
        ##Player Collision##
        if pygame.sprite.groupcollide(self.leftWallGroup,self.playerGroup,False,False) != {}:
            self.xMargin += self.p.xSpeed
        if pygame.sprite.groupcollide(self.rightWallGroup,self.playerGroup,False,False) != {}:
            self.xMargin += self.p.xSpeed
        if pygame.sprite.groupcollide(self.midWallTopGroup,self.playerGroup,False,False) != {}:
            self.yMargin += self.p.ySpeed
        if pygame.sprite.groupcollide(self.midWallBotGroup,self.playerGroup,False,False) != {}:
            self.yMargin += self.p.ySpeed
        ##Margin Update##
        if self.p.x > 305 or self.p.x < 295 or self.p.y < 195 or self.p.y > 205:
            self.p.unupdate()
            self.xMargin -= self.p.xSpeed
            self.yMargin -= self.p.ySpeed
            self.leftWallGroup.update(self.xMargin,self.yMargin)
            self.rightWallGroup.update(self.xMargin,self.yMargin)
            self.midWallTopGroup.update(self.xMargin,self.yMargin)
            self.midWallBotGroup.update(self.xMargin,self.yMargin)
            self.floorGroup.update(self.xMargin,self.yMargin)
            self.bulletGroup.update(self.xMargin,self.yMargin)
        else:
            self.bulletGroup.update(self.xMargin,self.yMargin)
        ##Pointer##
        self.Pointer.update()
        ##Wand Rotation##
        self.wand.rotateUpdate(self.mouseX, self.mouseY, self.p.x, self.p.y)
        ##Bullet Collisions##
        pygame.sprite.groupcollide(self.leftWallGroup,self.bulletGroup,False,True)
        pygame.sprite.groupcollide(self.rightWallGroup,self.bulletGroup,False,True)
        pygame.sprite.groupcollide(self.midWallTopGroup,self.bulletGroup,False,True)
        pygame.sprite.groupcollide(self.midWallBotGroup,self.bulletGroup,False,True)
        
        pass

    def redrawAll(self, screen):
        screen.fill((45, 45, 45))
        ############################################################
        # pygame.draw.rect(screen, (200,200,200), self.p.rect)
        # pygame.draw.rect(screen, (200,200,200), self.Pointer.rect)
        ############################################################
        self.floorGroup.draw(screen)
        self.leftWallGroup.draw(screen)
        self.midWallTopGroup.draw(screen)
        self.midWallBotGroup.draw(screen)
        self.rightWallGroup.draw(screen)
        self.bulletGroup.draw(screen)
        if self.mouseAngle < 180:
            self.wandGroup.draw(screen)
        self.playerGroup.draw(screen)
        self.PointerGroup.draw(screen)
        if self.mouseAngle > 180:
            self.wandGroup.draw(screen)
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
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()