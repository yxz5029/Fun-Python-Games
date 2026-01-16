#Yangxin Zhou (working alone)
#This is a PYGAME program, please click the screen once after click run to make
#sure you press keys for screen(not for console)
"""
1.Nested loop: under first_scene function's while loop there's forloop which was
drawing the grid of the floor
2.If statement: there's almost if statement everywhere...
3.List: under Blessings class there's a list called num_b which will sometime store
value and sometimes remove value from it(when trade with fox merchant it will remove
2 item)
"""
"""
creativity:
This programe was made to beat enemy, player can moving around by press keys on
keyboard(w up s down a left d right).Player could also have interactive with 
character in this game.
EXTRA features:
1.use PYGAME 2.movement of bullet(both player and monster) 3.boss's self auto-movements
4.blessing to store and use coins to trade 5.connections between each scene 6.using class
7.player could press key to control the character on screen and other interactives
"""
import pygame
import os
import numpy as np
import math
import random
from time import sleep
#screen init setup
os.environ['SDL_AUDIODRIVER'] = 'dsp'
pygame.init()
#class for user controlled character
class Player:
    def __init__(self):
        #set init position
        self.x = 250
        self.y = 270
        #let gun class initialize
        self.guns = Gun(self)
        #upload and fix the size of player image
        player = pygame.image.load(os.path.join("leftplayer.png"))
        player = pygame.transform.scale(player, (player.get_width()/6, player.get_height()/6))
        self.image = player
        # Create a rect with the size of the image at coords (0, 0).
        self.rect = self.image.get_rect()
        # Set the topleft coords of the rect.
        self.rect.x = self.x
        self.rect.y = self.y
        #player movement
        self.x_change = 0
        self.y_change = 0
        #varible to check if player meet merchant
        self.ifexclamation = False
        #a number to check which merchant player is meeting right now
        self.colliderect = 5
    #function for player movement check
    def update(self,traderrect,foxrect,red_manrect,scene):
        #check which scene is right now
        if scene == 1:
            self.rect.y += self.y_change
            #check if user is next to any merchant after moving
            if not self.rect.colliderect(red_manrect) and not self.rect.colliderect(traderrect) and not self.rect.colliderect(foxrect):
                #if not then player could move everywhere in the screen
                if self.y + self.y_change >= 90 and self.y + self.y_change <= 280:
                    self.y += self.y_change
                elif self.x + self.x_change >= (x-30)/2-70 and self.x + self.x_change <= (x-30)/2+50 and self.y + self.y_change >= 70 and self.y + self.y_change <= 280:
                    self.y += self.y_change
                else:
                    self.rect.y = self.y
                self.y_change = 0
            #else to check which merchant is next to player and have exclamation mark
            elif self.rect.colliderect(red_manrect):
                self.colliderect = 1
                self.rect.y = self.y
                self.y_change = 0
            elif not self.rect.colliderect(traderrect):
                self.colliderect = 3
                self.rect.y = self.y
                self.y_change = 0
            else:
                self.colliderect = 5
                self.rect.y = self.y
                self.y_change = 0
            self.rect.x += self.x_change
            #check if user is next to any merchant
            if not self.rect.colliderect(red_manrect) and not self.rect.colliderect(traderrect) and not self.rect.colliderect(foxrect):
                #if not then player could move everywhere in the screen
                if self.x + self.x_change <= 435 and self.x + self.x_change >= 0:
                    #check and swich side of player image
                    if self.x_change > 0:
                        player = pygame.image.load(os.path.join("rightplayer.png"))
                        player = pygame.transform.scale(player, (player.get_width()/6, player.get_height()/6))
                        self.image = player
                        self.ifexclamation = False
                    elif self.x_change < 0:
                        player = pygame.image.load(os.path.join("leftplayer.png"))
                        player = pygame.transform.scale(player, (player.get_width()/6, player.get_height()/6))
                        self.image = player
                        self.ifexclamation = False
                    self.x += self.x_change
                else:
                    self.rect.x = self.x
                    self.ifexclamation = False
                self.x_change = 0
            #else to check which merchant is next to player and have exclamation mark
            elif self.rect.colliderect(red_manrect):
                self.ifexclamation = True
                self.rect.x = self.x
                self.x_change = 0
                self.colliderect = 1
            elif self.rect.colliderect(foxrect):
                self.ifexclamation = True
                self.rect.x = self.x
                self.x_change = 0
                self.colliderect = 3
            else:
                self.ifexclamation = True
                self.rect.x = self.x
                self.x_change = 0
                self.colliderect = 5
        #means not scene 1 no more merchant
        else:
            #check if movement will be in screen
            if self.x + self.x_change <= 460 and self.x + self.x_change >= 0:
                #check and swich side of player image
                if self.x_change > 0:
                    player = pygame.image.load(os.path.join("rightplayer.png"))
                    player = pygame.transform.scale(player, (player.get_width()/6, player.get_height()/6))
                    self.image = player
                elif self.x_change < 0:
                    player = pygame.image.load(os.path.join("leftplayer.png"))
                    player = pygame.transform.scale(player, (player.get_width()/6, player.get_height()/6))
                    self.image = player
                self.x += self.x_change
                self.rect.x = self.x
                self.x_change = 0
            else:
                self.rect.x = self.x
            if self.y + self.y_change >= 40 and self.y + self.y_change <= 290:
                    self.y += self.y_change
                    self.rect.y = self.y
            else:
                self.rect.y = self.y
            self.y_change = 0
    #draw player on screen and also check if next to merchant
    def draw(self, display,ifright,scene):
        screen.blit(self.image, self.rect)
        self.guns.draw(screen,ifright,scene,self)
        if self.ifexclamation:
            return True
        else:
            return False
