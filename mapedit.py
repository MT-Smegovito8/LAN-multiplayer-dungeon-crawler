import pygame
import sys

# Define some constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TILE_SIZE = 32
NUM_TEXTURES = 4

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Load the textures
textures = []
for i in range(NUM_TEXTURES):
    texture = pygame.image.load(f'texture{i}.png').convert()
    textures.append(texture)

# Load the map data
map_data = []
with open('map.dat', 'r') as f:
    for line in f.readlines():
        row = list(map(int, line.strip()))
        map_data.append(row)
if len(map_data)!=15:
    map_data=[]
    jomama=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(15):
        map_data.append(jomama)
# Initialize Pygame


# Create a clock
clock = pygame.time.Clock()

# Create a font
font = pygame.font.SysFont(None, 30)

# Set the initial tile type
current_tile = 0
custom_event = pygame.USEREVENT + 1
pygame.time.set_timer(custom_event, 10)

# Main game loop
while True:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save the map data
            with open('map.dat', 'w') as f:
                for row in map_data:
                    f.write(''.join(map(str, row)) + '\n')
            pygame.quit()
            sys.exit()
        elif event.type == custom_event:
            mouse_state = pygame.mouse.get_pressed()
            if mouse_state[0]:
                # Manually post a MOUSEBUTTONDOWN event
                button = 1  # left mouse button
                pos = pygame.mouse.get_pos()
                mouseEvent = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': button, 'pos': pos})
                pygame.event.post(mouseEvent)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle mouse clicks
            x, y = event.pos
            tile_x = x // TILE_SIZE
            tile_y = y // TILE_SIZE
            if tile_x >= 0 and tile_x < len(map_data[0]) and tile_y >= 0 and tile_y < len(map_data):
                map_data[tile_y][tile_x] = current_tile
        elif event.type == pygame.KEYDOWN:
            # Handle key presses
            if event.key == pygame.K_2 and current_tile<NUM_TEXTURES-1:
                current_tile += 1
            elif event.key == pygame.K_1 and current_tile!=0:
                current_tile -= 1
            

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

    # Draw the current tile type
    tile_text = font.render(f'Current Tile: {current_tile}', True, WHITE)
    screen.blit(tile_text, (10, 10))

    # Update the screen
    pygame.display.update()

    # Limit the framerate
    clock.tick(60)
