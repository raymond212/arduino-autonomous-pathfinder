import serial
from pathplanning import next_cell, search_bfs, convert_path_to_instructions, in_bound, is_obstacle, update_position
from visualizer import display_grid

PORT = "COM4"  # "COM4" for BT, "COM6" for arduino

print("Welcome to Pathfinder.")
print("Arduino connecting...")
arduino = serial.Serial(PORT, 9600, timeout=2)
arduino.flushInput()
print("Connection established.")


def main():
    # command = ""
    # while command != "Quit":
    #     command = input()
    #     write(arduino, command)
    #     print(read(arduino))
    #
    # arduino.close()

    m, n = 5, 4
    # m, n = [int(x) for x in input("Rows, columns: ").split(" ")]
    grid = [[0] * n for _ in range(m)]

    # x, y = 2, 0
    # end = (4, 3)
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

    display_grid(grid, x, y, cur_dir)
    print("Grid initialized.")

    path = search_bfs(grid, (x, y), end)
    instructions = convert_path_to_instructions(path, cur_dir, end_dir)

    print("".join(instructions))
    input("Enter S to start navigation.")

    while (x, y) != end or cur_dir != end_dir:
        if grid_is_outdated(grid, x, y, cur_dir):
            print("Grid Updated. New grid:")
            display_grid(grid, x, y, cur_dir)

            path = search_bfs(grid, (x, y), end)
            if len(path) == 0:
                print("No path found. Quitting...")
                return

            instructions = convert_path_to_instructions(path, cur_dir, end_dir)

        instruction = instructions.pop(0)
        print("Current instruction: {}".format(instruction))
        execute_instruction(instruction)
        print("Executed")
        # print("{} {} {}".format(x, y, cur_dir))
        x, y, cur_dir = update_position(x, y, cur_dir, instruction)
        display_grid(grid, x, y, cur_dir)

    print("Destination reached.")


def execute_instruction(instruction):
    write(instruction)
    read()


def grid_is_outdated(grid, x, y, cur_dir):
    nx, ny = next_cell(grid, x, y, cur_dir)
    if not in_bound(grid, nx, ny):
        return False
    write("D")
    sees_obstacle = read()
    print(sees_obstacle)
    if sees_obstacle == "Yes":
        if is_obstacle(grid, nx, ny):
            return False
        grid[nx][ny] = 1
        return True
    else:
        if not is_obstacle(grid, nx, ny):
            return False
        grid[nx][ny] = 0
        return True


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
    grid = [[0, 0, 0],
            [0, 0, 0]]
    display_grid(grid, 0, 1, 0)

    # while True:
    #
    #


# test()
command = ""
while command != "quit":

    command = input("Navigate again?\n")
    if command == "override":
        while True:
            instruction = input()
            if instruction == "quit":
                break
            elif instruction == "D":
                write("D")
                sees_obstacle = read()
                arduino.flushInput()
                print(sees_obstacle)
            else:
                execute_instruction(instruction)

    main()

# main()


# m = 3
# n = 3
# grid = [[0] * m for _ in range(n)]
# start = (0, 0)
# end = (m - 1, n - 1)

#
#
# grid = [[0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
#         [1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
#         [0, 0, 1, 0, 0, 1, 1, 1, 0, 0],
#         [0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], ]