#class for trading page
class Trading_page:
    def __init__(self):
        self.total_item = ["Increase CRIT DMG by 20%","Increase CRIT Rate by 10%","Increase bullet ATK by 10%","Increase user's max HP by 20%"] 
        self.list_of_items = [[self.total_item[random.randint(0, 3)],self.total_item[random.randint(0, 3)],self.total_item[random.randint(0, 3)],self.total_item[random.randint(0, 3)],self.total_item[random.randint(0, 3)]],[self.total_item[random.randint(0,3)],self.total_item[random.randint(0,3)],self.total_item[random.randint(0,3)]],[" 30% chance to lose 30% HP"]]
        self.box_x = 90
        self.trade_t = "Use 2 random blssings from the current "
        self.box_y = 100
        self.l = 220
        self.w = 46
        self.index = 0
        self.rect = pygame.Rect(430,90,30,30)
        self.rect.x = 430
        self.rect.y = 90
        self.chance_t = "70% chance to gain a random blessing,"
        self.clicked = False
        self.empty = (150,150,150) 
        self.empty_num = (250,0,0)
        self.full_num = (0,0,0)
    #draw trading page on screen
    def draw(self,hp,player):
        index = int(((player.colliderect*-1)+5)/2)
        pygame.draw.rect(screen,(200,200,200),(30,35,460,55))
        text = f3.render("Press 'p' on keyboard to exit Press numbers on keyboard",True,"black")
        text1 = f3.render("to chose option: press 1 for option 1",True,"black")
        pygame.draw.rect(screen,(0,0,0),(70,90,390,260))
        screen.blit(text,(40,40))
        screen.blit(text1,(40,60))
        pygame.draw.rect(screen,(90,80,100),(75,95,380,250))
        #check which merchant and do corredsponding things
        if player.colliderect == 5:
            for i in range(player.colliderect):
                trade.box_y = 100+(44*i)+(5*i)
                pygame.draw.rect(screen,(240,240,240),(90,self.box_y,350,44))
                pygame.draw.line(screen, (40,40,40), (350,self.box_y), (350,self.box_y+44), 2)
                if if_empty.count(i) != 0:
                    blessing = f3.render(str(i+1)+self.list_of_items[index][i],True,self.empty)
                    cost = f2.render(str(6),True,self.empty_num)
                else:
                    blessing = f3.render(str(i+1)+self.list_of_items[index][i],True,"black")
                    cost = f2.render(str(6),True,self.full_num)
                pygame.draw.circle(screen, "orange", (350+30,self.box_y+15), 14)        
                pygame.draw.circle(screen, "yellow", (350+30,self.box_y+15), 9)
                screen.blit(cost,(350+60,self.box_y+10))
                screen.blit(blessing,(trade.box_x+5,self.box_y+5))
        elif player.colliderect == 3:
            for i in range(player.colliderect):
                self.box_y = 100+(230/3*i)+(5*i)
                pygame.draw.rect(screen,(240,240,240),(90,self.box_y,350,230/3))
                if if_empty.count(i) == 0 and len(blessings_l) >=2:
                    blessing1 = f3.render(str(i+1)+" "+self.trade_t,True,"black")
                    blessing2 = f3.render("procession to trade for: ",True,"black")
                    blessing3 = f3.render(self.list_of_items[index][i],True,"black")
                else:
                    blessing1 = f3.render(str(i+1)+" "+self.trade_t,True,self.empty)
                    blessing2 = f3.render("procession to trade for: ",True,self.empty)
                    blessing3 = f3.render(self.list_of_items[index][i],True,self.empty)
                screen.blit(blessing1,(trade.box_x+5,self.box_y+5))
                screen.blit(blessing2,(trade.box_x+15,self.box_y+25))
                screen.blit(blessing3,(trade.box_x+15,self.box_y+45))
        else:
            self.box_y = 100
            pygame.draw.rect(screen,(240,240,240),(90,self.box_y,350,230/3))
            if if_empty.count(0) == 0 and hp >= 200:
                blessing1 = f3.render("1. "+self.chance_t,True,"black")
                blessing2 = f3.render(self.list_of_items[index][0],True,"black")
            else:
                blessing1 = f3.render("1. "+self.chance_t,True,self.empty)
                blessing2 = f3.render(self.list_of_items[index][0],True,self.empty) 
            screen.blit(blessing1,(trade.box_x+5,self.box_y+5))
            screen.blit(blessing2,(trade.box_x+15,self.box_y+25))
#class for the gun in clude direction and moving with player
class Gun:
    def __init__(self,player):
        self.x = 260
        self.y = 260
        gun_i = pygame.image.load(os.path.join("leftpoisongun.png"))
        gun_i = pygame.transform.scale(gun_i, (gun_i.get_width()/6, gun_i.get_height()/7))
        self.image = gun_i
        # Create a rect with the size of the image at coords (0, 0).
        self.rect = self.image.get_rect()
        # Set the topleft coords of the rect.
        self.rect.x = player.x+15
        self.rect.y = player.y+20
    #draw the gun direction based on user or enemy moving
    def draw(self,display,ifright,scene,player):
        #upload gun image
        gun_i = pygame.image.load(os.path.join("rightpoisongun.png"))
        gun_i = pygame.transform.scale(gun_i, (gun_i.get_width()/6, gun_i.get_height()/7))
        if scene == 1:
            x_change = player.x_change
            
            y_change = player.y_change
        elif scene == 2:
            x_change = boss.x-player.x
            y_change = boss.y+122-player.y
        else:
            rect = monster.closer(player)
            x_change = rect.x - player.x
            y_change = rect.y - player.y
        extra_x = 15
        extra_y = 20
        if x_change != 0:
            #check if have to flip image(left to right)
            if x_change > 0:
                if math.degrees(math.atan(y_change/x_change)) >= 0:
                    self.rect.x = player.x+15
                    self.rect.y = player.y+20
                else:
                    self.rect.x = player.x+15
                    self.rect.y = player.y-10
                #
                gun_i = pygame.image.load(os.path.join("rightpoisongun.png"))
                gun_i = pygame.transform.scale(gun_i, (gun_i.get_width()/6, gun_i.get_height()/8))
                self.image = pygame.transform.rotate(gun_i, 360-(math.degrees(math.atan(y_change/x_change))))
                extra_y = 20
            else:
                if math.degrees(math.atan(y_change/x_change)) > 0:
                    self.rect.x = player.x-15
                    self.rect.y = player.y-10
                else:
                    self.rect.x = player.x-15
                    self.rect.y = player.y+20
                gun_i = pygame.image.load(os.path.join("leftpoisongun.png"))
                gun_i = pygame.transform.scale(gun_i, (gun_i.get_width()/6, gun_i.get_height()/8))
                self.image = pygame.transform.rotate(gun_i, 360-(math.degrees(math.atan(y_change/x_change))))
        #if player have moved
        elif player.y_change != 0:
            self.rect.x = player.x
            self.rect.y = player.y
            if ifright:
                gun_i = pygame.image.load(os.path.join("rightpoisongun.png"))
                gun_i = pygame.transform.scale(gun_i, (gun_i.get_width()/6, gun_i.get_height()/8))
                if player.y_change > 0:
                    self.image = pygame.transform.rotate(gun_i, 270)
                else:
                    self.image = pygame.transform.rotate(gun_i, 90)
            else:
                self.rect.x = player.x+40
                gun_i = pygame.image.load(os.path.join("leftpoisongun.png"))
                gun_i = pygame.transform.scale(gun_i, (gun_i.get_width()/6, gun_i.get_height()/8))
                if y_change > 0:
                    self.image = pygame.transform.rotate(gun_i, 90)
                else:
                    self.image = pygame.transform.rotate(gun_i, 270)
        screen.blit(self.image, self.rect)
#function to draw exclamation mark on screen and check if start trading page
def exclamation(ifright,player):
    mark = pygame.image.load(os.path.join("exclamation.png"))
    mark = pygame.transform.scale(mark, (mark.get_width()/8, mark.get_height()/8))
    if ifright:
        screen.blit(mark,(player.rect.x+45,player.y+5))
    else:
        screen.blit(mark,(player.rect.x-5,player.y+5))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        return True
    else:
        return False
#class to store coins and blessings
class Blessing:
    def __init__(self):
        self.coin = 25
        self.num_b = [0,0,0,0]
    def print_blessing(self,coins):
        self.coin = coins
        self.num_b[0] = blessings_l.count(trade.total_item[0])
        self.num_b[1] = blessings_l.count(trade.total_item[1])
        self.num_b[2] = blessings_l.count(trade.total_item[2])
        self.num_b[3] = blessings_l.count(trade.total_item[3])
        print("Your current gained blessings are: ")
        for i in range(4):
            print(trade.total_item[i]+" x "+str(self.num_b[i]))
