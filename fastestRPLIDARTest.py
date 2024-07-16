from fastestrplidar.fastestrplidar import FastestRplidar
import serial.tools.list_ports

port = ""
ports = list(serial.tools.list_ports.comports())
for p in ports:
    if p.pid == 60000:
        port = p.device

lidar = FastestRplidar(port=port)
lidar.connectlidar()
print(lidar.checkhealth())
lidar.startmotor()
result = lidar.fetchscandata()
print(result)
lidar.stopmotor()
