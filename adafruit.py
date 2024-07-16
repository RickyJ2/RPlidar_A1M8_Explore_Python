from math import floor
from adafruit_rplidar import RPLidar
import pygame, math

#global variables
running = True
max_distance = 0
scan_data = [0] * 360

pygame.init()
# Setup the RPLidar
PORT_NAME = "COM7"
lidar = RPLidar(None, PORT_NAME, timeout=3)

# Set up the drawing window
screen = pygame.display.set_mode([600, 600])

def GameUpdate(distances_list): 
    global running
    # print(distances_list)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((20, 10, 30))
    for i, d in enumerate(distances_list):
        dx = 300 + (d*math.sin(math.radians(i)))
        dy = 300 + (d*math.cos(math.radians(i)))
        pygame.draw.aaline(screen, pygame.Color(100,100,120), (300,300), (dx, dy), 1)
       
    pygame.draw.circle(screen, pygame.Color(100, 100, 120), (300, 300), 60)
    pygame.display.flip()

def main():
    for scan in lidar.iter_scans():
        for _, angle, distance in scan:
            scan_data[min([359, floor(angle)])] = distance
        GameUpdate(scan_data)

try:
    main()
except:
    running = False
    lidar.stop()
    lidar.disconnect()