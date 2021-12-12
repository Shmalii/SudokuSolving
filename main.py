import json
import copy
import os


def read_file(filename):
    with open(filename) as file:
        start_data = json.load(file)
    return start_data


def make_start_state(data):
    for row in range(9):
        for column in range(9):
            if data[row][column] == 0:
                data[row][column] = [i for i in range(1, 10)]
    return data


def clear_by_row(data):
    for row in range(9):
        element_to_delete = {column for column in data[row] if isinstance(column, int) or len(column) == 1}
        for column in range(9):
            if isinstance(data[row][column], list):
                value = data[row][column]
                if len(value) > 1:
                    data[row][column] = sorted(list(set(value) - element_to_delete))
                    if not data[row][column]:
                        return
                else:
                    data[row][column] = value[0]
    return data


def clear_by_column(data):
    for column in range(9):
        element_to_delete = set()
        for row in range(9):
            if isinstance(data[row][column], int):
                element_to_delete.add(data[row][column])
        for row in range(9):
            if isinstance(data[row][column], list):
                value = data[row][column]
                if len(value) > 1:
                    data[row][column] = sorted(list(set(value) - element_to_delete))
                    if not data[row][column]:
                        return
                else:
                    data[row][column] = value[0]
    return data


def clear_by_block(data):
    blocks = [(0, 3), (3, 6), (6, 9)]
    for block_row in blocks:
        for block_column in blocks:
            element_to_delete = set()
            for i in range(*block_row):
                for j in range(*block_column):
                    if isinstance(data[i][j], int):
                        element_to_delete.add(data[i][j])
            for i in range(*block_row):
                for j in range(*block_column):
                    if isinstance(data[i][j], list):
                        value = data[i][j]
                        if len(value) > 1:
                            data[i][j] = sorted(list(set(value) - element_to_delete))
                            if not data[i][j]:
                                return
                        else:
                            data[i][j] = value[0]
    return data


def fix_mark(data):
    find_len = 2
    while find_len < 10:
        for row in range(9):
            for column in range(9):
                value = data[row][column]
                if isinstance(value, list) and len(value) == find_len:
                    return row, column, value

        find_len += 1
    return None, None, None


def clear_sudoku_field(data):
    for row in range(9):
        for column in range(9):
            value = data[row][column]
            data[row][column] = value if isinstance(value, int) or len(value) > 1 else value[0]
    return data


def print_sudoku(data):
    for row in data:
        for elem in row:
            print(elem, end=' ')
        print('\n')


def clear_elements_cycle(data):
    clear_functions = [clear_by_row, clear_by_column, clear_by_block]
    data_check = copy.deepcopy(data)
    while True:
        for function in clear_functions:
            data = function(copy.deepcopy(data))
            if not data:
                return None
        data = clear_sudoku_field(data)
        if data_check == data:
            return data
        else:
            data_check = copy.deepcopy(data)


def check_solved(data):
    for i in range(9):
        for j in range(9):
            if not isinstance(data[i][j], int):
                return False
    return True


def fixing_recursion(data):
    if check_solved(data):
        return data
    row, column, values = fix_mark(data)
    print(f"Fixing object row: {row}, col: {column}, possible values: {values}")
    for value in values:
        data_with_fixed = copy.deepcopy(data)
        data_with_fixed[row][column] = value
        data_with_fixed = clear_elements_cycle(data_with_fixed)
        print(f"Try to fix {value}")
        if data_with_fixed:
            data_with_fixed = fixing_recursion(data_with_fixed)
        if data_with_fixed and check_solved(data_with_fixed):
            return data_with_fixed
    return


def solve(filename):
    data = make_start_state(read_file(filename))
    data_copy = clear_elements_cycle(copy.deepcopy(data))
    while data_copy != data:
        if not data_copy:
            return None
        elif check_solved(data_copy):
            return data_copy
        data = copy.deepcopy(data_copy)
        data_copy = fixing_recursion(data_copy)


def main():
    for i in range(1, 100):
        file = f"sudoku_0{i}.json"
        if os.path.isfile(file):
            print(f"\n\nFile {file} exist")
            solved = solve(file)
            if solved:
                print_sudoku(solved)
            else:
                print("This sudoku does no have solution")


if __name__ == '__main__':
    main()
