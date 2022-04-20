import alg_variable as al


def test_check_unique():
    lines_row = [[0, 1, 0, 1, 1, 0], [1, 0, 0, 1, 0, 1],
                 [0, 1, 1, 0, 0, 1], [0, 1, 1, 0, 1, 0],
                 [1, 0, 0, 1, 1, 0], [1, 0, 1, 0, 0, 1]]

    lines_column = [[0, 1, 0, 0, 1, 1], [1, 0, 1, 1, 0, 0],
                    [0, 0, 1, 1, 0, 1], [1, 1, 0, 0, 1, 0],
                    [1, 0, 0, 1, 1, 0], [0, 1, 1, 0, 0, 1]]

    assert al.check_unique(lines_row)
    assert al.check_unique(lines_column)


def test_check_binary_eq():
    line = [0, 0, 0, 1, 1, 1]
    assert al.check_binary_eq(line)

    line = [1, 1, 1, 1, 0, 0]
    assert not al.check_binary_eq(line)

    line = [1, 1, None, None, None, 0]
    assert al.check_binary_eq(line)

    line = [1, 1, None, 1, None, 1]
    assert not al.check_binary_eq(line)


def test_check_binary_seq():
    line = [0, 0, 0, 1, 1, 1]
    assert not al.check_binary_seq(line)

    line = [1, 1, 1, 1, 0, 0]
    assert not al.check_binary_seq(line)

    line = [1, 1, None, None, None, 0]
    assert al.check_binary_seq(line)

    line = [1, 1, None, 1, None, 1]
    assert al.check_binary_seq(line)


def test_check_sudoku():
    line = [1, 2, 3, 4]
    assert al.check_sudoku(line)

    line = [4, 2, None, 4]
    assert not al.check_sudoku(line)

    line = [1, 2, 3, 4]
    assert al.check_sudoku(line)

