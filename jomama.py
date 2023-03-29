import pygame
import sys
import time
import socket
import threading
import random
import math

# Define some constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TILE_SIZE = 32
NUM_TEXTURES = 7
e_NUM_TEXTURES = 1

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
oldrender=False

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
ptx = pygame.image.load("player.png").convert()
health = pygame.image.load("health.png").convert()
emptyhealth = pygame.image.load("empty.png").convert()

player_pos = [64, 64]
player_health = 10
player_size = [TILE_SIZE, TILE_SIZE]
player_speed = TILE_SIZE
etextures=[]

# Load the textures
textures = []
for i in range(NUM_TEXTURES):
    texture = pygame.image.load(f'texture{i}.png').convert()
    textures.append(texture)
for i in range(e_NUM_TEXTURES):
    etexture = pygame.image.load(f'etx{i}.png').convert()
    etextures.append(etexture)

poison=pygame.image.load("poison.png").convert()
fire=pygame.image.load("fire.png").convert()
battle=pygame.image.load("bg.png").convert()
gameover=pygame.image.load("gameover.png").convert()

# Load the map data
with open('map.dat', 'r') as f:
    map_data = [list(map(int, line.strip())) for line in f.readlines()]


jtimer=0
# Create a clock
clock = pygame.time.Clock()

#declare special tiles
solid_tiles=[1]
deadly_tiles=[2]
r_enc_tiles=[4]
enemytypes=[["giant mouse",0,5,2]]
player_dmg=3
player_armor=0
offx=0
offy=0
isOpen=False
# Main game loop
d=0
player_effects=[["fire",0],["poison",0]]
def tick():
    global player_health
    global player_effects
    global player_size
    global player_pos
    global inFight
    global escapefailed
    global enemyturn
    global enemy
    #set player collider
    player_rect = pygame.Rect((player_pos[0],player_pos[1]), player_size)
    for y, row in enumerate(map_data):
        if y*TILE_SIZE+offy<0:
            continue
        if y*TILE_SIZE+offy>480:
            break
        for x, tile in enumerate(row): #loop through every tile
            if x*TILE_SIZE+offx<0:
                continue
            if x*TILE_SIZE+offx>640:
                break
            tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile==3 and player_rect.colliderect(tile_rect):
                player_effects[0]=["fire",0]
            if tile==6 and player_rect.colliderect(tile_rect):
                player_effects[1]=["poison",player_effects[1][1]+3]            
            if tile in deadly_tiles:
                tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if player_rect.colliderect(tile_rect):
                    if tile==2:
                        player_effects[0]=["fire",player_effects[0][1]+4]
                    else:
                        player_health-=1       
            if tile in r_enc_tiles and player_rect.colliderect(tile_rect) and random.randint(1,4)==2:
                inFight=True
                escapefailed=False
                enemyturn=False
                enemy=enemytypes[e_NUM_TEXTURES-1]
    jomama=0
    for i in player_effects:
        if i[0]=="poison" and i[1]>=1:
            player_health=player_health/2
            i[1]-=1
            screen.blit(poison,(608,0))
        if i[0]=="fire" and i[1]>=1:
            player_health-=1
            i[1]-=1
            screen.blit(fire,(608,32))
        player_effects[jomama]=i
        jomama+=1
    return player_effects
def displayeffects():
    for i in player_effects:
        if i[0]=="poison" and i[1]>=1:
            screen.blit(poison,(608,0))
        if i[0]=="fire" and i[1]>=1:
            screen.blit(fire,(608,32))
def overlay():
    for i in range(10):
        if player_health>=i:
            screen.blit(health,(i*12,0))
        else:
            screen.blit(emptyhealth,(i*12,0))
    displayeffects()
inFight=False
ymod=0
font = pygame.font.Font('freesansbold.ttf', 32)
xx=[]
yy=[]
for i in range(72):
    xx.append(math.sin(i*5))
    yy.append(math.cos(i*5))
