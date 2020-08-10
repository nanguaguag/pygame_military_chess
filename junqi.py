# -*- coding: utf-8 -*- 
# Time : 2019/1/29 21:39 
# Author : ***
import pygame,random
from pygame.locals import *
from sys import exit

pygame.init()
SCREEN_SIZE = (540,1080)#3*3*3*2*2*2*2*5
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

font = pygame.font.Font("HanYiYanKaiW-2.ttf", 30)
font_height = font.get_linesize()
move=False
compare=False
red_turn=True
select_block=None
clock=pygame.time.Clock()


listfast=[(0,1),(1,1),(2,1),(3,1),(4,1),(0,2),(4,2),(0,3),(4,3),(0,4),(4,4),(0,5),(1,5),(2,5),(3,5),(4,5),
    (0,6),(1,6),(2,6),(3,6),(4,6),(0,7),(4,7),(0,8),(4,8),(0,9),(4,9),(0,10),(1,10),(2,10),(3,10),(4,10)]

list_qi=['军旗1', '司令1','军长1','师长1','师长1', '旅长1', '旅长1', '团长1', '团长1', 
    '营长1', '营长1', '连长1', '连长1', '连长1', '工兵1', '工兵1', '工兵1', '排长1', 
    '排长1', '排长1', '地雷1', '地雷1', '地雷1', '炸弹1', '炸弹1', '军旗0', '司令0',
    '军长0','师长0', '师长0', '旅长0', '旅长0', '团长0', '团长0', '营长0', '营长0',
    '连长0', '连长0', '连长0', '工兵0', '工兵0', '工兵0', '排长0', '排长0', '排长0',
    '地雷0', '地雷0', '地雷0', '炸弹0', '炸弹0']


list_circle=[(1,2),(3,2),(2,3),(1,4),(3,4),(1,7),(3,7),(2,8),(1,9),(3,9)]


list_block=[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10),
    (0, 11), (1, 0), (1, 1), (1, 3), (1, 5), (1, 6), (1, 8), (1, 10), (1, 11), (2, 0), (2, 1), (2, 2),
    (2, 4), (2, 5), (2, 6), (2, 7), (2, 9), (2, 10), (2, 11), (3, 0), (3, 1), (3, 3), (3, 5), (3, 6),
    (3, 8), (3, 10), (3, 11), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8),
    (4, 9), (4, 10), (4, 11)]

dAttackNumber={'司令':8, '军长':7, '师长':6, '旅长':5, '团长':4, '营长':3,
    '连长':2, '排长':1, '工兵':0, '地雷':9, '炸弹':10, '军旗': 9}

def toPygame(x,y,is_circle):
    if is_circle:
        pygame_x=120*x+30
        pygame_y=90*y+30
    else:
        pygame_x=(2*x)*60
        pygame_y=(3*y)*30
    return (pygame_x,pygame_y)


def fastGoWhere(pos,x,y,color,is_gb,times):
    try:
        if is_gb and times<40:
            for a,b in [(-1,0),(0,1),(0,-1),(1,0)]:
                if (a,b)!=(-x,-y):
                    nextPos=(pos[0]+a,pos[1]+b)
                    nextQi=d[nextPos]
                    if nextPos in listfast:
                        if nextQi==[]:
                            pygame.draw.circle(screen, (0,255,0),
                                toPygame(*nextPos,True), 15, 0)
                            fastGoWhere(nextPos,a,b,color,True,times+1)
                        elif (not nextQi[2]) or (nextQi[0]!=color):
                            pygame.draw.circle(screen, (255,0,0),
                                toPygame(*nextPos,True), 15, 0)
        elif times<40:
            nextPos=(pos[0]+x,pos[1]+y)
            nextQi=d[nextPos]
            if nextPos in listfast:
                if nextQi==[]:
                    pygame.draw.circle(screen, (0,255,0),
                        toPygame(*nextPos,True), 15, 0)
                    fastGoWhere(nextPos,x,y,color,False,times+1)
                elif (not nextQi[2]) or (nextQi[0]!=color):
                    pygame.draw.circle(screen, (255,0,0),
                        toPygame(*nextPos,True), 15, 0)
    except KeyError:
        pass
