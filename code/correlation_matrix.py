import pprint
import random


def get_random(high_bound):
    return random.randint(0, high_bound - 1)


def get_random_matrix(size, high_bound):
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        j = 0
        while j < i:
            matrix[i][j] = get_random(high_bound)
            j += 1
    return matrix


def get_default_matrix(size, default_value):
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        j = 0
        while j < i:
            matrix[i][j] = default_value
            j += 1
    return matrix


class CorrelationMatrix:
    def __init__(self, size, randomization=False, default_value=0, bound=1):
        self.size = size
        if randomization:
            self.matrix = get_random_matrix(size, bound)
        else:
            self.matrix = get_default_matrix(size, default_value)

    def get(self, x, y):
        if x < self.size and y < self.size:
            return self.matrix[x][y]
        return 0

    def set(self, x, y, value):
        if x < self.size and y < self.size:
            self.matrix[x][y] = value

    def print_matrix(self):
        pprint.PrettyPrinter().pprint(self.matrix)
