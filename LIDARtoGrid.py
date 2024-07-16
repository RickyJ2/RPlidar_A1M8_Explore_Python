from math import floor
from adafruit_rplidar import RPLidar
import pygame, math

#params
grid_size = 10 #grid size in pixel for display
map_size = 3000 #mm
resolution = 100 #mm per grid
grid_count = int(map_size/resolution)
robot_pose = (grid_count/2, grid_count/2) 

#global variables
running = True
scan_data = [0] * 360
grid_map = [[-1 for i in range(grid_count)] for j in range(grid_count)]

pygame.init()
# Setup the RPLidar
PORT_NAME = "COM7"
lidar = RPLidar(None, PORT_NAME, timeout=3)

# Set up the drawing window
screen = pygame.display.set_mode([grid_count*grid_size, grid_count*grid_size])

def ProcessData(distances_list): 
    global grid_map
    for i, d in enumerate(distances_list):
        dx = int(robot_pose[0] + (d*math.sin(math.radians(i)))/resolution)
        dy = int(robot_pose[1] + (d*math.cos(math.radians(i)))/resolution)
        if(dx >= 0 and dx < grid_count and dy >= 0 and dy < grid_count):
            grid_map[dx][dy] = 1
            #give value 0 to all the cells between the robot and the obstacle
            for j in range(1, int(d/resolution)):
                grid_map[int(robot_pose[0] + j*math.sin(math.radians(i)))][int(robot_pose[1] + j*math.cos(math.radians(i)))] = 0

def DisplayUpdate():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((128, 128, 128))
    for idxI,i in enumerate(grid_map):
        for idxJ,j in enumerate(i):
            if j == 1:
                pygame.draw.rect(screen, pygame.Color(0,0,0), (idxI*grid_size,idxJ*grid_size,grid_size,grid_size))
            if j == 0:
                pygame.draw.rect(screen, pygame.Color(255,255,255), (idxI*grid_size,idxJ*grid_size,grid_size,grid_size))
    pygame.draw.circle(screen, pygame.Color(100, 100, 120), (robot_pose[0]*grid_size,robot_pose[1]*grid_size), grid_size)
    pygame.display.flip()

def main():
    for scan in lidar.iter_scans():
        for _, angle, distance in scan:
            scan_data[min([359, floor(angle)])] = distance
        ProcessData(scan_data)
        DisplayUpdate()

try:
    main()
except Exception as e:
    print(e)
    running = False
    lidar.stop()
    lidar.disconnect()