ARROWS = ["↑", "→", "↓", "←"]


def display_grid(grid, x, y, cur_dir):
    m, n = len(grid), len(grid[0])
    s = ""
    for i in range(m):
        for j in range(n):
            if i == x and j == y:
                s += "|" + ARROWS[cur_dir]
            else:
                s += "|" + str(grid[i][j])
        s += "|\n"
    print(s.strip())