#class for player shoot bullets
class Bullets:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,5,5)
        self.rect.x = self.x
        self.rect.y = self.y
    def draw(self,x_change,y_change,scene,player):
        self.rect.x += x_change
        self.rect.y += y_change
        if scene == 2:
            if self.rect.x >= 0 and self.rect.x <= x-20 and self.rect.y >= 50 and self.rect.y <= y-20 and not self.rect.colliderect(pygame.Rect(boss.x+20,boss.y+122,100,50)):
                self.x = self.rect.x
                self.y = self.rect.y
                pygame.draw.circle(screen,"yellow",(self.rect.x,self.rect.y),6)
                return False
            else:
                #check if collide enemy
                if self.rect.colliderect(pygame.Rect(boss.x+20,boss.y+122,100,50)):
                    if bless.num_b[1] > 0:
                        critr = random.randint(1,10)
                        if critr <= bless.num_b[1]:
                            bless.coin += 1
                            boss.hp -= (2+(bless.num_b[0]*0.2))*15+(15*(0.1*bless.num_b[2]))
                        else:
                            boss.hp -= 15+(15*(0.1*bless.num_b[2]))
                    else:
                        if random.randint(0,10) == 4:
                            bless.coin += 2
                        boss.hp -= 15+(15*(0.1*bless.num_b[2]))
                self.rect.x -= x_change
                self.rect.y -= y_change
                return True
        else:
            if self.rect.x >= 0 and self.rect.x <= x-20 and self.rect.y >= 50 and self.rect.y <= y-20 and not self.rect.colliderect(pygame.Rect(monster.rect1)) and not self.rect.colliderect(pygame.Rect(monster.rect2)) and not self.rect.colliderect(pygame.Rect(monster.rect3)):
                self.x = self.rect.x
                self.y = self.rect.y
                pygame.draw.circle(screen,"yellow",(self.rect.x,self.rect.y),6)
                return False
            else:
                damage = 15+(15*(0.1*bless.num_b[2]))
                if bless.num_b[1] > 0:
                    critr = random.randint(1,10)
                    if critr <= bless.num_b[1]:
                        damage = (2+(bless.num_b[0]*0.2))*15+(15*(0.1*bless.num_b[2]))
                    else:
                        damage = 15+(15*(0.1*bless.num_b[2]))
                else:
                    damage = 15+(15*(0.1*bless.num_b[2]))
                text = f2.render(str(int(damage)),True,(255,0,0))
                if monster.hp1 >= 0 and self.rect.colliderect(monster.rect1):
                    pygame.draw.circle(screen,"orange",(monster.rect1.x+20,monster.rect1.y+5),6)
                    screen.blit(text,(monster.rect1.x+20,monster.rect1.y+5))
                    if bless.num_b[1] > 0:
                        critr = random.randint(1,10)
                        if critr <= bless.num_b[1]:
                            monster.hp1 -= (2+(bless.num_b[0]*0.2))*15+(15*(0.1*bless.num_b[2]))
                        else:
                            monster.hp1 -= 15+(15*(0.1*bless.num_b[2]))
                    else:
                        if random.randint(0,10) == 4:
                            bless.coin += 2
                        monster.hp1 -= 15+(15*(0.1*bless.num_b[2]))
                elif monster.hp2 >= 0 and self.rect.colliderect(monster.rect2):
                    pygame.draw.circle(screen,"orange",(monster.rect2.x+16,monster.rect2.y+5),6)
                    screen.blit(text,(monster.rect2.x+20,monster.rect2.y+5))
                    if bless.num_b[1] > 0:
                        critr = random.randint(1,10)
                        if critr <= bless.num_b[1]:
                            bless.coin += 1
                            monster.hp2 -= (2+(bless.num_b[0]*0.2))*15+(15*(0.1*bless.num_b[2]))
                        else:
                            monster.hp2 -= 15+(15*(0.1*bless.num_b[2]))
                    else:
                        if random.randint(0,10) == 4:
                            bless.coin += 2
                        monster.hp2 -= 15+(15*(0.1*bless.num_b[2]))
                elif monster.hp3 >= 0 and self.rect.colliderect(monster.rect3):
                    pygame.draw.circle(screen,"orange",(monster.rect3.x+16,monster.rect3.y+5),6)
                    screen.blit(text,(monster.rect3.x+20,monster.rect3.y+5))
                    if bless.num_b[1] > 0:
                        critr = random.randint(1,10)
                        if critr <= bless.num_b[1]:
                            bless.coin += 1
                            monster.hp3 -= (2+(bless.num_b[0]*0.2))*15+(15*(0.1*bless.num_b[2]))
                        else:
                            monster.hp3 -= 15+(15*(0.1*bless.num_b[2]))
                    else:
                        if random.randint(0,10) == 4:
                            bless.coin += 1
                        monster.hp3 -= 15+(15*(0.1*bless.num_b[2]))
                self.rect.x -= x_change
                self.rect.y -= y_change
                return True
#class for the bosss
class Boss:
    def __init__(self):
        self.x = 180
        self.y = -60
        self.boss = pygame.image.load(os.path.join("boss_moving.png"))
        self.image = pygame.transform.scale(self.boss, (self.boss.get_width()*0.8, self.boss.get_height()*0.8))
        self.nonflip = pygame.transform.scale(self.boss, (self.boss.get_width()*0.8, self.boss.get_height()*0.8))
        self.boss_r = pygame.image.load(os.path.join("rightboss.png"))
        self.flip = pygame.transform.scale(self.boss_r, (self.boss_r.get_width()*0.8, self.boss_r.get_height()*0.8))
        self.rect = pygame.Rect(self.x+20,self.y+102,150,50)
        self.rect.x = self.x
        self.rect.y = self.y
        self.hp = mode_enemyhp[mode-1]
        self.now = self.image
    def update(self,x_move,y_move,player):
        if not player.rect.colliderect(self.rect):
            if self.x + x_move >= 20 and self.x+x_move-50 <= 450:
                if self.x+20 - player.x < 0:
                    self.image = self.flip
                else:
                    self.image = self.nonflip
                self.x += x_move
                self.rect.x = self.x
                print(str(self.y + 130+y_move))
            if self.y + 130+y_move >= 50 and self.y +y_move <= 170:
                self.y += y_move
                self.rect.y = self.y
            self.now = self.image
        else:
            boss = pygame.image.load(os.path.join("left_boss_attack.png"))
            boss = pygame.transform.scale(boss, (boss.get_width()*0.7, boss.get_height()*0.7))
            if self.x+20 - player.x > 0:
                self.image = boss
            else:
                boss = pygame.image.load(os.path.join("right_boss_attack.png"))
                boss = pygame.transform.scale(boss, (boss.get_width()*0.7, boss.get_height()*0.7))
                self.image = boss
        self.rect = pygame.Rect(self.x+20,self.y+102,150,50)
    def draw(self,screen):
        transparent = (0,0,0,0)
        screen.blit(self.image,(self.x,self.y))
        self.image = self.now
#function to draw and let user pick difficulties they want
def difficulties():
    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        welcome = f2.render("Welcome to Brave vs Moster Game",True,"black")
        difficulties = f3.render("Please pick the difficulties you want below: (press on keyboard)",True,"black")
        choice = f2.render("1 for Easy, 2 for Medium, 3 for Hard, 4 for Legend",True,"black")
        rule = f3.render("The more difficult the mode,the higher the boss's ATK and HP",True,"red")
        pygame.draw.rect(screen,(190,190,190),(20,20,x-40,y-40))
        screen.blit(welcome,(70,40))
        screen.blit(difficulties,(30,70))
        screen.blit(choice,(30,90))
        screen.blit(rule,(30,120))
        #use keys to check which mode user pick
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            return 1
        if keys[pygame.K_2]:
            return 2
        if keys[pygame.K_3]:
            return 3
        if keys[pygame.K_4]:
            return 4
        if keys[pygame.K_5]:
            return 5
        pygame.display.flip()