# 我的理想是：
#            ╔╦╗
#，，，一亩薄 ╠╬╣，一间草屋，一杯粗茶，一亿存款
#            ╚╩╝
def whereToGo(pos):
    if pos!=None:
        pygame_pos=toPygame(*pos,True)
        for x in [-1,0,1]:
            for y in [-1,0,1]:
                try:
                    if screen.get_at((pygame_pos[0]+x*44,pygame_pos[1]+y*33))==(0,0,255):
                        nearbyPos=(pos[0]+x,pos[1]+y)
                        nearbyQi=d[nearbyPos]
                        qi=d[pos]
                        if nearbyQi==[]:
                            if nearbyPos in listfast and pos in listfast:
                                fastGoWhere(nearbyPos,x,y,qi[0],qi[1]=='工兵',1)
                            pygame.draw.circle(screen, (0,255,0),
                                (pygame_pos[0]+120*x,pygame_pos[1]+90*y), 15, 0)
                        elif (not nearbyQi[2] or nearbyQi[0]!=qi[0]) and (nearbyPos not in list_circle):
                            pygame.draw.circle(screen, (255,0,0),
                                (pygame_pos[0]+120*x,pygame_pos[1]+90*y), 15, 0)
                except IndexError:
                    pass

def drawBlock():
    for x in range(5):
        for y in range(12):
            qi=d[(x,y)]
            if qi==[]:
                pass
            elif qi[2]:
                pygame.draw.rect(screen, (255,255,255), Rect(toPygame(x,y,False),(60,60)),0)
                screen.blit(font.render(qi[1], True, (255,255*int(qi[0]),0)), toPygame(x,y,False))
            else:
                pygame.draw.rect(screen, (0,0,0), Rect(toPygame(x,y,False),(60,60)),0)


def line(pos1,pos2):
    pygame.draw.line(screen,(0,0,255),pos1,pos2,2)

def drawAll():
    screen.fill((127,127,127))
    for x in range(5):
        for y in range(12):
            if (x,y) in list_circle:
                pos=toPygame(x,y,True)
                pygame.draw.circle(screen,(0,0,255),pos,30,2)
            else:
                pos=toPygame(x,y,False)
                pygame.draw.rect(screen, (90,0,255), Rect(pos,(60,60)),2)
    for a in range(12):
        pygame.draw.line(screen,(0,0,255),(30,30+90*a),(510,30+90*a),2)
    for b in range(5):
        if b==1 or b==3:
            line((30+b*120,30),(30+b*120,480))
            line((30+b*120,570),(30+b*120,1020))
        else:
            line((30+b*120,30),(30+b*120,1020))
    line((30,120),(510,480))
    line((510,120),(30,480))
    line((30,570),(510,930))
    line((510,570),(30,930))
    pygame.draw.lines(screen,(0,0,255),True,[(270,120),(30,300),(270,480),(510,300)],2)
    pygame.draw.lines(screen,(0,0,255),True,[(270,570),(30,750),(270,930),(510,750)],2)

def select():
    pygame.draw.rect(screen, (255,255*int(d[select_block][0]),0), 
        Rect(toPygame(*select_block,False),(60,60)),5)

def change():
    global red_turn
    if red_turn:
        red_turn=False
        pygame.display.set_caption("黄方走棋")
    else:
        red_turn=True
        pygame.display.set_caption("红方走棋")

def moveqi():
    global move,select_block,pos1,pos2,text,color,step_x,step_y
    move=True
    pos1=toPygame(*select_block,False)
    pos2=toPygame(*a,False)
    text=d[select_block][1]
    color=int(d[select_block][0])
    step_x=(pos2[0]-pos1[0])/50 
    step_y=(pos2[1]-pos1[1])/50
    d[select_block]=[]
    select_block=None
    change()

