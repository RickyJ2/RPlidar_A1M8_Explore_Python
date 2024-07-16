from rplidar import RPLidar
import pygame, math

#global variables
distances_list = []
first_run = True
running = True

pygame.init()
lidar = RPLidar('COM7')

health = lidar.get_health()
if(health[1] == 0):
    print("Health status: ", health[0])
else: 
    print("Error, health status: ", health[0], " error code: ", health[1])
    running = False
    lidar.stop()
    lidar.disconnect()

# Set up the drawing window
screen = pygame.display.set_mode([600, 600])

def GameUpdate(): 
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((20, 10, 30))
    for d in distances_list:
        dx = 300 + (d[2]*math.sin(math.radians(d[1])))
        dy = 300 + (d[2]*math.cos(math.radians(d[1])))
        pygame.draw.aaline(screen, pygame.Color(100,100,120), (300,300), (dx, dy), 1)
       
    pygame.draw.circle(screen, pygame.Color(100, 100, 120), (300, 300), 60)
    pygame.display.flip()

def main():
    global distances_list, first_run, running

    for scan in lidar.iter_scans('normal', 0, 1):
        distances_list = scan
        GameUpdate()
        lidar.clean_input()
        if not running:
            break

try:
    main()
except:
    running = False
    lidar.stop()
    lidar.disconnect()