#class for monster's bullet move ment and hit player
class Attack:
    def __init__(self,x,y):
        clock = pygame.time.Clock()
        dt = clock.tick(50) / 1000
        self.move = int(105*dt)
        self.xpos = x
        self.xneg = x
        self.ypos = y
        #record how many bullet hit the player
        self.damage = 0
        self.yneg = y
        #creat same size rect for bullet for detect if hit anything later
        #each monster could shoot 4 bullet a time
        self.rect1 = pygame.Rect(self.xpos,self.ypos,10,10)
        self.rect2 = pygame.Rect(self.xneg,self.ypos,10,10)
        self.rect3 = pygame.Rect(self.xneg,self.yneg,10,10)
        self.rect4 = pygame.Rect(self.xpos,self.yneg,10,10)
        self.rect1.x = self.xpos
        self.rect1.y = self.ypos
        self.rect2.x = self.xneg
        self.rect2.y = self.ypos
        self.rect3.x = self.xneg
        self.rect3.y = self.xneg
        self.rect4.x = self.xpos
        self.rect4.y = self.xneg
        self.end = False
    #draw bullet on screen
    def draw(self,player):
        #recount everytime have bullet shoot to player
        self.damage = 0
        self.rect1.x += self.move
        self.rect1.y += self.move
        self.rect2.x -= self.move
        self.rect2.y += self.move
        self.rect3.x -= self.move
        self.rect3.y -= self.move
        self.rect4.x += self.move
        self.rect4.y -= self.move
        if not self.rect1.colliderect(player.rect):
            if self.rect1.x <= x-20 and self.rect1.y <= y-50:
                pygame.draw.circle(screen,(255,0,0),(self.rect1.x,self.rect1.y),5)
                self.end = False
            else:
                self.end = True
        else:
            pygame.draw.circle(screen,"orange",(self.rect1.x,self.rect1.y),5)
            self.damage += 1
            self.end = True
        if not self.rect2.colliderect(player.rect):
            if self.rect2.x >= 20 and self.rect2.y <= y-50:
                pygame.draw.circle(screen,(255,0,0),(self.rect2.x,self.rect2.y),5)
                self.end = False
            else:
                self.end = True
        else:
            pygame.draw.circle(screen,"orange",(self.rect2.x,self.rect2.y),5)
            self.damage += 1
        if not self.rect3.colliderect(player.rect):
            if self.rect3.x >= 20 and self.rect3.y >= 50:
                pygame.draw.circle(screen,(255,0,0),(self.rect3.x,self.rect3.y),5)
                self.end = False
            else:
                if self.end:
                    self.end = True
        else:
            pygame.draw.circle(screen,"orange",(self.rect3.x,self.rect3.y),5)
            self.damage += 1
            if self.end:
                self.end = True
        if not self.rect4.colliderect(player.rect):
            if self.rect4.x <= x-20 and self.rect4.y >= 50:
                pygame.draw.circle(screen,(255,0,0),(self.rect4.x,self.rect4.y),5)
                self.end = False
            else:
                if self.end:
                    self.end = True
        else:
            if self.end:
                self.end = True
            pygame.draw.circle(screen,"orange",(self.rect4.x,self.rect4.y),5)
            self.damage += 1
        return self.damage
