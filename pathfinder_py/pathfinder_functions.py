from collections import deque

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def next_cell(grid, x, y, cur_dir):
    if cur_dir == 0:
        return x - 1, y
    if cur_dir == 1:
        return x, y + 1
    if cur_dir == 2:
        return x + 1, y
    if cur_dir == 3:
        return x, y - 1


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



#
#
# class Pathfinder:
#
#     def in_bound(self, grid, x, y):
#         return 0 <= x < len(grid) and 0 <= y < len(grid[0])
#
#     def print_arr(self, grid):
#         s = ""
#         for i in range(len(grid)):
#             for j in range(len(grid[0])):
#                 s += str(grid[i][j])
#             s += "\n"
#         return s
#
#     def create_graph(self, grid):
#         graph = {}  # cell : [(neighboring cell, distance)]
#
#         for i in range(len(grid)):
#             for j in range(len(grid[0])):
#                 if grid[i][j] == 1:  # Cell is obstacle, skip
#                     continue
#                 for dx, dy in DIRS:  # Cell is not obstacle, connect to neighbors
#                     nx, ny = i + dx, j + dy
#                     if in_bound(grid, nx, ny) and grid[nx][ny] == 0:
#                         graph.setdefault((i, j), []).append(((nx, ny), 1))  # Distance is set to 1 in grid
#         return graph
#
#     def generate_heuristics(grid, end):
#         heuristics = {}  # cell : Manhattan distance from end cell
#
#         for i in range(len(grid)):
#             for j in range(len(grid[0])):
#                 heuristics[(i, j)] = abs(i - end[0]) + abs(j - end[1])  # Manhattan distance
#
#         return heuristics
#
#     # path cost
#     # heuristic cost
#
#     def astar(grid, start, end):
#         graph = create_graph(grid)
#         heuristics = generate_heuristics(grid, end)
#         visited = {start}
#
#         min_heap = [(heuristics[start], start)]  # combined cost, cell
#
#         prev = {}  # cell : previous cell
#         costs = {start: 0}  # cell : dist from start
#
#         while min_heap:
#             combined_cost, cost, u = heappop(min_heap)
#             if u == end:
#                 break
#             for v, distance in graph[u]:
#                 if v in costs:  # Check if better to go to neighbor through current node
#                     alt_cost = cost + distance
#                     if alt_cost < costs[v]:
#                         costs[v] = alt_cost
#                         prev[v] = u
#                 else:  # Add v to queue
#                     costs[v] = cost + distance
#                     prev[v] = u
#                     heappush(min_heap, (costs[v] + heuristics[v], v))
#
#             if node == end:
#                 res = path
#                 break
#             for neighbor, distance in graph[node]:
#                 if neighbor in visited:
#                     continue
#                 new_heuristic = heuristic + distance - heuristics[node] + heuristics[neighbor]
#                 new_path = list(path)
#                 new_path.append(neighbor)
#                 heappush(min_heap, (new_heuristic, neighbor, new_path))
#
#         for x, y in res:
#             grid[x][y] = "P"
#         print(iterations)
#         return print_arr(grid)
