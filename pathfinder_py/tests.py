from pathplanning import next_cell, search_bfs, create_graph, in_bound, convert_path_to_instructions, \
    calculate_turns, update_position


def test_update_position():
    grid = [[0] * 3 for _ in range(3)]
    assert update_position(0, 0, 1, "F") == (0, 1, 1)
    assert update_position(2, 2, 3, "R") == (2, 2, 0)
    assert update_position(1, 1, 2, "L") == (1, 1, 1)


def test_next_cell():
    grid = [[0] * 3 for _ in range(3)]
    assert next_cell(grid, 0, 0, 1) == (0, 1)
    assert next_cell(grid, 2, 2, 3) == (2, 1)
    assert next_cell(grid, 1, 1, 0) == (0, 1)
    assert next_cell(grid, 2, 0, 2) == (3, 0)


def test_bfs_1():
    grid = [[0] * 3 for _ in range(3)]
    grid[1][0] = 1
    grid[1][2] = 1
    # 000
    # 101
    # 000
    # Shortest path: (0,0) -> (0,1) -> (1,1) -> (2,1) -> (2,2)
    path = search_bfs(grid, (0, 0), (2, 2))
    assert path == [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]


def test_bfs_2():
    grid = [[0, 0, 0],
            [0, 1, 0]]
    path = search_bfs(grid, (1, 0), (1, 2))
    assert path == [(1, 0), (0, 0), (0, 1), (0, 2), (1, 2)]


def test_in_bound():
    grid = [[0] * 3 for _ in range(3)]
    assert in_bound(grid, 0, 0)
    assert in_bound(grid, 2, 2)
    assert in_bound(grid, 0, 1)
    assert not in_bound(grid, -1, 0)
    assert not in_bound(grid, 3, 3)
    assert not in_bound(grid, 0, 3)


def test_calculate_turns_1():
    turn_type, turn_num = calculate_turns(0, 1)
    assert turn_type == "R"
    assert turn_num == 1


def test_calculate_turns_2():
    turn_type, turn_num = calculate_turns(3, 2)
    assert turn_type == "L"
    assert turn_num == 1


def test_calculate_turns_3():
    turn_type, turn_num = calculate_turns(3, 1)
    assert turn_type == "R"
    assert turn_num == 2


def test_calculate_turns_4():
    turn_type, turn_num = calculate_turns(2, 2)
    assert turn_num == 0


def test_convert_path_to_instructions_1():
    path = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (1, 3)]
    instructions = "".join(convert_path_to_instructions(path, 1, 1))
    assert instructions == "FFRFFLFLFR"


def test_convert_path_to_instructions_2():
    path = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 0), (3, 0), (3, 1), (3, 2), (3, 1), (4, 1), (4, 2)]
    instructions = "".join(convert_path_to_instructions(path, 1, 1))
    assert instructions == "RFLFRFRFLFLFFRRFLFLF"


def test_convert_path_to_instructions_3():
    path = [(0, 0), (0, 1), (1, 1), (1, 2), (0, 2), (0, 3), (1, 3)]
    instructions = "".join(convert_path_to_instructions(path, 3, 0))
    assert instructions == "RRFRFLFLFRFRFRR"