#class for the 3 monster's movement and image and attack
class Monster:
    def __init__(self):
        #coordinates set up
        self.x1 = 100
        self.x2 = 250
        self.x3 = 400
        self.y1 = 150
        self.y2 = 150
        self.y3 = 150
        #upload image
        self.right_moster = pygame.image.load(os.path.join("right_monster.png"))
        self.right_moster = pygame.transform.scale(self.right_moster,(self.right_moster.get_width()/7,self.right_moster.get_height()/7))
        self.left_moster = pygame.image.load(os.path.join("left_monster.png"))
        self.left_moster = pygame.transform.scale(self.left_moster,(self.left_moster.get_width()/7,self.left_moster.get_height()/7))
        self.dead = pygame.image.load(os.path.join("dead_monster.png"))
        self.dead = pygame.transform.scale(self.dead,(self.dead.get_width()/8,self.dead.get_height()/8))
        self.image1 = self.right_moster
        self.image2 = self.right_moster
        self.image3 = self.right_moster
        self.rect1 = self.image1.get_rect()
        self.rect2 = self.image2.get_rect()
        self.rect3 = self.image3.get_rect()
        self.rect1.x = self.x1
        self.rect1.y = self.y1
        self.rect2.x = self.x2
        self.rect2.y = self.y2
        self.rect3.x = self.x3
        self.rect3.y = self.y3
        #movements for each monster
        self.x_change1 = 0
        self.y_change1 = 0
        self.x_change2 = 0
        self.y_change2 = 0
        self.x_change3 = 0
        self.y_change3 = 0
        #hp for each monster
        self.hp1 = int(mode_enemyhp[mode-1]/3)
        self.hp2 = int(mode_enemyhp[mode-1]/3)
        self.hp3 = int(mode_enemyhp[mode-1]/3)
        self.attack = [0,0,0]
        #make attack class callable everywhere
        self.shoot1 = Attack(self.x1,self.y1)
        self.shoot2 = Attack(self.x2,self.y2)
        self.shoot3 = Attack(self.x3,self.y3)
    #function to check which non dead monster was closer to user and return that monster's rect for gun direction use
    def closer(self,player):
        diff1 = abs(player.x - self.x1)+abs(player.y - self.y1)  
        diff2 = abs(player.x - self.x2)+abs(player.y - self.y2)
        diff3 = abs(player.x - self.x3)+abs(player.y - self.y3)
        #check if that monster has dead
        if self.hp1 >= 0 and self.hp2 >= 0:
            if diff1 < diff2:
                if self.hp3 >= 0:
                    if diff1 < diff3:
                        return self.rect1
                    else:
                        return self.rect3
                else:
                    return self.rect1
            else:
                if diff2 < diff3:
                    return self.rect2
                else:
                    return self.rect3
        elif self.hp1 >= 0 and self.hp3 >= 0:
            if diff1 <= diff3:
                return self.rect1
            else:
                return self.rect3
        elif self.hp2 >= 0 and self.hp3 >= 0:
            if diff2 <= diff3:
                return self.rect2
            else:
                return self.rect3
        else:
            if self.hp1 >= 0:
                return self.rect1
            elif self.hp2 >= 0:
                return self.rect2
            else:
                return self.rect3
    #function to draw the 3 monster and calculate their movement if they aern't dead
    def draw(self,x_change,y_change,attack,player):
        num_damage = 0
        if self.x_change1 == 0:
            self.x_change1 = x_change
            self.y_change1 = y_change
            self.x_change2 = x_change
            self.y_change2 = -y_change
            self.x_change3 = -x_change
            self.y_change3 = -y_change
        #check if alive
        if self.hp1 >= 0:
            if self.attack[0] == 0:
                if attack and random.randint(1,3) != 3:
                    self.attack[0] = 1
                    self.shoot1 = Attack(self.x1,self.y1)
                    num_damage += self.shoot1.draw(player)
            else:
                num_damage += self.shoot1.draw(player)
            if self.shoot1.end:
                self.attack[0] = 0
            self.rect1.x += self.x_change1
            self.rect1.y += self.y_change1
            if not self.rect1.colliderect(player.rect):
                if self.x1 + self.x_change1 <= x-20 and self.x1 + self.x_change1 >= 20: 
                    self.x1 += self.x_change1
                else:
                    self.x_change1 *= -1
                if self.y1 + self.y_change1 <= y-40 and self.y1 + self.y_change1 >= 50:
                   self.y1 += self.y_change1
                else:
                    self.y_change1 *= -1
            else:
                self.rect1.x = self.rect1.x - (2*x_change)
                self.rect1.y = self.rect1.y - (2*y_change)
                #if not self.rect1.colliderect(player.rect):
                if self.x1 - x_change <= x-20 and self.x1 - x_change >= 20: 
                    self.x_change1 *= -1
                    self.x1 += self.x_change1
                if self.y1 - self.y_change1 <= y-40 and self.y1 - self.y_change1 >= 50:
                    self.y_change1 *= -1
                    self.y1 += self.y_change1
            self.rect1.x = self.x1
            self.rect1.y = self.y1
            #draw monster's hp
            pygame.draw.rect(screen,(0,0,0),(self.rect1.x+10,self.rect1.y-5,30,5))
            pygame.draw.rect(screen,(255,0,0),(self.rect1.x+10,self.rect1.y-5,self.hp1/int(mode_enemyhp[mode-1]/3)*30,5))
            screen.blit(self.image1,self.rect1)
        else:
            screen.blit(self.dead,(self.rect1))
        #check if still alive
        if self.hp2 >= 0:
            if self.attack[1] == 0:
                if attack and random.randint(1,3) != 3:
                    self.attack[1] = 1
                    self.shoot2 = Attack(self.x2,self.y2)
                    num_damage += self.shoot2.draw(player)
            else:
                num_damage += self.shoot2.draw(player)
            if self.shoot2.end:
                    self.attack[1] = 0
            self.rect2.x += self.x_change2
            self.rect2.y += self.y_change2
            if not self.rect2.colliderect(player.rect):
                if self.x2 + self.x_change2 <= x-20 and self.x2 + self.x_change2 >= 20: 
                    self.x2 += self.x_change2
                else:
                    self.x_change2 *= -1
                if self.y2 - self.y_change2 >= 50 and self.y2 - self.y_change2 <= y-40:
                    self.y2 -= self.y_change2
                else:
                    self.y_change2 *= -1
            
            else:
                self.rect2.x = self.rect2.x - (2*self.x_change2)
                self.rect2.y = self.rect2.y + (2*self.y_change2)
                if self.x2 - self.x_change2 >= 20 and self.x2 - self.x_change2 < x-20: 
                    self.x_change2 *= -1
                    self.x2 += self.x_change2   
            self.rect2.x = self.x2
            self.rect2.y = self.y2
            #draw monster's hp
            pygame.draw.rect(screen,(0,0,0),(self.rect2.x+10,self.rect2.y-5,30,5))
            pygame.draw.rect(screen,(255,0,0),(self.rect2.x+10,self.rect2.y-5,self.hp2/int(mode_enemyhp[mode-1]/3)*30,5))
            screen.blit(self.image2,self.rect2)
        else:
            screen.blit(self.dead,(self.rect2))
        #check if still alive
        if self.hp3 >= 0:
            if self.attack[2] == 0:
                if attack and random.randint(1,3) != 3:
                    self.attack[2] = 1
                    self.shoot3 = Attack(self.x3,self.y3)
                    num_damage += self.shoot2.draw(player)
            else:
                num_damage += self.shoot3.draw(player)
            if self.shoot3.end:
                    self.attack[2] = 0
            self.rect3.x += self.x_change3
            self.rect3.y += self.y_change3
            if not self.rect3.colliderect(player.rect):
                if self.x3 + self.x_change3 >= 20 and self.x3 + self.x_change3 < x-20: 
                    self.x3 += self.x_change3
                else:
                    self.x_change3 *= -1
                if self.y3 + self.y_change3 >= 50 and self.y3 + self.y_change3 < y-40:
                    self.y3 += self.y_change3
                else:
                    self.y_change3 *= -1
            else:
                self.rect3.x = self.rect3.x - (2*self.x_change3)
                self.rect3.y = self.rect3.y - (2*self.y_change3)
                if self.x3 - self.x_change3 <= x-20 and self.x3 - self.x_change3 >= 20: 
                    self.x3 -= self.x_change3
                    self.x_change3 *= -1
            self.rect3.x = self.x3
            self.rect3.y = self.y3
            #draw monster's hp
            pygame.draw.rect(screen,(0,0,0),(self.rect3.x+10,self.rect3.y-5,30,5))
            pygame.draw.rect(screen,(255,0,0),(self.rect3.x+10,self.rect3.y-5,self.hp3/int(mode_enemyhp[mode-1]/3)*30,5))
            screen.blit(self.image3,self.rect3)
        else:
            screen.blit(self.dead,(self.rect3))
        #return how many bullets has hit player
        return num_damage
#function for instruction page at the beginning(page 1)
def instruction1():
    instruction = pygame.image.load(os.path.join("text1.png"))
    instruction = pygame.transform.scale(instruction, (instruction.get_width(), instruction.get_height()/1.35))
    pygame.draw.rect(screen,(200,200,200),(0,0,x,y))
    screen.blit(instruction,(0,0))
#function for instruction page at the beginning(page 2)
def instruction2():
    instruction = pygame.image.load(os.path.join("text2.png"))
    instruction = pygame.transform.scale(instruction, (instruction.get_width(), instruction.get_height()/1.25))
    pygame.draw.rect(screen,(200,200,200),(0,0,x,y))
    screen.blit(instruction,(0,0))
