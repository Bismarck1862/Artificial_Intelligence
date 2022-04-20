import random

from correlation_matrix import CorrelationMatrix as CorMat


def get_random_data(pop_size, high_bound):
    flow = CorMat(pop_size, randomization=True, bound=high_bound)
    cost = CorMat(pop_size, randomization=True, bound=high_bound)
    return cost, flow


def get_random_population(pop_size, layout_size, x_size, y_size):
    population = []
    i = 0
    while i < pop_size:
        layout = get_random_layout(layout_size, x_size, y_size)
        if layout not in population:
            population.append(layout)
            i += 1
    return population


def get_random_layout(layout_size, x_size, y_size):
    layout = []
    i = 0
    while i < layout_size:
        element = (get_random(x_size), get_random(y_size))
        if element not in layout:
            layout.append(element)
            i += 1
    return layout


def get_random(high_bound):
    return random.randint(0, high_bound-1)
