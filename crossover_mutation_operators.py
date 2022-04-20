import copy
import random


def crossover(parent_1, parent_2, probability, split_line_1=-1, split_line_2=-1):
    if is_crossover(probability):
        return make_crossover(parent_1, parent_2, split_line_1, split_line_2)
    else:
        return copy.deepcopy(parent_1), copy.deepcopy(parent_2)


def make_crossover(parent_1, parent_2, split_line_1, split_line_2):
    layout_size = len(parent_1)
    if split_line_1 == -1:
        split_line_1 = random.randint(1, len(parent_1) - 1)
    if split_line_2 == -1:
        split_line_2 = random.randint(1,  len(parent_1) - 1)
        while split_line_2 == split_line_1:
            split_line_2 = random.randint(1,  len(parent_1) - 1)

    split_line_1, split_line_2 = swap(split_line_1, split_line_2)

    child_1 = [0 for _ in range(layout_size)]
    child_2 = [0 for _ in range(layout_size)]
    child_1_parent = parent_2[split_line_1:split_line_2]
    child_2_parent = parent_1[split_line_1:split_line_2]

    # from parent
    for i in range(split_line_1, split_line_2):
        child_1[i] = child_1_parent[i - split_line_1]
        child_2[i] = child_2_parent[i - split_line_1]

    # from parent, without conflict
    for i in range(layout_size):
        if i < split_line_1 or i >= split_line_2:
            elem_1 = parent_1[i]
            elem_2 = parent_2[i]
            if elem_1 not in child_1_parent:
                child_1[i] = elem_1
            else:
                child_1[i] = None

            if elem_2 not in child_2_parent:
                child_2[i] = elem_2
            else:
                child_2[i] = None

    # resolving conflicts
    for i in range(layout_size):
        if child_1[i] is None:
            for j in range(layout_size):
                if parent_1[j] not in child_1:
                    child_1[i] = parent_1[j]

        if child_2[i] is None:
            for j in range(layout_size):
                if parent_2[j] not in child_2:
                    child_2[i] = parent_2[j]

    return child_1, child_2


def swap(split_line_1, split_line_2):
    if split_line_1 > split_line_2:
        return split_line_2, split_line_1
    else:
        return split_line_1, split_line_2


def mutation(child, probability):
    prob = random.random()
    if prob <= probability:
        child = make_mutation(child)
    return child


def make_mutation(child):
    gen_1 = random.randint(0, len(child) - 1)
    gen_2 = random.randint(0, len(child) - 1)
    while gen_1 == gen_2:
        gen_2 = random.randint(0, len(child) - 1)
    tmp = child[gen_1]
    child[gen_1] = child[gen_2]
    child[gen_2] = tmp
    return child


def is_crossover(probability):
    prob = random.random()
    return prob <= probability
