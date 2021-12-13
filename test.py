import pytest
from main import *
from boards import *


@pytest.mark.parametrize('data', [board])
def test_read_function(data):
    filename = "file_test.json"
    with open(filename, 'w') as file:
        file.write(repr(data))
    read_data = read_file(filename)
    os.remove(filename)
    assert read_data == data, "Read function does not work correctly"


@pytest.mark.parametrize("data, expected", [(board, board_start_state)])
def test_make_start_state(data, expected):
    assert make_start_state(copy.deepcopy(data)) == expected, "Make start state func does not work correctly"


@pytest.mark.parametrize('data', [board_start_state])
def test_check_solve(data):
    assert not check_solved(board_start_state), "Check solve function does not work correctly"


@pytest.mark.parametrize('data, cleared_data', [(board_clear_field, board_solved)])
def test_clear_field_function(data, cleared_data):
    assert clear_sudoku_field(copy.deepcopy(data)) == cleared_data, "Clear field function does not work correctly"


@pytest.mark.parametrize('data, expected_result', [(board_start_state, board_start_state_cleared_by_row)])
def test_clear_by_row(data, expected_result):
    assert clear_by_row(copy.deepcopy(data)) == expected_result, "Clear by row function does not work correctly"


@pytest.mark.parametrize('data, expected_result', [(board_start_state, board_start_state_cleared_by_column)])
def test_clear_by_column(data, expected_result):
    assert clear_by_column(copy.deepcopy(data)) == expected_result, "Clear by column row does not work correctly"


@pytest.mark.parametrize('data, expected_result', [(board_start_state, board_start_state_cleared_by_block)])
def test_clear_by_block(data, expected_result):
    assert clear_by_block(copy.deepcopy(data)) == expected_result, "Clear by block function does not work correctly"


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