while True:
    if inFight:
        jtimer+=1
        if jtimer>=180:
            jtimer=0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                print("closed")
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handle mouse clicks
            x, y = event.pos
            if y>350:
                if x>320 and not escapefailed:
                    if random.randint(1,5)==1:
                        inFight=False
                    else:
                        escapefailed=True
                        enemyturn=True
                elif x<320:
                    enemy[2]-=player_dmg
                    enemyturn=True
            if enemyturn:
                player_health-=enemy[3]-player_armor
                ymod=40
                enemyturn=False
            time.sleep(0.5)
        if enemy[2]<=0:
            enemytypes=[["giant mouse",0,5,2]]
            inFight=False
        ymod=ymod*0.8
            
        text = font.render(str(enemy[2]), True, BLACK)
        screen.fill(BLACK)
        screen.blit(battle, (0,0))
        screen.blit(etextures[enemy[1]], (340, 100+math.sin(jtimer/4)*ymod*2))
        screen.blit(text,(340, 100+math.sin(jtimer/4)*ymod*2))
        screen.blit(ptx,(150,50+math.sin(jtimer)*ymod))
        overlay()
        # Update the screen
        pygame.display.update()
        # Limit the framerate
        clock.tick(60)
    else:
        player_rect = pygame.Rect(player_pos, player_size)
        jtimer+=1
        if jtimer>=50:
            jtimer=0
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                print("closed")
        keys = pygame.key.get_pressed()
        if jtimer%5==0:
            for i in range(1):
                if keys[pygame.K_LEFT]:
                    player_pos[0] -= player_speed
                    d=0
                elif keys[pygame.K_RIGHT]:
                    player_pos[0] += player_speed
                    d=1
                elif keys[pygame.K_UP]:
                    player_pos[1] -= player_speed
                    d=2
                elif keys[pygame.K_DOWN]:
                    player_pos[1] += player_speed
                    d=3
                
                if keys[pygame.K_a]:
                    offx-=player_speed
                elif keys[pygame.K_d]:
                    offx+=player_speed
                elif keys[pygame.K_w]:
                    offy+=player_speed
                elif keys[pygame.K_s]:
                    offy-=player_speed
                
                for y, row in enumerate(map_data):
                    tile_y = y * TILE_SIZE
                    if tile_y+offy>480:
                        break
                    if tile_y+offy<0:
                        continue
                    for x, tile in enumerate(row):
                        tile_x=x*TILE_SIZE
                        if tile_x+offx>640:
                            break
                        if tile_x+offx<0:
                            continue
                        player_rect = pygame.Rect([player_pos[0]+offx,player_pos[1]+offy], player_size)
                        if tile in solid_tiles:
                            tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                            while player_rect.colliderect(tile_rect):
                                # Undo the player movement
                                player_rect = pygame.Rect([player_pos[0]+offx,player_pos[1]+offy], player_size)
                                if not player_rect.colliderect(tile_rect):
                                        break
                                if d==0:
                                    player_pos[0] += player_speed
                                elif d==1:
                                    player_pos[0] -= player_speed
                                elif d==2:
                                    player_pos[1] += player_speed
                                elif d==3:
                                    player_pos[1] -= player_speed
                                player_rect = pygame.Rect([player_pos[0]+offx,player_pos[1]+offy], player_size)
                                if not player_rect.colliderect(tile_rect):
                                    break
            if keys[pygame.K_DOWN] or keys[pygame.K_UP] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                player_effects=tick()
    
        # Clear the screen
        screen.fill(BLACK)
        if player_health>0:
            # Draw the map
            if oldrender:
                for y, row in enumerate(map_data):
                    tile_y = y * TILE_SIZE
                    if tile_y+offy>480:
                        break
                    if tile_y+offy<0:
                        continue
                    for x, tile in enumerate(row):
                        tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        # Calculate the tile position
                        tile_x = x * TILE_SIZE + offx
                        tile_y = y * TILE_SIZE + offy
                        # Draw the tile
                        if tile < NUM_TEXTURES:
                            sxp=player_pos[0]
                            syp=player_pos[1]
                            for sus in range(36):
                                xa=xx[sus]
                                ya=yy[sus]
                                for i2 in range(10):
                                    sxp=sxp+xa
                                    syp=syp+ya
                                    vrect = pygame.Rect((sxp,syp), (2,2))
                                    pygame.draw.rect(screen, WHITE, vrect,2)
                                    #pygame.display.flip()
                                    if vrect.colliderect(tile_rect):                            
                                        texture = textures[tile]
                                        screen.blit(texture, (tile_x, tile_y))
                                        if tile in solid_tiles:
                                            break
                        if tile_x+offx>640 or tile_x+offx<0:
                            continue
            else:

                for sus in range(72):
                    xa=xx[sus]
                    ya=yy[sus]
                    sxp=player_pos[0]+offx
                    syp=player_pos[1]+offy
                    for i2 in range(100):
                        sxp=sxp+xa*2
                        syp=syp+ya*2
                        mx=int(sxp//TILE_SIZE)
                        my=int(syp//TILE_SIZE)
                        tile=map_data[my+offy//64][mx+offx//64]
                        tile_rect = pygame.Rect(sxp//TILE_SIZE,syp//TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        vrect = pygame.Rect((mx,my), (4,4))
                        pygame.draw.rect(screen, WHITE, vrect,2)
                        #pygame.display.flip()
                        if vrect.colliderect(tile_rect):                            
                            texture = textures[tile]
                            screen.blit(texture, (mx*TILE_SIZE, my*TILE_SIZE))
                            if tile in solid_tiles:
                                break
            screen.blit(ptx, [player_pos[0]+offx,player_pos[1]+offy])
            overlay()
        else:
            screen.blit(gameover,(0,0))
        # Update the screen
        pygame.display.update()
        # Limit the framerate
        clock.tick(60)
