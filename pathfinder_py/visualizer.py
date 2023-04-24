CAR_ORIENTATION = ["▲", "▶", "▼", "◀"]
ADJACENT = {(-1, 0): "A",
                    (0, 1): "B",
                    (1, 0): "C",
                    (0, -1): "D"}
ARROWS = {("A", "B"): "↘",
          ("A", "C"): "↓",
          ("A", "D"): "↙",
          ("B", "A"): "↖",
          ("B", "C"): "↙",
          ("B", "D"): "←",
          ("C", "A"): "↑",
          ("C", "B"): "↗",
          ("C", "D"): "↖",
          ("D", "A"): "↗",
          ("D", "B"): "→",
          ("D", "C"): "↘"}


def display_grid(grid, cur_dir, path):
    if not path:
        return

    m, n = len(grid), len(grid[0])
    s = ""
    for x in range(m):
        for y in range(n):
            if x == path[0][0] and y == path[0][1]:
                s += "|" + CAR_ORIENTATION[cur_dir]
            elif x == path[-1][0] and y == path[-1][1]:
                s += "|X"
            elif (x, y) in path:
                idx = path.index((x, y))
                px, py = path[idx - 1]
                nx, ny = path[idx + 1]
                s += "|" + ARROWS[ADJACENT[(px - x, py - y)],ADJACENT[(nx - x, ny - y)]]
            else:
                s += "|" + str(grid[x][y])
        s += "|\n"
    print(s.strip())