def isbigger(chiqiText,beichiqiText):
    chiqiNumber=dAttackNumber[chiqiText]
    beichiqiNumber=dAttackNumber[beichiqiText]
    if chiqiText=='工兵' and (beichiqiText=='地雷' or beichiqiText=='军旗'):
        return 1
    if chiqiText=='炸弹' or beichiqiText=='炸弹' or chiqiNumber==beichiqiNumber:
        return 0
    if chiqiNumber>beichiqiNumber:
        return 1
    if chiqiNumber<beichiqiNumber:
        return -1

def eatqi(text):
    global compare,beichiqiText
    moveqi()
    compare=True
    beichiqiText=text


# ----------------------init-------------------------

d={}
for x in range(-1,5):
    for y in range(12):
        a=(x,y)
        if a in list_block:
            i=random.randint(0,len(list_qi)-1)
            d[a]=[list_qi[i][-1],list_qi.pop(i)[0:2],0]
        else:
            d[a]=[]

pygame.display.set_caption("红方走棋")
# print(d)
drawAll()
drawBlock()
# -------------------end====init---------------------

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            a=(pos[0]//120,pos[1]//90)
            qi=d[a]
            drawAll()
            if qi==[]:
                if select_block!=None:
                    drawBlock()
                    whereToGo(select_block)
                    if screen.get_at(pos)==(0,255,0):
                        select()
                        moveqi()
                    elif screen.get_at(pos)==(255,0,0):
                        select()
                        eatqi(qi[1])
                    else:
                        select_block=None
                        drawAll()
            elif qi[2]:
                if select_block==None:#无选中棋
                    if ((red_turn and qi[0]=="0") or ((not red_turn) and qi[0]=="1")) \
                        and qi[1]!="地雷" and qi[1]!="军旗":
                        select_block=a
                        select()
                else:#有选中棋
                    drawBlock()
                    whereToGo(select_block)
                    if ((qi[0]=="0" and red_turn) or (qi[0]!="0" and not red_turn)) \
                        and qi[1]!="地雷" and qi[1]!="军旗":
                        select_block=a#切换选中的棋
                        select()
                        drawAll()
                        select()
                    elif screen.get_at(pos)==(255,0,0):
                        select()
                        eatqi(qi[1])#吃棋
                    elif screen.get_at(pos)==(0,255,0):
                        select()
                        moveqi()
                    else:
                        select_block=None
                        drawAll()
            elif select_block==None:
                qi[2]=1
                select_block=None
                change()
            else:
                whereToGo(select_block)
                if screen.get_at(pos)==(255,0,0):
                    qi[2]=1
                    if qi[0]==d[select_block][0]:
                        change()
                        select_block=None
                        drawAll()
                    else:
                        select()
                        eatqi(qi[1])#吃棋
                else:
                    select_block=None
                    drawAll()
            drawBlock()
            whereToGo(select_block)
            if red_turn:
                screen.blit(font.render("红方", True, (255,0,0)), (240,1050))
            else:
                screen.blit(font.render("黄方", True, (255,255,0)), (240,1050))

    if move:
        drawAll()
        drawBlock()
        pos1=(pos1[0]+step_x,pos1[1]+step_y)
        pygame.draw.rect(screen, (255,255,255), Rect(pos1,(60,60)),0)
        screen.blit(font.render(text, True, (255,255*color,0)), pos1)
        if abs(float(pos1[0]-pos2[0]))<=abs(step_x) and abs(float(pos1[1]-pos2[1]))<=abs(step_y):
            move=False
            if compare:
                if isbigger(text,beichiqiText)>0:
                    d[a]=[str(color),text,1]
                elif isbigger(text,beichiqiText)==0:
                    d[a]=[]
                elif isbigger(text,beichiqiText)<0:
                    pass
                compare=False
            else:
                d[a]=[str(color),text,1]
            drawAll()
            drawBlock()
    pygame.display.update()
    # clock.tick(20)