#function for draw second and third scene
def second_scene(coins,hps,scene):
    clock = pygame.time.Clock()
    dt = clock.tick(50) / 1000
    #player movement
    move = int(305*dt)
    #boss movement
    b_move = int(100*dt)
    #bullet speed
    bullet_speed = int(1500*dt)
    finished = False
    #player side(left/right)
    right = False
    player = Player()
    #record which bullet is on screen
    num_bullet = [0,0,0,0]
    #movement for different bullets(max 4 bullets shoot by user on screen total)
    bullet_m = [[0,0],[0,0],[0,0],[0,0]]
    bullet1 = Bullets(player.x,player.y)
    bullet2 = Bullets(player.x,player.y)
    bullet3 = Bullets(player.x,player.y)
    bullet4 = Bullets(player.x,player.y)
    #varible check if bullets hit something and are over
    end1 = False
    monster.hp1 = int(mode_enemyhp[mode-1]/3)
    monster.hp2 = int(mode_enemyhp[mode-1]/3)
    monster.hp3 = int(mode_enemyhp[mode-1]/3)
    boss.hp = mode_enemyhp[mode-1]
    end2 = False
    end3 = False
    end4 = False
    enemy_x = 0
    hp = hps
    ememy_y = 0
    #check if monster showld shoot bullet to attack player
    attack = 0
    #state what is the next scene to jump to after respite room 2 means boss 3 means monster
    jump_to = 2
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        keys = pygame.key.get_pressed()
        #check if anyone has dead
        if boss.hp <= 0 or hp <= 0 or monster.hp1+monster.hp2+monster.hp3 <= 0:
            #if boss dead, player could chose to restart the game for free
            if boss.hp <= 0:
                pygame.draw.rect(screen,(200,200,200),(50,60,450,200))
                congrats = f3.render("Congrats! You Win! If you want to keep the blessing",True,"black")
                rule = f3.render(" and replay again, please press return on keyboard",True,"black")
                screen.blit(congrats,(60,90))
                screen.blit(rule,(60,120))
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    jump_to = 3
                    break
            #if user dead then 100 coins is required to restart the game
            elif hp <= 0:
                pygame.draw.rect(screen,(200,200,200),(50,60,450,200))
                if bless.coin >= 100:
                    sorry = f3.render("Sorry! You Lose! If you want to spend 100 coins to keep the",True,"black")
                    rule = f3.render("blessing and replay again, please press return on keyboard",True,"black")
                    screen.blit(sorry,(60,90))
                    screen.blit(rule,(60,120))
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_RETURN]:
                        bless.coin -= 100
                        jump_to = 3
                        break
                else:
                    sorry = f3.render("Sorry You Lose! And you don't have enough coins to restart(100)",True,"black")
                    screen.blit(sorry,(30,90))
            #if three monster all dead then break the loop and go back to respit room
            elif monster.hp1+monster.hp2+monster.hp3 <= 0:
                break
        else:
            #print coins and player hp on screen
            numcoin = f2.render(str(bless.coin),True,"black")
            pygame.draw.rect(screen, gray, (0, 0, x, y))
            pygame.draw.circle(screen, "orange", (40,15), 14)        
            pygame.draw.circle(screen, "yellow", (40,15), 9)
            screen.blit(numcoin,(65,7))
            #draw background
            pygame.draw.rect(screen,(120,120,120),(0,30,x,y-30))
            pygame.draw.line(screen,(0,0,0),(0,30),(x,30),1)
            pygame.draw.rect(screen,(60,60,60),(0,30,20,y-30))
            pygame.draw.rect(screen,(30,30,30),(0,30,x,20))
            pygame.draw.rect(screen,(60,60,60),(x-20,30,20,y-30))
            pygame.draw.rect(screen,(30,30,30),(0,y-20,x,20))
            pygame.draw.line(screen,(40,90,255),(10,40),(x-10,40),3)
            pygame.draw.line(screen,(40,90,255),(10,40),(10,y-10),3)
            pygame.draw.line(screen,(40,90,255),(x-10,40),(x-10,y-10),3)
            pygame.draw.line(screen,(40,40,255),(10,y-10),(x-10,y-10),3)
            #draw grid for the floor
            for i in range(9):
                    pygame.draw.line(screen, (30,240,250), (20,50+(i*40)), (x-20,50+(i*40)), 1)
                    pygame.draw.line(screen, (200,200,200), (20,51+(i*40)), (x-20,51+(i*40)), 1)
            for i in range(9):
                pygame.draw.line(screen, (30,240,250), (20+(i*(500/8)),50), (20+(i*(500/8)),370), 1)
                pygame.draw.line(screen, (200,200,200), (22+(i*(500/8)),50), (22+(i*(500/8)),370), 1)
            #gun's direction movement's x and y will equal to boss's x y movement if it is 2 scene
            if scene == 2:
                enemy_x = boss.x
                enemy_y = boss.y+122
            #else equals to closest monster's x y movement
            else:
                enemy_rect = monster.closer(player)
                enemy_x = enemy_rect.x
                enemy_y = enemy_rect.y   
            #detecte which key user press to control player/gun shooting
            player.draw(screen,right,3)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player.y_change = -move
            if keys[pygame.K_s]:
                player.y_change = move
            if keys[pygame.K_d]:
                player.x_change = move
                right = True
            if keys[pygame.K_a]:
                right = False
                player.x_change = -move
            if keys[pygame.K_j]:
                x_direction = 40
                y_direction = 60
                #for gun direction calculate
                if enemy_x -player.x < 0:
                    x_direction = 30
                    if enemy_y-player.y < 0:
                        y_direction = 40
                else:
                    if enemy_y-player.y < 0:
                        y_direction = 60
                #check if bullets is moving or is finished and ready for next shoot
                if num_bullet[0] == 0:
                    bullet1 = Bullets(player.x+x_direction,player.y+y_direction)
                    bullet_m[0][0] = (enemy_x-player.x)/bullet_speed
                    bullet_m[0][1] = (enemy_x+122-player.y)/bullet_speed
                    num_bullet[0] = 1
                else:
                    if num_bullet[1] == 0:
                        bullet2 = Bullets(player.x+x_direction,player.y+y_direction)
                        bullet_m[1][0] = (enemy_x-player.x)/bullet_speed
                        bullet_m[1][1] = (enemy_y-player.y)/bullet_speed
                        num_bullet[1] = 1
                    else:
                        if num_bullet[2] == 0:
                            bullet3 = Bullets(player.x+x_direction,player.y+y_direction)
                            bullet_m[2][0] = (enemy_x-player.x)/bullet_speed
                            bullet_m[2][1] = (enemy_x-player.y)/bullet_speed
                            num_bullet[2] = 1
                        else:
                            if num_bullet[3] == 0:
                                bullet4 = Bullets(player.x+x_direction,player.y+y_direction)
                                bullet_m[3][0] = (enemy_x-player.x)/bullet_speed
                                bullet_m[3][1] = (enemy_y-player.y)/bullet_speed
                                num_bullet[3] = 1
                print(num_bullet[0])
            #draw boss hp if scene equals to 2
            if scene == 2:
                boss.draw(screen)
                pygame.draw.rect(screen,(0,0,0),(190,5,150,20))
                t = f3.render("Boss HP",True,"black")
                screen.blit(t,(110,8))
                pygame.draw.rect(screen,"red",(190,5,boss.hp/int(mode_enemyhp[mode-1])*150,20))
            #draw player hp
            pygame.draw.rect(screen,(0,0,0),(390,5,150,20))
            t = f3.render("HP",True,"black")
            screen.blit(t,(350,8))
            pygame.draw.rect(screen,"green",(390,5,hp/2000*150,20))
            if scene == 2:
                x_change = b_move
                y_change = b_move
                moving = random.randint(0,2)
                if abs(boss.x +30- player.x) >= 80 and abs(boss.y+122 - player.y) >= 40:
                    if boss.x +30- player.x > 0 and moving != 2:
                        x_change = x_change*-1
                    if boss.y+122 - player.y > 0 and moving != 2:
                        y_change = y_change*-1
                elif abs(boss.x +30- player.x) >= 80:
                    if boss.x - player.x > 0 and moving!= 2:
                        x_change = x_change*-1
                    y_change = y_change*-1
                elif abs(boss.y+122 - player.y) >= 40:
                    if boss.y+122 - player.y > 0 and moving != 2:
                        y_change = y_change*-1
                    x_change = x_change*-1
                else:
                    if 300-boss.y+122 >= 150:
                        y_change = -2*y_change
                    else:
                        y_change = 2*y_change
                    if 500 - boss.x-26 < 250:
                        x_change = -2*x_change
                    else:
                        x_change = 2*x_change
                if player.rect.colliderect(boss.rect):
                    hp -= mode_damage[mode-1]
                boss.update(x_change,y_change,player)
            else:
                y_change = b_move
                x_change = b_move
                attack += 100
                if attack >= 10000:
                    attack = 0                
                    hp = hp-(int(mode_damage[mode-1]/2)*monster.draw(x_change,y_change,True,player))
                else:
                    hp = hp-(int(mode_damage[mode-1]/2)*monster.draw(x_change,y_change,False,player))
            if num_bullet[0] != 0:
                end1 = bullet1.draw(bullet_m[0][0],bullet_m[0][1],scene,player)
                if end1 == True:
                    num_bullet[0] = 0
                    bullet_m[0][0] = 0
                    bullet_m[0][1] = 0
            if num_bullet[1] != 0:
                end2 = bullet2.draw(bullet_m[1][0],bullet_m[1][1],scene,player)
                if end1 == True:
                    num_bullet[1] = 0
                    bullet_m[1][0] = 0
                    bullet_m[1][1] = 0
            if num_bullet[2] != 0:
                end3 = bullet3.draw(bullet_m[2][0],bullet_m[2][1],scene,player)
                if end1 == True:
                    num_bullet[2] = 0
                    bullet_m[2][0] = 0
                    bullet_m[2][1] = 0
            if num_bullet[3] != 0:
                end4 = bullet4.draw(bullet_m[3][0],bullet_m[3][1],scene,player)
                if end1 == True:
                    num_bullet[3] = 0
                    bullet_m[3][0] = 0
                    bullet_m[3][1] = 0
            player.update(traderrect,foxrect,red_manrect,2)
        pygame.display.flip()
    first_scene(bless.coin,jump_to)
