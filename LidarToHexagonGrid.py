from time import sleep
from lidar import Lidar
from hexagon import hexGrid
import math

map = []
resolution = 100
robot_pose = (300, 300)

def main():
    global map
    lidar = Lidar("COM7")
    lidar.init()
    if(lidar.checkHealth()):
        lidar.start()
    sleep(5)
    try:
        while True:
            lidar_data = lidar.getScanData()
            temp = []
            for i, d in enumerate(lidar_data):
                q = robot_pose[0] + int((d*(math.sin(math.radians(i))*math.sqrt(3) + math.cos(math.radians(i))))/resolution)
                r = robot_pose[1] + -1 * int(d*math.sin(math.radians(i))*math.sqrt(3)/(2*resolution))
                temp.append(hexGrid(q, r))
            map = temp
    except:
        lidar.stop()
   
main()

# sleep(10)