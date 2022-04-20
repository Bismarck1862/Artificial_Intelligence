import random
import sys
import constant as con


def select_parents(population, scores, weights, tournament_size=0, selection_op=con.ROULETTE_CODE):

    if selection_op == con.ROULETTE_CODE:
        parent_1, parent_1_id = roulette(population, weights)
        parent_2, parent_2_id = roulette(population, weights)
        while parent_1 == parent_2:
            parent_2, parent_2_id = roulette(population, weights)
    else:
        parent_1, parent_1_id = tournament(population, scores, tournament_size)
        parent_2, parent_2_id = tournament(population, scores, tournament_size)
        # while parent_1 == parent_2:
        #     parent_2, parent_2_id = tournament(population, scores, tournament_size)

    return parent_1, parent_1_id, parent_2, parent_2_id


def roulette(population, weights, rand_num=-1):
    if rand_num == -1:
        rand_num = random.random()
    prob = 0
    pop_elem_id = 0
    while prob < rand_num:
        prob = weights[pop_elem_id]
        pop_elem_id += 1

    chosen_elem = population[pop_elem_id-1]
    return chosen_elem, pop_elem_id-1


def tournament(population, scores, tournament_size, random_numbers=-1):
    pop_size = len(population)
    if tournament_size > pop_size:
        return 0
    else:
        if random_numbers == -1:
            rand_numbers = get_random_numbers(tournament_size, pop_size)
        else:
            rand_numbers = random_numbers

        best_score = sys.maxsize
        best_elem = []
        best_idx = 0
        for num in rand_numbers:
            elem = population[num]
            adapt = scores[num]
            if adapt < best_score:
                best_score = adapt
                best_elem = elem
                best_idx = num

        return best_elem, best_idx


def get_random_numbers(tournament_size, pop_size):
    rand_numbers = []
    for i in range(tournament_size):
        rand_num = random.randint(0, pop_size - 1)
        while rand_num in rand_numbers:
            rand_num = random.randint(0, pop_size - 1)
        rand_numbers.append(rand_num)

    return rand_numbers


def weight_fun(adaptations):
    weights = []
    prev_probability = 0
    for adapt in adaptations:
        prev_probability += 1/(adapt*adapt)
        weights.append(prev_probability)

    sum_w = weights[-1]
    for w in range(len(weights)):
        weights[w] = weights[w]/sum_w
    return weights