#function to draw the first scene           
def first_scene(coin,scene):
    coins = coin
    clock = pygame.time.Clock()
    dt = clock.tick(50) / 1000
    #user movement
    move = int(235*dt)
    finished = False
    right = False
    ifexclamation = False
    p_enter = False
    index = 0
    player = Player()
    player.x = 250
    player.y = 270
    #record if entering trading page
    ifprint = True
    hp = 2000*(1+(bless.num_b[3]*0.2))
    fhp = hp
    #if entering instruction page
    iftrade = False
    guns = Gun(player)
    if scene == 2:
        iftrade = True
    page = 1
    #border = pygame.Rect()
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_i]:
            #will enter instruction page later
            iftrade = False
            ifprint = False
            print(page)
        #means will enter instruction page
        if not iftrade:
            if page == 1:
                instruction1()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_2]:
                    page = 2
            elif page == 2:
                instruction2()
                #press enter key to exit
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    iftrade = True
                    ifprint = True
                elif keys[pygame.K_1]:
                    page = 1
        else:
            page = 1
            if coins < 6:
                trade.full_num = (250,0,0)
            #if player is next to a merchant
            if ifexclamation:
                #check if user want to press enter keys to enter trading page
                if not p_enter:
                    ifprint = True
                else:
                    ifprint = False
                    #check if player want to exit trading page
                    keys = pygame.key.get_pressed()
                    if not keys[pygame.K_p]:
                        trade.draw(hp,player)
                        index = int(((player.colliderect*-1)+5)/2)
                        keys = pygame.key.get_pressed()
                        #check which merchant is trading with player right now and also start collecting blessings
                        #also detect if user press key to buy anything
                        if player.colliderect == 5:
                            if keys[pygame.K_4] and if_empty.count(3) == 0:
                                if coins - 6 >= 0:
                                    blessings_l.append(trade.list_of_items[index][3])
                                    if_empty.append(3)
                                    bless.print_blessing(coins)
                                    coins -= 6
                                else:
                                    full_num = (250,0,0)
                            if keys[pygame.K_5] and if_empty.count(4) == 0:
                                if coins - 6 >= 0:
                                    blessings_l.append(trade.list_of_items[index][4])
                                    if_empty.append(4)
                                    bless.print_blessing(coins)
                                    coins -= 6
                                else:
                                    trade.full_num = (250,0,0)
                        if player.colliderect >= 3:
                            if keys[pygame.K_2] and if_empty.count(1) == 0:
                                if player.colliderect == 5:
                                    if coins - 6 >= 0:
                                        coins -= 6
                                        blessings_l.append(trade.list_of_items[index][1])
                                        bless.print_blessing(coins)
                                        if_empty.append(1)
                                    else:
                                        trade.full_num = (250,0,0)
                                else:
                                    #remove blessing based on rules
                                    if len(blessings_l) >= 2:
                                        if_empty.append(1)
                                        blessings_l.remove(blessings_l[0])
                                        blessings_l.remove(blessings_l[0])
                                        blessings_l.append(trade.list_of_items[index][1])
                                        bless.print_blessing(coins)
                                    else:
                                        print("You don't have enough blessings to trade.")
                            if keys[pygame.K_3] and if_empty.count(2) == 0:
                                if player.colliderect == 5:
                                    if coins - 6 >= 0:
                                        if_empty.append(2)
                                        coins -= 6
                                        blessings_l.append(trade.list_of_items[index][2])
                                        bless.print_blessing(coins)
                                    else:
                                        trade.full_num = (250,0,0)
                                else:
                                    if len(blessings_l) >= 2:
                                        if_empty.append(2)
                                        blessings_l.remove(blessings_l[0])
                                        blessings_l.remove(blessings_l[0])
                                        blessings_l.append(trade.list_of_items[index][2])
                                        bless.print_blessing(coins)
                                    else:
                                        print("You don't have enough blessings to trade.")
                        if keys[pygame.K_1] and if_empty.count(0) == 0:
                            if player.colliderect == 5:
                                if coins - 6 >= 0:
                                    coins -= 6
                                    blessings_l.append(trade.list_of_items[trade.index][0])
                                    bless.print_blessing(coins)
                                    if_empty.append(0)
                                else:
                                    trade.full_num = (250,0,0)
                            elif player.colliderect == 3:
                                if len(blessings_l) >= 2:
                                    blessings_l.remove(blessings_l[0])
                                    blessings_l.remove(blessings_l[0])
                                    blessings_l.append(trade.list_of_items[trade.index][0])
                                    bless.print_blessing(coins)
                                    if_empty.append(0)
                                else:
                                    print("You don't have enough blessings to trade.")
                            elif hp >= 200:
                                chance = random.randint(1,10)
                                if chance <= 7:
                                    blessings_l.append(trade.total_item[random.randint(0,3)])
                                    bless.print_blessing(coins)
                                    if_empty.append(0)
                                else:
                                    hp = hp*0.7    
                                    if_empty.append(0)
                                    print("Sorry you lost the bet.")
                            else:
                                print("You don't have enough hp to bet.")
                                if_empty.append(0)
                    else:
                        ifexclamation = False
                        p_enter = False
                        trade.list_of_items = [[trade.total_item[random.randint(0, 3)],trade.total_item[random.randint(0, 3)],trade.total_item[random.randint(0, 3)],trade.total_item[random.randint(0, 3)],trade.total_item[random.randint(0, 3)]],[trade.total_item[random.randint(0,3)],trade.total_item[random.randint(0,3)],trade.total_item[random.randint(0,3)]],[" 30% chance to lose 30% HP"]]
                        if_empty.clear()
                        trade.full_num = (0,0,0)
                        ifprint = True
                    #redraw coins and player's hp beased on trading result
                    pygame.draw.rect(screen, gray, (0, 0, 90, 30))
                    numcoin = f2.render(str(coins),True,"black")
                    pygame.draw.rect(screen,wallwidth,(340,7,150,20))
                    pygame.draw.rect(screen,(0,220,0),(340,7,(hp/fhp)*150,20))
                    pygame.draw.circle(screen, "orange", (40,15), 14)        
                    pygame.draw.circle(screen, "yellow", (40,15), 9)
                    screen.blit(numcoin,(65,7))
            if ifprint:
                #draw coins, player hp, background
                numcoin = f2.render(str(coins),True,"black")
                pygame.draw.rect(screen, gray, (0, 0, x, y))
                hp_t = f2.render("Mode: "+mode_name[mode-1]+"   HP      "+ str(int(hp))+"/"+str(int(fhp)),True,"black")
                pygame.draw.rect(screen,wallwidth,(340,7,150,20))
                pygame.draw.rect(screen,(0,220,0),(340,7,hp/fhp*150,20))
                screen.blit(hp_t,(150,10))
                pygame.draw.circle(screen, "orange", (40,15), 14)        
                pygame.draw.circle(screen, "yellow", (40,15), 9)
                screen.blit(numcoin,(65,7))
                pygame.draw.rect(screen, walltop, (0, 30, 30, y))
                pygame.draw.rect(screen, innerwall, (5, 35, 20, y-40))
                pygame.draw.rect(screen, walltop, (0, 30, x, 30))
                pygame.draw.rect(screen, innerwall, (5, 35, x-10, 20))
                pygame.draw.rect(screen, wallwidth, (30, 60, x-30, 10))
                pygame.draw.rect(screen, wall, (30, 70, (x-30)/2-100, 80))
                fight = f2.render("Go Fight:L2",True,"yellow")
                if scene == 3:
                    fight = f2.render("Go Fight:L1",True,"yellow")
                pygame.draw.rect(screen, (30,30,30), ((x-30)/2-70, 70, 140, 70))
                screen.blit(fight,((x-30)/2-55,110))
                pygame.draw.rect(screen, wall, ((x-30)/2+70, 70, (x-30)/2-70, 80))
                pygame.draw.rect(screen, walltop, (x-30, 60, 30, y))
                pygame.draw.rect(screen, innerwall, (x-25, 60, 20, y-40))
                pygame.draw.rect(screen, walltop, (0, 360, x, 30))
                pygame.draw.rect(screen, innerwall, (5, 365, x-10, 20))
                pygame.draw.line(screen, (240,240,240), (0,28+30), (x,28+30), 1)
                pygame.draw.line(screen, (250,250,250), (0,1+30), (x,1+30), 1)
                pygame.draw.line(screen, (0,0,0), (30,40), (450,40), 2)
                pygame.draw.line(screen, (15,15,15), (30,43+30), (x-30,43+30), 2)
                pygame.draw.line(screen, (20,20,20), (30,46+30), (x-30,46+30), 2)
                pygame.draw.line(screen, (30,30,30), (30,49+30), (x-30,49+30), 2)
                pygame.draw.line(screen, (40,40,40), (30,52+30), (x-30,52+30), 2)
                pygame.draw.line(screen, (50,50,50), (30,55+30), (x-30,55+30), 2)
                pygame.draw.line(screen, (60,60,60), (30,58+30), (x-30,58+30), 2)
                pygame.draw.line(screen, (70,70,70), (30,61+30), (x-30,61+30), 2)
                pygame.draw.line(screen, (70,70,70), (30,64+30), (x-30,64+30), 2)
                pygame.draw.line(screen, (75,75,75), (30,67+30), (x-30,67+30), 2)
                #draw grid for the floor
                for i in range(9):
                    pygame.draw.line(screen, (0,0,0), (30,150+(i*30)), (x-30,150+(i*30)), 1)
                for i in range(17):
                    if i == 0:
                        pygame.draw.line(screen, (0,0,0), (30,60), (30,360), 1) 
                    elif i == 16:
                        pygame.draw.line(screen, (0,0,0), (30+(i*30),60), (30+(i*30),360), 1) 
                    else:
                        pygame.draw.line(screen, (0,0,0), (30+(i*30),150), (30+(i*30),360), 1)
                #player movement
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    player.y_change = -move
                if keys[pygame.K_s]:
                    player.y_change = move
                if keys[pygame.K_d]:
                    player.x_change = move
                    right = True
                if keys[pygame.K_a]:
                    right = False
                    player.x_change = -move
                #build 3 merchant on screen
                screen.blit(scaled_image1,(20,120))
                screen.blit(scaled_image2,(430,110))
                screen.blit(scaled_image3,(445,250))
                #print instructions on screen
                instr = f2.render("Press 'i' key to check the rule again",True,"black")
                screen.blit(instr,(100,170))
                instr = f2.render("You can only check instruction in this room",True,"black")
                screen.blit(instr,(80,200))
                #check if player is next to a merchant after moving
                if not ifexclamation:
                    ifexclamation = player.draw(screen,right,1)
                else:
                    ifexclamation = player.draw(screen,right,1)
                    p_enter = exclamation(right,player)
                player.update(traderrect,foxrect,red_manrect,1)
            #ajust player hp after gain hp blessing
            if hp == fhp:
                fhp = 2000*(1+(bless.num_b[3]*0.2)) 
                hp = fhp
            else:
                ratio = hp/fhp
                fhp = 2000*(1+(bless.num_b[3]*0.2))
                hp = (fhp*ratio)
            #check if user go into the door for fight
            if player.y < 90:
                finished = True
        pygame.display.flip()
    second_scene(coins,hp,scene)
