import bluetooth
import serial
import time
from heapq import heappush, heappop

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

port = "COM4"  # "COM4" for BT, "COM6" for arduino
arduino = serial.Serial(port, 9600, timeout=2)
print("Connected.")
arduino.flushInput()


def read():
    return arduino.readline().decode('utf-8').rstrip()


def write(x):
    arduino.write(bytes(x, 'utf-8'))


while True:
    num = input("Enter a number: ")
    write(num)
    print(read())










arduino.close()

# nearby_devices = bluetooth.discover_devices(duration=5, flush_cache=True, lookup_names=True, lookup_class=False, device_id=-1)
#
# print("Found {} devices.".format(len(nearby_devices)))
#
# for i, (address, name) in enumerate(nearby_devices):
#     print("{:<1} {:<30}{}".format(str(i), name, address))
#
# index = int(input("Select device: "))
# sensor_address = nearby_devices[index][0]
#
# socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# socket.connect((sensor_address, 1))
#
# print(sensor_address)
#
# socket.close()
