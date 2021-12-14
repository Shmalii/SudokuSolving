import json
import copy
import os
from collections import Counter
from collections import namedtuple

index = namedtuple('index', ('row', 'column'))


class DeletedMark:
    del_index = index(-1, -1)


class FixedMark:
    fix_index = index(-1, -1)


def read_file(filename):
    with open(filename) as file_read:
        start_data = json.load(file_read)
    return start_data


def make_start_state(data):
    for row in range(9):
        for column in range(9):
            if data[row][column] == 0:
                data[row][column] = [i for i in range(1, 10)]
    return data


def clear_by_row(data):
    global blya
    for row in range(9):
        element_to_delete = set()
        for elem in data[row]:
            if isinstance(elem, int):
                element_to_delete.add(elem)
            elif len(elem) == 1:
                element_to_delete.add(elem[0])
        for column in range(9):
            if isinstance(data[row][column], list):
                value = data[row][column]
                if len(value) > 1:
                    sub = list(set(value) - element_to_delete)
                    if not sub:
                        DeletedMark.del_index = index(row, column)
                        return
                    data[row][column] = sorted(sub) if len(sub) > 1 else sub[0]
                elif FixedMark.fix_index != (row, column):
                    data[row][column] = value[0]

    return data


def clear_by_column(data):
    global blya
    for column in range(9):
        element_to_delete = set()
        for row in range(9):
            if isinstance(data[row][column], int):
                element_to_delete.add(data[row][column])
            elif len(data[row][column]) == 1:
                element_to_delete.add(data[row][column][0])
        for row in range(9):
            if isinstance(data[row][column], list):
                value = data[row][column]
                if len(value) > 1:
                    sub = list(set(value) - element_to_delete)
                    if not sub:
                        DeletedMark.del_index = index(row, column)
                        return
                    data[row][column] = sorted(sub) if len(sub) > 1  else sub[0]
                elif FixedMark.fix_index != (row, column):
                    data[row][column] = value[0]
    return data


def clear_by_block(data):
    global blya
    blocks = [(0, 3), (3, 6), (6, 9)]
    for block_row in blocks:
        for block_column in blocks:
            element_to_delete = set()
            for i in range(*block_row):
                for j in range(*block_column):
                    if isinstance(data[i][j], int):
                        element_to_delete.add(data[i][j])
                    elif len(data[i][j]) == 1:
                        element_to_delete.add(data[i][j][0])
            for i in range(*block_row):
                for j in range(*block_column):
                    if isinstance(data[i][j], list):
                        value = data[i][j]
                        if len(value) > 1:
                            sub = list(set(value) - element_to_delete)
                            if not sub:
                                DeletedMark.del_index = index(i, j)
                                return
                            data[i][j] = sorted(sub) if len(sub) > 1 else sub[0]

                        elif FixedMark.fix_index != (i, j):
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
            if not check_inconsistency(data):
                return None
        if data_check == data:
            row = FixedMark.fix_index.row
            column = FixedMark.fix_index.column
            data[row][column] = data[row][column][0] if isinstance(data[row][column], list) else data[row][column]
            return data
        else:
            data_check = copy.deepcopy(data)


def check_inconsistency(data):
    for i in range(9):
        row = [elem for elem in data[i] if isinstance(elem, int)]
        count = Counter(row).most_common(1)[0][1] if row else 0
        if count > 1:
            return
    for j in range(9):
        column = [data[i][j] for i in range(9) if isinstance(data[i][j], int)]
        count = Counter(column).most_common(1)[0][1] if column else 0
        if count > 1:
            return
    blocks = [(0, 3), (3, 6), (6, 9)]
    for block_row in blocks:
        for block_column in blocks:
            block = [data[i][j] for i in range(*block_row) for j in range(*block_column) if isinstance(data[i][j], int)]
            count = Counter(block).most_common(1)[0][1] if block else 0
            if count > 1:
                return
    return True


def check_solved(data):
    for i in range(9):
        for j in range(9):
            if not isinstance(data[i][j], int):
                return False
    for i in range(9):
        if len(set(data[i])) != 9:
            return False
    for j in range(9):
        column = {data[i][j] for i in range(9)}
        if len(column) != 9:
            return False
    blocks = [(0, 3), (3, 6), (6, 9)]
    for block_row in blocks:
        for block_column in blocks:
            block = {data[i][j] for i in range(*block_row) for j in range(*block_column)}
            if len(block) != 9:
                return False
    return True


def fixing_recursion(data):
    if data == "exit" or check_solved(data):
        return data
    row, column, values = fix_mark(data)
    FixedMark.fix_index = index(row, column)
    print(f"Fixing object row: {row}, col: {column}, possible values: {values}")
    for value in values:
        data_with_fixed = copy.deepcopy(data)
        print(f"Try to fix {value}")
        data_with_fixed[row][column] = [value]
        data_with_fixed = clear_elements_cycle(data_with_fixed)
        if data_with_fixed and not check_solved(data_with_fixed):
            data_with_fixed = fixing_recursion(data_with_fixed)
        if data_with_fixed and data_with_fixed != "exit" and check_solved(data_with_fixed):
            return data_with_fixed
        if data_with_fixed == "exit" and DeletedMark.del_index != (row, column):
            return data_with_fixed

    if DeletedMark.del_index == (row, column):
        print("Violation of invariance")
        return "exit"
    return




def solve(filename):
    data = make_start_state(read_file(filename))
    data_copy = clear_elements_cycle(copy.deepcopy(data))
    while True:
        if not data_copy:
            return None
        elif data_copy == 'exit':
            return data_copy
        elif check_solved(data_copy):
            return data_copy
        data = copy.deepcopy(data_copy)
        data_copy = fixing_recursion(data_copy)
        if data == data_copy:
            break


def main():
    for i in range(1, 100):
        filename = f"sudoku_0{i}.json"
        if os.path.isfile(filename):
            print(f"\n\nFile {filename} exist")
            solved = solve(filename)
            if solved == "exit":
                continue
            elif solved:
                print_sudoku(solved)
            else:
                print("This sudoku does no have solution")


if __name__ == '__main__':
    main()
