import pprint
import copy
import random
from abc import ABC, abstractmethod


import constants as con
import data_loading as dl


def get_condition_symbol(condition):
    if condition == con.GREATER_CON:
        return '>'
    elif condition == con.UNIQUE_CON:
        return 'unq'
    elif condition == con.BINARY_SEQ_CON:
        return 'not000nor111'
    elif condition == con.SUDOKU_CON:
        return 'sudoku'
    elif condition == con.BINARY_EQ_CON:
        return '0eq1'


class AbsLimit(ABC):
    def __init__(self, var_list, condition):
        self.var_list = var_list
        self.condition = condition
        self.condition_symbol = get_condition_symbol(condition)

    @abstractmethod
    def satisfied(self, field) -> bool:
        pass

    def __str__(self):
        return f"{self.var_list}: {self.condition_symbol}"

    def __repr__(self):
        return f"{self.var_list}: {self.condition_symbol}"


class SingleLimit(AbsLimit):
    def __init__(self, var_list, condition):
        super().__init__(var_list, condition)

    def satisfied(self, field) -> bool:
        if self.condition == con.GREATER_CON:
            if self.var_list[0] in field.keys() and self.var_list[1] in field.keys():
                return field[self.var_list[0]] > field[self.var_list[1]]
            else:
                return True
        else:
            return False


class GroupLimit(AbsLimit):
    def __init__(self, var_list, condition):
        super().__init__(var_list, condition)

    def satisfied(self, field) -> bool:
        if self.condition == con.SUDOKU_CON:
            line = get_line(self.var_list, field, with_none=False)
            return check_sudoku(line)
        else:
            line = get_line(self.var_list, field)
            if self.condition == con.BINARY_SEQ_CON:
                return check_binary_seq(line)
            elif self.condition == con.BINARY_EQ_CON:
                return check_binary_eq(line)


def get_line(var_list, field, with_none=True):
    line = list()
    for x in var_list:
        if x in field.keys():
            line.append(field[x])
        elif with_none:
            line.append(None)
    return line


class UniqueLimit(AbsLimit):
    def __init__(self, var_list, condition):
        super().__init__(var_list, condition)

    def satisfied(self, field) -> bool:
        lines_row = []
        lines_column = []
        lines = list()
        for sub_list in self.var_list:
            lines.append(get_line(sub_list, field))
        return check_unique(lines)


def check_unique(lines):
    full_lines = []
    for line in lines:
        if None not in line:
            if line not in full_lines:
                full_lines.append(line)
            else:
                return False
    return True


def check_binary_seq(line):
    return not x_in_y([0, 0, 0], line) and not x_in_y([1, 1, 1], line)


def check_binary_eq(line):
    line_len = len(line)
    count_0, count_1 = count_elements(line)
    return count_1 <= line_len // 2 and count_0 <= line_len // 2


def count_elements(line):
    count_0 = 0
    count_1 = 0
    for elem in line:
        if elem is not None:
            if elem == 0:
                count_0 += 1
            elif elem == 1:
                count_1 += 1
    return count_0, count_1


def x_in_y(subseq, base) -> bool:
    sub_len = len(subseq)
    for i in range(len(base)):
        if base[i:i + sub_len] == subseq:
            return True
    return False


def check_sudoku(line):
    domain_list = list()
    for val in line:
        if val not in domain_list:
            domain_list.append(val)
        else:
            return False
    return True


def check_limits(limits, field, position):
    for idx, limit in enumerate(limits):
        if position in limit.var_list or limit.condition == con.UNIQUE_CON:
            if not limit.satisfied(field):
                return False
    return True


def get_default_matrix(size):
    matrix = dict()
    for i in range(size):
        for j in range(size):
            matrix[(i, j)] = None
    return matrix


def count_value_in_domains(value, dep_domains):
    counter = 0
    for dom in dep_domains:
        if value in dom:
            counter += 1
    return counter