#screen size
x = 540
y = 390
size = (x, y)
#color setup
gray = (200, 200, 200)
innerwall = (30,30,30)
wallwidth = (100,100,70)
walltop = (80,80,80)
wall = (80,80,80)
screen = pygame.display.set_mode(size)
front_sprites = pygame.sprite.Group()
color = (225, 225, 225)
screen.fill(color)
#enemy's setup for different mode
mode_damage = [4,8,16,32]
mode_enemyhp = [5000,7000,8000,9000]
finished = False
#text's size and style
f2 = pygame.font.Font('freesansbold.ttf', 20)
f3 = pygame.font.Font('freesansbold.ttf', 16)
mode = 0
#pick difficulties for fight
mode += difficulties()
trader = pygame.image.load(os.path.join("pngegg.png"))
fox = pygame.image.load(os.path.join("fox.png"))
red_man = pygame.image.load(os.path.join("red_man.png"))
mode_name = ["Easy","Medium","Hard","Legend"]
blessings_l = []
if_empty = []
#initialize each class for later use
bless = Blessing()
boss = Boss()
monster = Monster()
#merchants' image and size adjust
trade = Trading_page()
scaled_image1 = pygame.transform.scale(trader, (trader.get_width()/10, trader.get_height()/10))
traderrect = scaled_image1.get_rect()
traderrect.x = -25
traderrect.y = 105
scaled_image2 = pygame.transform.scale(fox, (fox.get_width()/11, fox.get_height()/11))
foxrect = scaled_image2.get_rect()
foxrect.x = 460
foxrect.y = 70
scaled_image3 = pygame.transform.scale(red_man, (red_man.get_width()/13, red_man.get_height()/13))
red_manrect = scaled_image3.get_rect()
red_manrect.x = 460
red_manrect.y = 270
#call first scene at here and given the scene 3 as the scene to jump next
first_scene(25,3)