import serial
from serial import SerialException
import cv2 as cv
from time import sleep
from threading import Thread

from pathplanning import next_cell, search_bfs, convert_path_to_instructions, in_bound, update_position, \
    clear_obstacles
from visualizer import display_grid
from vision import identify_obstacles

PORT = "COM4"  # "COM4" for BT, "COM6" for arduino

print("Welcome to Pathfinder.")
print("Connecting to Arduino...")

try:
    arduino = serial.Serial(PORT, 9600, timeout=2)
    arduino.flushInput()
    print("Connection established.")
except SerialException:
    print("Connection failed. Terminating...")

obstacles = set()

def stream_video():
    cap = cv.VideoCapture(1)
    while True:
        success, frame = cap.read()

        if not success:
            break

        global obstacles
        obstacles = identify_obstacles(frame)
        # cv.imshow('Video', frame)

        # exits when q key is pressed
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()


def main():
    print("[navigate] [override] [quit]")

    command = input()
    while command != "quit":
        if command == "override":
            while True:
                s = input()
                if s == "quit":
                    break
                elif s == "D":
                    write("D")
                    obstacle = read()
                    print(obstacle)
                else:
                    execute_instruction(s)

        navigate()
        command = input("Navigate again?\n")


def navigate():
    m, n = 5, 4
    # m, n = [int(x) for x in input("Rows, columns: ").split(" ")]
    grid = [[0] * n for _ in range(m)]

    x, y = tuple([int(x) for x in input("Start coordinate: ").split(" ")])
    end = tuple([int(x) for x in input("Target coordinate: ").split(" ")])
    cur_dir = int(input("Start direction: "))
    end_dir = int(input("End direction: "))
    print("Enter location of obstacles (finish with -1): ")

    while True:
        location = input()
        if location == "-1":
            break
        a, b = [int(x) for x in location.split(" ")]
        if in_bound(grid, a, b):
            grid[a][b] = 1
        else:
            print("Invalid location.")

    path = search_bfs(grid, (x, y), end)
    instructions = convert_path_to_instructions(path, cur_dir, end_dir)
    display_grid(grid, cur_dir, path)
    print("".join(instructions))

    print("Grid initialized.")
    input("Enter S to start navigation.")

    while (x, y) != end or cur_dir != end_dir:
        if len(instructions) == 0:
            print("No path found. Clearing obstacles and exploring.")
            clear_obstacles(grid)

            path = search_bfs(grid, (x, y), end)
            instructions = convert_path_to_instructions(path, cur_dir, end_dir)
            continue
        if grid_is_outdated(grid, x, y, cur_dir):
            print("Grid Updated. New grid:")

            path = search_bfs(grid, (x, y), end)
            instructions = convert_path_to_instructions(path, cur_dir, end_dir)

            display_grid(grid, cur_dir, path)
            # continue
        if not instructions:
            continue
        instruction = instructions.pop(0)
        print("Current instruction: {}".format(instruction))
        execute_instruction(instruction)

        if instruction == "F":
            path.pop(0)

        x, y, cur_dir = update_position(x, y, cur_dir, instruction)
        display_grid(grid, cur_dir, path)

    print("Destination reached.")


def execute_instruction(instruction):
    write(instruction)
    read()


def grid_is_outdated(grid, x, y, cur_dir):
    outdated = False

    nx, ny = next_cell(grid, x, y, cur_dir)
    # if in_bound(grid, nx, ny):
    #     write("D")
    #     sees_obstacle = read()
    #     # print(sees_obstacle)
    #     if sees_obstacle == "Yes":
    #         if is_obstacle(grid, nx, ny):
    #             outdated = False
    #         else:
    #             grid[nx][ny] = 1
    #             outdated = True
    #     else:
    #         if not is_obstacle(grid, nx, ny):
    #             outdated = False
    #         else:
    #             grid[nx][ny] = 0
    #             outdated = True

    # cap = cv.VideoCapture(1)
    # success, frame = cap.read()
    # obstacles = identify_obstacles(frame)

    global obstacles

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0 and (i, j) not in obstacles:
                continue
            elif grid[i][j] == 0 and (i, j) in obstacles:
                grid[i][j] = 1
                outdated = True
            elif grid[i][j] == 1 and (i, j) not in obstacles:
                grid[i][j] = 0
                outdated = True

    return outdated


def read_instant():
    return arduino.readline().decode('utf-8').rstrip()


def write(msg):
    arduino.write(bytes(msg, 'utf-8'))


def read():
    while True:
        s = read_instant()
        if s != "":
            arduino.flushInput()
            return s


def test():
    with open("mydata.txt", "w") as f:
        f.write("{}".format([0, 1, 2]))


# test()

if __name__ == "__main__":
    t1 = Thread(target=stream_video, args=())
    t2 = Thread(target=main, args=())

    t1.start()
    t2.start()
