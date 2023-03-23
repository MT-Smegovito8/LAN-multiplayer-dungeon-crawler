import pygame
import sys
import time
import socket
import threading
import random

# Define some constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TILE_SIZE = 32
NUM_TEXTURES = 5

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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

# Load the textures
textures = []
for i in range(NUM_TEXTURES):
    texture = pygame.image.load(f'texture{i}.png').convert()
    textures.append(texture)
poison=pygame.image.load("poison.png").convert()
fire=pygame.image.load("fire.png").convert()
battle=pygame.image.load("bg.png").convert()

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
    #set player collider
    player_rect = pygame.Rect((player_pos[0],player_pos[1]), player_size)
    for y, row in enumerate(map_data): 
        for x, tile in enumerate(row): #loop through every tile
            tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile==3 and player_rect.colliderect(tile_rect):
                player_effects[0]=["fire",0]
            if tile in deadly_tiles:
                tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if player_rect.colliderect(tile_rect):
                    if tile==2:
                        player_effects[0]=["fire",player_effects[0][1]+4]
                    else:
                        player_health-=1       
            if tile in r_enc_tiles and player_rect.colliderect(tile_rect) and random.randint(1,4)==2:
                inFight=True
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
while True:
    if inFight:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                print("closed")
        
        screen.fill(BLACK)
        screen.blit(battle, (0,0))
        overlay()
        # Update the screen
        pygame.display.update()
        # Limit the framerate
        clock.tick(60)
    else:
        player_rect = pygame.Rect(player_pos, player_size)
        jtimer+=1
        if jtimer==50:
            jtimer=0
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                print("closed")
        keys = pygame.key.get_pressed()
        if jtimer%5==0:
            for i in range(player_speed):
                if keys[pygame.K_LEFT]:
                    player_pos[0] -= 1
                    d=0
                elif keys[pygame.K_RIGHT]:
                    player_pos[0] += 1
                    d=1
                elif keys[pygame.K_UP]:
                    player_pos[1] -= 1
                    d=2
                elif keys[pygame.K_DOWN]:
                    player_pos[1] += 1
                    d=3
                for y, row in enumerate(map_data):
                    for x, tile in enumerate(row):
                        if tile in solid_tiles:
                            tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                            while player_rect.colliderect(tile_rect):
                                # Undo the player movement
                                player_rect = pygame.Rect(player_pos, player_size)
                                if not player_rect.colliderect(tile_rect):
                                        break
                                if d==0:
                                    player_pos[0] += 1
                                elif d==1:
                                    player_pos[0] -= 1
                                elif d==2:
                                    player_pos[1] += 1
                                elif d==3:
                                    player_pos[1] -= 1
                                player_rect = pygame.Rect(player_pos, player_size)
                                if not player_rect.colliderect(tile_rect):
                                    break
            if keys[pygame.K_DOWN] or keys[pygame.K_UP] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                player_effects=tick()
    
        # Clear the screen
        screen.fill(BLACK)
    
        # Draw the map
        for y, row in enumerate(map_data):
            for x, tile in enumerate(row):
                # Calculate the tile position
                tile_x = x * TILE_SIZE
                tile_y = y * TILE_SIZE
                # Draw the tile
                if tile < NUM_TEXTURES:
                    texture = textures[tile]
                    screen.blit(texture, (tile_x, tile_y))
        screen.blit(ptx, (player_pos[0], player_pos[1]))
        overlay()
        # Update the screen
        pygame.display.update()
        # Limit the framerate
        clock.tick(60)
