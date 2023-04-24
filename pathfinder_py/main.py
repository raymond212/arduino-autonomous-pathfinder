import serial
from pathplanning import next_cell, search_bfs, convert_path_to_instructions, in_bound, is_obstacle, update_position, clear_obstacles
from visualizer import display_grid

PORT = "COM4"  # "COM4" for BT, "COM6" for arduino

print("Welcome to Pathfinder.")
print("Arduino connecting...")
arduino = serial.Serial(PORT, 9600, timeout=2)
arduino.flushInput()
print("Connection established.")


def main():
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

        if grid_is_outdated(grid, x, y, cur_dir):
            print("Grid Updated. New grid:")

            path = search_bfs(grid, (x, y), end)
            instructions = convert_path_to_instructions(path, cur_dir, end_dir)

            display_grid(grid, cur_dir, path)

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
    nx, ny = next_cell(grid, x, y, cur_dir)
    if not in_bound(grid, nx, ny):
        return False
    write("D")
    sees_obstacle = read()
    # print(sees_obstacle)
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
    with open("mydata.txt", "w") as f:
        f.write("{}".format([0, 1, 2]))


# test()


command = ""

while command != "quit":
    command = input("Navigate again?\n")
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

    main()
