import alg_variable as al
import constants as con


def load_futoshiki(file_name, size) -> object:
    try:
        with open(file_name) as file:
            lines = file.readlines()
            data = al.Data(size, max_value=size, is_binary=False)
            field = dict()
            limits = []
            field_i, field_j = 0, 0
            for i, line in enumerate(lines):
                if i % 2 == 0:
                    field_j = 0
                    for j in range(size * 2 - 1):
                        elem = line[j]
                        if j % 2 == 0:
                            if elem != 'x':
                                field[(field_i, field_j)] = int(elem)
                        else:
                            if elem != '-':
                                if elem == '>':
                                    limits.append(al.SingleLimit([(field_i, field_j),
                                                                  (field_i, field_j + 1)],
                                                                 condition=con.GREATER_CON))
                                elif elem == '<':
                                    limits.append(al.SingleLimit([(field_i, field_j + 1),
                                                                  (field_i, field_j)],
                                                                 condition=con.GREATER_CON))
                            field_j += 1
                else:
                    field_i += 1
                    for j in range(size):
                        elem = line[j]
                        if elem != '-':
                            if elem == '>':
                                limits.append(al.SingleLimit([(field_i - 1, j),
                                                              (field_i, j)],
                                                             condition=con.GREATER_CON))
                            elif elem == '<':
                                limits.append(al.SingleLimit([(field_i, j),
                                                              (field_i - 1, j)],
                                                             condition=con.GREATER_CON))
            limits.extend(sudoku_conditions(size))
            return field, data, limits
    except IOError:
        print('File not found')
        return None


def load_binary(file_name):
    try:
        with open(file_name) as file:
            lines = file.readlines()
            size = count_size(lines)
            data = al.Data(size, is_binary=True)
            field = dict()
            for i, line in enumerate(lines):
                for j in range(size):
                    if line[j] != 'x':
                        field[(i, j)] = int(line[j])
            limits = binary_conditions(size)
            return field, data, limits
    except IOError:
        print('File not found')
        return None


def count_size(data):
    return len(data)


def sudoku_conditions(size):
    return get_limits(size, con.SUDOKU_CON)


def binary_conditions(size):
    limits = []
    limits.extend(unique_conditions(size))
    limits.extend(zero_one_seq_con(size))
    limits.extend(zero_one_equality_con(size))
    return limits


def unique_conditions(size):
    rows, columns = get_rows_columns(size)
    limits = [al.UniqueLimit(rows, condition=con.UNIQUE_CON), al.UniqueLimit(columns, condition=con.UNIQUE_CON)]
    return limits


def zero_one_equality_con(size):
    return get_limits(size, con.BINARY_SEQ_CON)


def zero_one_seq_con(size):
    return get_limits(size, con.BINARY_EQ_CON)


def get_limits(size, condition):
    limits = list()
    for i in range(size):
        rows = [(i, x) for x in range(size)]
        columns = [(x, i) for x in range(size)]
        limits.append(al.GroupLimit(rows, condition=condition))
        limits.append(al.GroupLimit(columns, condition=condition))

    return limits


def get_rows_columns(size):
    rows = list()
    columns = list()
    for i in range(size):
        rows.append([(i, x) for x in range(size)])
        columns.append([(x, i) for x in range(size)])
    return rows, columns
