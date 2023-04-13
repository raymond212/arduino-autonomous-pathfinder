import serial
from collections import deque

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
PORT = "COM4"

# port = "COM4"  # "COM4" for BT, "COM6" for arduino
# arduino = serial.Serial(port, 9600, timeout=2)
# print("Connected.")
# arduino.flushInput()
#
# def read():
#     return arduino.readline().decode('utf-8').rstrip()
#
#
# def write(x):
#     arduino.write(bytes(x, 'utf-8'))

def main():
    print("Welcome to Pathfinder.")
    # print("Arduino connecting...")
    # arduino = serial.Serial(PORT, 9600, timeout=2)
    # arduino.flushInput()
    # print("Connected.")

    m, n = [int(x) for x in input("Rows, columns: ").split(" ")]
    cur = tuple([int(x) for x in input("Start coordinate: ").split(" ")])
    end = tuple([int(x) for x in input("Target coordinate: ").split(" ")])
    cur_dir = int(input("Start direction: "))
    end_dir = int(input("End direction: "))

    grid = [[0] * n for _ in range(m)]

    while cur != end or cur_dir != end_dir:
        path = search_bfs(grid, cur, end)
        if path == -1:
            print("No path found")
        instructions = convert_path_to_instructions(path, cur_dir, end_dir)
        for instruction in instructions:
            



def search_bfs(grid, start, end):
    q = deque([(start, [start])])  #
    visited = {start}

    while q:
        (x, y), path = q.popleft()
        if (x, y) == end:
            return path
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if not in_bound(grid, nx, ny) or (nx, ny) in visited or grid[nx][ny] == 1:
                continue
            new_path = list(path)
            new_path.append((nx, ny))
            q.append(((nx, ny), new_path))
            visited.add((nx, ny))

    return -1


def create_graph(grid):
    graph = {}  # cell : [neighboring cells]

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 1:  # Cell is obstacle, skip
                continue
            for dx, dy in DIRS:  # Cell is not obstacle, connect to neighbors
                nx, ny = x + dx, y + dy
                if in_bound(grid, nx, ny) and grid[nx][ny] == 0:
                    graph.setdefault((x, y), []).append((nx, ny))


def in_bound(grid, x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])


def convert_path_to_instructions(path, start_dir, end_dir):
    cur_dir = start_dir
    instructions = []

    for i in range(len(path) - 1):
        dx = path[i + 1][0] - path[i][0]
        dy = path[i + 1][1] - path[i][1]
        if dx == 0 and dy == 1:
            target_dir = 1
        elif dx == 1 and dy == 0:
            target_dir = 2
        elif dx == 0 and dy == -1:
            target_dir = 3
        else:
            target_dir = 0

        # rotate to correct direction
        turn_type, turn_num = calculate_turns(cur_dir, target_dir)
        instructions.extend([turn_type for _ in range(turn_num)])

        # move forward
        instructions.append("F")

        # update direction
        cur_dir = target_dir

    # rotate to correct direction in the end
    turn_type, turn_num = calculate_turns(cur_dir, end_dir)
    instructions.extend([turn_type for _ in range(turn_num)])

    return instructions


def calculate_turns(cur_dir, target_dir):
    left_turn_num = (cur_dir - target_dir) % 4
    right_turn_num = (target_dir - cur_dir) % 4
    if left_turn_num < right_turn_num:
        return "L", left_turn_num
    else:
        return "R", right_turn_num


main()
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
