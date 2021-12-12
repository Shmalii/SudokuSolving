import json
import pytest
from main import *

board = [
    [7, 5, 1, 8, 0, 2, 4, 6, 3],
    [2, 3, 6, 1, 7, 4, 8, 9, 5],
    [8, 0, 4, 5, 0, 3, 1, 7, 2],
    [6, 4, 5, 3, 2, 9, 7, 1, 8],
    [0, 2, 9, 4, 8, 0, 3, 0, 6],
    [3, 7, 8, 6, 5, 0, 0, 0, 0],
    [9, 0, 0, 0, 0, 0, 0, 8, 0],
    [5, 6, 2, 7, 0, 0, 0, 0, 1],
    [4, 8, 3, 9, 1, 6, 5, 2, 7]
]

board_start_state = [
    [7, 5, 1, 8, [1, 2, 3, 4, 5, 6, 7, 8, 9], 2, 4, 6, 3],
    [2, 3, 6, 1, 7, 4, 8, 9, 5],
    [8, [1, 2, 3, 4, 5, 6, 7, 8, 9], 4, 5, [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 1, 7, 2],
    [6, 4, 5, 3, 2, 9, 7, 1, 8],
    [[1, 2, 3, 4, 5, 6, 7, 8, 9], 2, 9, 4, 8, [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, [1, 2, 3, 4, 5, 6, 7, 8, 9], 6],
    [3, 7, 8, 6, 5, [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],
     [1, 2, 3, 4, 5, 6, 7, 8, 9]],
    [9, [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],
     [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], 8,
     [1, 2, 3, 4, 5, 6, 7, 8, 9]],
    [5, 6, 2, 7, [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9],
     [1, 2, 3, 4, 5, 6, 7, 8, 9], 1],
    [4, 8, 3, 9, 1, 6, 5, 2, 7]
]

board_solved = [
     [7, 5, 1, 8, 9, 2, 4, 6, 3],
     [2, 3, 6, 1, 7, 4, 8, 9, 5],
     [8, 9, 4, 5, 6, 3, 1, 7, 2],
     [6, 4, 5, 3, 2, 9, 7, 1, 8],
     [1, 2, 9, 4, 8, 7, 3, 5, 6],
     [3, 7, 8, 6, 5, 1, 2, 4, 9],
     [9, 1, 7, 2, 3, 5, 6, 8, 4],
     [5, 6, 2, 7, 4, 8, 9, 3, 1],
     [4, 8, 3, 9, 1, 6, 5, 2, 7]
]

board_clear_field = [
     [7, 5, 1, 8, 9, 2, 4, 6, 3],
     [2, [3], 6, 1, 7, 4, 8, 9, 5],
     [8, 9, 4, 5, 6, 3, 1, 7, 2],
     [6, 4, 5, 3, 2, 9, 7, 1, 8],
     [1, 2, 9, 4, [8], 7, 3, 5, 6],
     [3, 7, 8, 6, 5, 1, 2, 4, 9],
     [9, 1, 7, 2, 3, 5, 6, 8, 4],
     [5, 6, 2, 7, 4, 8, 9, 3, 1],
     [4, [8], 3, 9, 1, 6, 5, 2, 7]
]

board_with_error = [
    [7, 5, 1, 8, 0, 2, 4, 6, 3],
    [2, 3, 6, 1, 7, 4, 8, 9, 5],
    [8, 0, 4, 5, 0, 3, 1, 7, 2],
    [6, 4, 5, 3, 2, 9, 7, 1, 8],
    [0, 2, 9, 4, 8, 0, 3, 0, 6],
    [3, 7, 8, 6, 5, 0, 0, 0, 0],
    [9, 0, 0, 0, 0, 0, 0, 8, 0],
    [5, 6, 2, 7, 0, 0, 0, 0, 1],
    [4, 8, 3, 9, 1, 6, 2, 5, 7]
]


@pytest.mark.parametrize("data, expected", [(board, board_start_state)])
def test_make_start_state(data, expected):
    assert make_start_state(data) == expected, "Make start state func does not work correctly"


@pytest.mark.parametrize('data', [board])
def test_read_function(data):
    filename = "file_test.json"
    with open(filename, 'w') as file:
        file.write(repr(data))
    read_data = read_file(filename)
    os.remove(filename)
    assert read_data == data, "Read function does not work correctly"


@pytest.mark.parametrize('data', [board_start_state])
def test_check_solve(data):
    assert not check_solved(board_start_state), "Check solve function does not work correctly"


@pytest.mark.parametrize('data, solved_data, data_with_error', [(board, board_solved, board_with_error)])
def test_solve_function(data, solved_data, data_with_error):
    filename = "file_test.json"
    with open(filename, 'w') as file:
        file.write(repr(data))
    solved = solve(filename)
    assert solved == solved_data, "Solve function does not work correctly. Expected solved sudoku"
    with open(filename, 'w') as file:
        file.write(repr(data_with_error))
    solved = solve(filename)
    os.remove(filename)
    assert not solved, "Solve function does not work correctly. Expected unsolved sudoku"


@pytest.mark.parametrize('data, cleared_data', [(board_clear_field, board_solved)])
def test_clear_field_function(data, cleared_data):
    assert clear_sudoku_field(data) == cleared_data, "Clear field function does not work correctly"
