import pygame
import sys
import time
import socket
import threading

received_data=None
def send_to_local_ips(data):
    # Get the list of local IP addresses
    local_ips = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")]
    print(local_ips)
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set the socket timeout to 1 second
    sock.settimeout(1)

    # Send the data to each local IP address on port 80
    for ip in local_ips:
        try:
            sock.sendto(data.encode(), (ip, 80))
            print(f"Sent {data} to {ip}:80")
        except socket.error as e:
            print(f"Failed to send {data} to {ip}:80: {e}")

    # Close the socket
    sock.close()
def receive_from_local_ips():
    # Create a UDP socket and bind it to port 80
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 80))

    # Set the socket timeout to 0.1 seconds
    sock.settimeout(0.1)

    # Receive data from the socket
    try:
        data, addr = sock.recvfrom(1024)
        received_data = data.decode()
    except socket.timeout:
        received_data = None
    finally:
        # Close the socket
        sock.close()
# Define some constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TILE_SIZE = 32
NUM_TEXTURES = 3

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)
## printing the hostname and ip_address
thread = threading.Thread(target=receive_from_local_ips)
thread.daemon = True
thread.start()
print(f"Hostname: {hostname}")
print("IP Address:" + ip_address)

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
player_speed = 4
# Load the textures
textures = []
for i in range(NUM_TEXTURES):
    texture = pygame.image.load(f'texture{i}.png').convert()
    textures.append(texture)

# Load the map data
with open('map.dat', 'r') as f:
    map_data = [list(map(int, line.strip())) for line in f.readlines()]


jtimer=0
# Create a clock
clock = pygame.time.Clock()
input_box = pygame.Rect(0, 0, 0, 0)
font = pygame.font.Font(None, 16)
input_text = ''
solid_tiles=[1]
deadly_tiles=[2]
isOpen=False
# Main game loop
sus="-"
d=0
while True:
    jtimer+=1
    if jtimer==60:
        jtimer=0
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            print("closed")
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LCTRL:
            # Open the text input window
            input_box = pygame.Rect(0, 450, 140, 32)
            input_box.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.05) # set position to the center of the screen
            pygame.key.set_repeat(10,10)
            isOpen=True
        elif event.key == pygame.K_RETURN and isOpen:
            pygame.key.set_repeat(10,10)
            isOpen=False
            # Save the input text to a variable and close the text input window
            input_text = input_text.strip()
            input_text = input_text[:20] # Limit to 20 characters
            input_text = input_text.lower()
            input_box = pygame.Rect(0, 0, 0, 0)
            pygame.key.set_repeat()
            print("jomama: "+input_text)
            send_to_local_ips(input_text)
            input_text=""
        elif event.key == pygame.K_BACKSPACE and isOpen:
            # Remove the last character from the input text
            for i in range(1):
                try:
                    input_text = input_text.rstrip(input_text[-1])
                except:
                    input_text=""
            time.sleep(0.1)
        if event.key == pygame.K_ESCAPE and isOpen:
            pygame.key.set_repeat(10,10)
            isOpen=False
            input_text = ""
            input_box = pygame.Rect(0, 0, 0, 0)
            pygame.key.set_repeat()
        try:
            if isOpen and chr(event.key)!=sus:
                # Append the pressed key to the input text
                try:
                    input_text += chr(event.key)
                    sus=chr(event.key)
                except:
                    sus="-"
            elif isOpen:
                time.sleep(0.1)
                sus="-"
        except:
            sus="-"
    player_rect = pygame.Rect(player_pos, player_size)
    keys = pygame.key.get_pressed()
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
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            if tile in deadly_tiles:
                tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if jtimer==0 and player_rect.colliderect(tile_rect):
                    player_health-=1
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
    if received_data is not None:
        jomama=received_data
        print(jomama)
    pygame.draw.rect(screen, BLACK, input_box, 2)
    text_surface = font.render(input_text, True, WHITE)
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
    text_surface2 = font.render(received_data, True, WHITE)
    screen.blit(text_surface2, (0, 0))
    screen.blit(ptx, (player_pos[0], player_pos[1]))
    for i in range(10):
        if player_health>=i:
            screen.blit(health,(i*12,0))
        else:
            screen.blit(emptyhealth,(i*12,0))
    # Update the screen
    pygame.display.update()
    # Limit the framerate
    clock.tick(60)
