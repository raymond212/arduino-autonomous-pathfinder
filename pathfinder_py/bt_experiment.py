import bluetooth
import serial
import time
import math
from heapq import heappush, heappop
from pathplanning import convert_path_to_instructions, search_bfs

from visualizer import display_grid


def get_dist(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


# port = "COM4"  # "COM4" for BT, "COM6" for arduino
# arduino = serial.Serial(port, 9600, timeout=2)
# print("Connected.")
# arduino.flushInput()


# def read():
#     return arduino.readline().decode('utf-8').rstrip()
#
#
# def write(x):
#     arduino.write(bytes(x, 'utf-8'))


def main():
    # with open("mydata.txt", "w") as f:
    #     f.write("{}".format([0, 1, 2]))
    #     f.write("{}".format([1, 2, 3]))
    # with open("mydata.txt") as f:
    #     a = f.readlines()
    #     print(a)
    # grid = [[0, 0, 1, 0],
    #         [1, 0, 0, 0],
    #         [0, 1, 1, 0],
    #         [0, 1, 0, 0]]
    # cur_dir = 1
    # path = search_bfs(grid, (3, 0), (1, 1))
    # display_grid(grid, cur_dir, path)
    print(get_dist((100, 100), (200, 200)))


main()

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
