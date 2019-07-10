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
from Maps import *
from Misc import *
from Map_Creator import *


        
    

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
        self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*1.5), int(self.size[1]*1.5)))
        self.image = self.bigger_img
        self.state = 1
        self.count = 0
        self.movedX = 0
        self.movedY = 0
        self.health = 100
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
            self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*1.5), int(self.size[1]*1.5)))
            self.image = self.bigger_img
            pass
        elif self.state == 1:
            self.movedX += self.speed*dirX
            self.movedY += self.speed*dirY
            self.image = pygame.image.load(os.path.join("spriteAssets","big_demon_run_anim_f"+str(self.count//4%4)+".png"))
            self.rect = pygame.Rect(self.x-24,self.y-27,48,54)
            self.size = self.image.get_size()
            self.bigger_img = pygame.transform.scale(self.image, (int(self.size[0]*1.5), int(self.size[1]*1.5)))
            self.image = self.bigger_img
        self.getRect()
    def hit(self,dirX,dirY):
        self.health -= 25
        self.movedX -= 4*self.speed*dirX
        self.movedY -= 4*self.speed*dirY
        self.getRect()



class PygameGame(object):

    def init(self):
        ##Player##
        self.p = Player(300,200)
        self.dir = "Right"
        self.playerGroup = pygame.sprite.Group()
        self.playerGroup.add(self.p)
        self.playerCenterX = 20
        self.playerCenterY = 20
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
        self.bulletCount = 0
        ##Map##
        self.leftWallGroup = pygame.sprite.Group()
        self.rightWallGroup = pygame.sprite.Group()
        self.midWallTopGroup = pygame.sprite.Group()
        self.midWallBotGroup = pygame.sprite.Group()
        self.floorGroup = pygame.sprite.Group()
        map = magnify(removeIslands(drunkWalk(createList2(50),400,25,25)))
        '''
        key:
        A: base
        B: LT1
        C: LT2
        D: LMD
        E: LB1
        F: LB2
        G: RT1
        H: RT2
        I: RMD
        J: RB1
        K: RB2
        L: MT1
        M: MT2
        N: MB1
        O: MB2
        '''
        for row in range(len(map)):
            for col in range(len(map[0])):
                if map[row][col] == "B":
                    self.leftWallGroup.add(LeftWall(24+(col-75)*24,24+(row-75)*24,"Top1"))
                elif map[row][col] == "C":
                    self.leftWallGroup.add(LeftWall(24+(col-75)*24,24+(row-75)*24,"Top2"))
                    self.floorGroup.add(Floor(24+(col-75)*24,24+(row-75)*24))
                elif map[row][col] == "D":
                    self.leftWallGroup.add(LeftWall(24+(col-75)*24,24+(row-75)*24,"Mid"))
                    self.floorGroup.add(Floor(24+(col-75)*24,24+(row-75)*24))
                elif map[row][col] == "E":
                    self.leftWallGroup.add(LeftWall(24+(col-75)*24,24+(row-75)*24,"Bot1"))
                    self.floorGroup.add(Floor(24+(col-75)*24,24+(row-75)*24))
                elif map[row][col] == "F":
                    self.leftWallGroup.add(LeftWall(24+(col-75)*24,24+(row-75)*24,"Bot2"))
                    self.floorGroup.add(Floor(24+(col-75)*24,24+(row-75)*24))
                elif map[row][col] == "G":
                    self.rightWallGroup.add(RightWall(24+(col-75)*24,24+(row-75)*24,"Top1"))
                elif map[row][col] == "H":
                    self.rightWallGroup.add(RightWall(24+(col-75)*24,24+(row-75)*24,"Top2"))
                    self.floorGroup.add(Floor(24+(col-75)*24,24+(row-75)*24))
                elif map[row][col] == "I":
                    self.rightWallGroup.add(RightWall(24+(col-75)*24,24+(row-75)*24,"Mid"))
                    self.floorGroup.add(Floor(24+(col-75)*24,24+(row-75)*24))
                elif map[row][col] == "J":
                    self.rightWallGroup.add(RightWall(24+(col-75)*24,24+(row-75)*24,"Bot1"))
                    self.floorGroup.add(Floor(24+(col-75)*24,24+(row-75)*24))
                elif map[row][col] == "K":
                    self.rightWallGroup.add(RightWall(24+(col-75)*24,24+(row-75)*24,"Bot2"))
                    self.floorGroup.add(Floor(24+(col-75)*24,24+(row-75)*24))
                elif map[row][col] == "L":
                    self.midWallTopGroup.add(MidWall(24+(col-75)*24,24+(row-75)*24,"Top1"))
                elif map[row][col] == "M":
                    self.midWallTopGroup.add(MidWall(24+(col-75)*24,24+(row-75)*24,"Top2"))
                    self.floorGroup.add(Floor(24+(col-75)*24,24+(row-75)*24))
                elif map[row][col] == "N":
                    self.midWallBotGroup.add(MidWall(24+(col-75)*24,24+(row-75)*24,"Bot1"))
                    self.floorGroup.add(Floor(24+(col-75)*24,24+(row-75)*24))
                elif map[row][col] == "O":
                    self.midWallBotGroup.add(MidWall(24+(col-75)*24,24+(row-75)*24,"Bot2"))
                    self.floorGroup.add(Floor(24+(col-75)*24,24+(row-75)*24))
                elif map[row][col] == "A":
                    self.floorGroup.add(Floor(24+(col-75)*24,24+(row-75)*24))
        ##MISC.##
        self.dirx = 1
        self.diry = 1
        self.mouseX = 0
        self.mouseY = 0
        self.mouseAngle = 0
        self.xMargin = 0
        self.yMargin = 0
        self.NTx, self.NTy = 0, 0
        pass
        ##Coins##
        self.coinsGroup = pygame.sprite.Group()
        self.coinsGroup.add(Coin(200,300))
        self.coinsTextGroup = pygame.sprite.Group()
        self.coinsTextGroup.add(textBox(200,300,"coin_text.png",36,36))
        ##Monster##
        self.monsterGroup = pygame.sprite.Group()
        self.monsterGroup.add(Monster(200,400,2))


    def mousePressed(self, x, y):
        dirx = x-self.p.x
        diry = y-self.p.y
        l = math.sqrt(dirx**2 + diry**2)
        direction = [(x-self.p.x)/l,(y-self.p.y)/l]
        self.bulletGroup.add(Bullet(self.p.x-self.xMargin,self.p.y-self.yMargin,12,direction))
        self.bulletGroup.update(self.xMargin,self.yMargin)
        pass

    def mouseReleased(self, x, y):
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
        
        if self.bulletCount%10 < 3:
            dirx = x-self.p.x
            diry = y-self.p.y
            l = math.sqrt(dirx**2 + diry**2)
            direction = [(x-self.p.x)/l,(y-self.p.y)/l]
            self.bulletGroup.add(Bullet(self.p.x-self.xMargin,self.p.y-self.yMargin,12,direction))
            self.bulletGroup.update(self.xMargin,self.yMargin)
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
        if keyCode == pygame.K_p:
            self.monsterGroup.add(Monster(200,400,2))
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
        pass

    def timerFired(self, dt):
        ##Player Position##
        self.p.imageUpdate(self.dir)
        ##Player Collision##
        if pygame.sprite.groupcollide(self.leftWallGroup,self.playerGroup,False,False) != {}:
            self.xMargin += self.p.xSpeed - 1
        if pygame.sprite.groupcollide(self.rightWallGroup,self.playerGroup,False,False) != {}:
            self.xMargin += self.p.xSpeed + 1
        if pygame.sprite.groupcollide(self.midWallTopGroup,self.playerGroup,False,False) != {}:
            self.yMargin += self.p.ySpeed - 1
        if pygame.sprite.groupcollide(self.midWallBotGroup,self.playerGroup,False,False) != {}:
            self.yMargin += self.p.ySpeed + 1
        ##Margin Update##
        self.xMargin -= self.p.xSpeed
        self.yMargin -= self.p.ySpeed
        NTx, NTy = 0.1*self.NTx, 0.1*self.NTy
        self.leftWallGroup.update(self.xMargin,self.yMargin)
        self.rightWallGroup.update(self.xMargin,self.yMargin)
        self.midWallTopGroup.update(self.xMargin,self.yMargin)
        self.midWallBotGroup.update(self.xMargin,self.yMargin)
        self.floorGroup.update(self.xMargin-NTx,self.yMargin-NTy)
        self.bulletGroup.update(self.xMargin,self.yMargin)
        self.coinsGroup.update(self.xMargin-NTx,self.yMargin-NTy)
        self.coinsTextGroup.update(self.xMargin-NTx,self.yMargin-NTy)
        self.p.x = self.p.startX - NTx
        self.p.y = self.p.startY - NTy
        self.p.getRect()
        ##Pointer##
        self.Pointer.update()
        ##Wand Rotation##
        self.wand.rotateUpdate(self.mouseX, self.mouseY, self.p.x, self.p.y)
        ##Bullet Collisions##
        pygame.sprite.groupcollide(self.leftWallGroup,self.bulletGroup,False,True)
        pygame.sprite.groupcollide(self.rightWallGroup,self.bulletGroup,False,True)
        pygame.sprite.groupcollide(self.midWallTopGroup,self.bulletGroup,False,True)
        pygame.sprite.groupcollide(self.midWallBotGroup,self.bulletGroup,False,True)
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
            if h <= 100000:
                monster.state = 1
                monster.imageUpdateMove(directionX,directionY)
            else:
                monster.state = 0
                monster.imageUpdateMove(directionX,directionY)
        for monster in pygame.sprite.groupcollide(self.monsterGroup,self.bulletGroup,False,True):
            directionX = (self.p.x - monster.x)
            directionY = (self.p.y - monster.y)
            h = math.sqrt(directionX**2 + directionY**2)
            directionX /= h
            directionY /= h
            monster.hit(directionX,directionY)
            if monster.health <= 0:
                self.monsterGroup.remove(monster)
        pass

    def redrawAll(self, screen):
        screen.fill((45,45,45))
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
        self.coinsGroup.draw(screen)
        self.monsterGroup.draw(screen)
        if self.mouseAngle < 180:
            self.wandGroup.draw(screen)
        self.playerGroup.draw(screen)
        self.PointerGroup.draw(screen)
        if self.mouseAngle > 180:
            self.wandGroup.draw(screen)
        self.coinsTextGroup.draw(screen)
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