class Data:
    def __init__(self, size, max_value=1, is_binary=True, variables=None, domains=None, levels=None, freedom=None):
        self.size = size
        if variables is None:
            self.variables = self.get_variables()
        else:
            self.variables = variables
        if domains is None:
            self.domains = self.get_domains(max_value, is_binary)
        else:
            self.domains = domains
        self.levels = levels
        self.freedom = freedom

    def __copy__(self):
        dom = self.domains.copy()
        free = None
        if self.freedom is not None:
            free = self.freedom.copy()
        return Data(self.size, variables=self.variables, domains=dom, levels=self.levels, freedom=free)

    def get_unassigned_elem(self, field):
        if self.levels is None:
            for var in self.variables:
                if var not in field:
                    return var
        else:
            for var in self.levels.keys():
                if var not in field:
                    return var

    def get_values(self, elem):
        if self.freedom is None:
            return self.domains[elem]
        else:
            return self.freedom[elem]

    def get_domains(self, max_value, is_binary):
        dom = dict()
        if is_binary:
            for key in self.variables:
                dom[key] = [x for x in range(2)]
        else:
            for key in self.variables:
                dom[key] = [x for x in range(1, max_value + 1)]

        return dom

    def get_variables(self):
        variables = list()
        for i in range(self.size):
            for j in range(self.size):
                variables.append((i, j))

        return variables

    def count_level(self, limits):
        levels = dict()
        for i in range(self.size):
            for j in range(self.size):
                levels[(i, j)] = 0
        for limit in limits:
            if limit.condition != con.UNIQUE_CON:
                for alg_var in limit.var_list:
                    levels[alg_var] += 1

        levels = dict(sorted(levels.items(), key=lambda item: item[1], reverse=True))
        self.levels = levels

    def count_freedom(self, limits):
        freedom = dict()
        for i in range(self.size):
            for j in range(self.size):
                freedom[(i, j)] = dict()

        for var in self.variables:
            dependents = get_dependents_vars(limits, var)
            dep_domains = list()
            for dep in dependents:
                dep_domains.append(self.domains[dep])
            local_free = freedom[var]
            for value in self.domains[var]:
                local_free[value] = count_value_in_domains(value, dep_domains)

            freedom[var] = dict(sorted(freedom[var].items(), key=lambda item: item[1], reverse=True))
            freedom[var] = list(freedom[var].keys())
        self.freedom = freedom

    def modify_domains(self, field, limits, position):
        pos_limits = get_limits(limits, position)
        for limit in pos_limits:
            for pos in limit.var_list:
                if pos not in field:
                    for value in self.domains[pos]:
                        local_field = field.copy()
                        local_field[pos] = value
                        if not limit.satisfied(local_field):
                            if value in self.domains[pos]:
                                if len(list(self.domains[pos])) >= 1:
                                    dom = self.domains[pos].copy()
                                    dom.remove(value)
                                    self.domains[pos] = dom
                                    if self.freedom is not None:
                                        free = self.freedom[pos].copy()
                                        free.remove(value)
                                        self.freedom[pos] = free
                                else:
                                    return False

        return True

    def revise(self, field, limits, position, counter):
        domain_changed = False
        for value in self.domains[position]:
            counter += 1
            local_field = field.copy()
            local_field[position] = value
            if not check_limits(limits, local_field, position):
                if len(list(self.domains[position])) >= 1:
                    dom = self.domains[position].copy()
                    dom.remove(value)
                    self.domains[position] = dom
                    domain_changed = True
                else:
                    return False, domain_changed, counter

        return True, domain_changed, counter

    def shuffle_domains(self):
        for var in self.variables:
            random.shuffle(self.domains[var])


def print_score(score, size):
    print(f"Number of scores: {len(score)}")
    for i in score:
        print_as_matrix(i, size)


def print_as_matrix(field, size):
    matrix = [[0 for x in range(size)] for y in range(size)]
    for key in field.keys():
        matrix[key[0]][key[1]] = field[key]

    pprint.pprint(matrix)


def get_dependents_vars(limits, position):
    dependent_vars = list()
    for limit in limits:
        if position in limit.var_list:
            for pos in limit.var_list:
                if pos not in dependent_vars and pos != position:
                    dependent_vars.append(pos)
    return dependent_vars


def get_limits(limits, position):
    pos_limits = list()
    for limit in limits:
        if position in limit.var_list:
            pos_limits.append(limit)
    return pos_limits
