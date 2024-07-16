import math
from adafruit_rplidar import RPLidar, RPLidarException
import threading

class Lidar:
    def __init__(self, port):
        self.port = port
        self.scan_data = [0] * 360
        #in mm
        self.max_distance = 10000
        self.min_distance = 0
        self.initState = False
    
    def checkHealth(self):
        print(self.lidar.health)
        if self.lidar.health[1] == 0 : 
            return True
        else :
            return False

    def init(self):
        try:
            self.lidar = RPLidar(None, self.port, timeout=3)
            self.lidar.clear_input()
            self.initState = True
        except RPLidarException as e:
            print(e)
        
    def start(self):
        if not self.initState:
            self.init()
        try:
            thread = threading.Thread(target=self._scan)
            thread.start()
        except RPLidarException as e:
            print(e)
        except e:
            print(e)

    def _scan(self):
        for scan in self.lidar.iter_scans():
            temp = [0]*360
            for _, angle, distance in scan:
                if distance > self.max_distance or distance < self.min_distance:
                    continue
                temp[min([359, math.floor(angle)])] = distance
            self.scan_data = temp

    def getScanData(self):
        return self.scan_data

    def stop(self):
        try:
            self.lidar.stop()
            self.lidar.disconnect()
        except RPLidarException as e:
            print(e)