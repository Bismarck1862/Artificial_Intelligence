import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp

import data_evaluation
import random_data as rnd
import selection_operators
import crossover_mutation_operators as cm
import constant as con


def whole_algorithm(pop_size, layout_size, x_size, y_size, generation_number,
                    population, costs, flow, selection_op, tournament_size, bound, crossover_prob, mutation_prob,
                    random):
    # collecting data
    if population == -1:
        population = rnd.get_random_population(pop_size, layout_size, x_size, y_size)
    if costs == -1 or flow == -1:
        costs, flow = rnd.get_random_data(layout_size, bound)

    # counting scores
    scores, best_id = data_evaluation.evaluate_population(costs, flow, population)
    best_solution = population[best_id]
    best_score = scores[best_id]
    best, worst, avg = get_best_worst_avg(scores)
    bests = [best]
    worsts = [worst]
    avgs = [avg]

    # main loop
    i = 0
    while i < generation_number:
        next_population = []
        next_scores = []
        weights = selection_operators.weight_fun(scores)
        # selection
        while len(next_population) != pop_size:
            if not random:
                parent_1, parent_1_id, parent_2, parent_2_id = \
                    selection_operators.select_parents(population, scores, weights, tournament_size, selection_op)

                # crossover
                child_1, child_2 = cm.crossover(parent_1, parent_2, crossover_prob)

                # mutation
                child_1 = cm.mutation(child_1, mutation_prob)
                child_2 = cm.mutation(child_2, mutation_prob)
            else:
                child_1 = rnd.get_random_layout(layout_size, x_size, y_size)
                child_2 = rnd.get_random_layout(layout_size, x_size, y_size)

            # counting and checking scores of children
            child_1_score, is_best = check_child(best_score, child_1, costs, flow)
            if is_best:
                best_score = child_1_score
                best_solution = child_1

            child_2_score, is_best = check_child(best_score, child_2, costs, flow)
            if is_best:
                best_score = child_2_score
                best_solution = child_2

            # writing children to the population
            next_population.append(child_1)
            next_scores.append(child_1_score)

            next_population.append(child_2)
            next_scores.append(child_2_score)

        population = next_population
        best, worst, avg = get_best_worst_avg(scores)
        bests.append(best)
        worsts.append(worst)
        avgs.append(avg)
        scores = next_scores
        i += 1

    return best_solution, best_score, (bests, worsts, avgs)


def whole_algorithm_parallel(pop_size, layout_size, x_size, y_size, generation_number,
                             population, costs, flow, selection_op, tournament_size, bound, crossover_prob,
                             mutation_prob, random):
    _, best_score, _ = whole_algorithm(pop_size, layout_size, x_size, y_size,
                                                                       generation_number,
                                                                       population, costs, flow, selection_op,
                                                                       tournament_size, bound, crossover_prob,
                                                                       mutation_prob, random)
    return best_score


def check_child(best_score, child, costs, flow):
    child_score = data_evaluation.evaluate_solution(costs, flow, child)
    if best_score > child_score:
        return child_score, True
    else:
        return child_score, False


def run_algorithm_many_times(tries_num, pop_size, layout_size, x_size, y_size, generation_number,
                             population=-1, costs=-1, flow=-1,
                             selection_op=con.ROULETTE_CODE, tournament_size=0, bound=10, crossover_prob=0.5,
                             mutation_prob=0.5,
                             random=False):
    pool = mp.Pool(processes=tries_num)
    if not random:
        scores = [pool.apply_async(whole_algorithm_parallel,
                                   args=(pop_size, layout_size, x_size, y_size,
                                         generation_number,
                                         population, costs, flow,
                                         selection_op,
                                         tournament_size,
                                         bound,
                                         crossover_prob,
                                         mutation_prob, False)) for _ in range(tries_num)]
    else:
        scores = [pool.apply_async(whole_algorithm_parallel,
                                   args=(pop_size, layout_size, x_size, y_size,
                                         generation_number,
                                         population, costs, flow,
                                         selection_op,
                                         tournament_size,
                                         bound,
                                         crossover_prob,
                                         mutation_prob, True)) for _ in range(tries_num)]
    return [score.get() for score in scores]


def run_algorithm(tries_num, pop_size, layout_size, x_size, y_size, generation_number,
                  population=-1, costs=-1, flow=-1,
                  selection_op=con.ROULETTE_CODE, tournament_size=0, bound=10, crossover_prob=0.5, mutation_prob=0.5):
    if selection_op == con.BOTH_CODE:
        scores = run_algorithm_many_times(tries_num, pop_size, layout_size, x_size, y_size,
                                          generation_number=generation_number,
                                          population=population, costs=costs, flow=flow,
                                          selection_op=con.ROULETTE_CODE,
                                          tournament_size=tournament_size,
                                          bound=bound,
                                          crossover_prob=crossover_prob,
                                          mutation_prob=mutation_prob,
                                          random=False)

        std, avg, sc_max, sc_min = analise_scores(scores)
        print("genetic roulette")
        print(f"Standard deviation is {std}")
        print(f"Average is {avg}")
        print(f"Worst score: {sc_max}")
        print(f"Best score: {sc_min}")

        scores = run_algorithm_many_times(tries_num, pop_size, layout_size, x_size, y_size,
                                          generation_number=generation_number,
                                          population=population, costs=costs, flow=flow,
                                          selection_op=con.TOURNAMENT_CODE,
                                          tournament_size=tournament_size,
                                          bound=bound,
                                          crossover_prob=crossover_prob,
                                          mutation_prob=mutation_prob,
                                          random=False)

        std, avg, sc_max, sc_min = analise_scores(scores)
        print("genetic tournament")
        print(f"Standard deviation is {std}")
        print(f"Average is {avg}")
        print(f"Worst score: {sc_max}")
        print(f"Best score: {sc_min}")

    else:
        scores = run_algorithm_many_times(tries_num, pop_size, layout_size, x_size, y_size,
                                          generation_number=generation_number,
                                          population=population, costs=costs, flow=flow,
                                          selection_op=selection_op,
                                          tournament_size=tournament_size,
                                          bound=bound,
                                          crossover_prob=crossover_prob,
                                          mutation_prob=mutation_prob,
                                          random=False)

        std, avg, sc_max, sc_min = analise_scores(scores)
        print("genetic")
        print(f"Standard deviation is {std}")
        print(f"Average is {avg}")
        print(f"Worst score: {sc_max}")
        print(f"Best score: {sc_min}")

        print("random")
        scores = run_algorithm_many_times(tries_num, pop_size, layout_size, x_size, y_size,
                                          generation_number=generation_number,
                                          population=population, costs=costs, flow=flow,
                                          selection_op=selection_op,
                                          tournament_size=tournament_size,
                                          bound=bound,
                                          crossover_prob=crossover_prob,
                                          mutation_prob=mutation_prob,
                                          random=True)

        std, avg, sc_max, sc_min = analise_scores(scores)
        print(f"Standard deviation is {std}")
        print(f"Average is {avg}")
        print(f"Worst score: {sc_max}")
        print(f"Best score: {sc_min}")


def analise_scores(scores):
    return np.std(scores), np.average(scores), np.max(scores), np.min(scores)


def get_best_worst_avg(scores):
    return np.min(scores), np.max(scores), np.average(scores)


def make_chart(gen_num, best_worst_avg):
    generations = [i for i in range(gen_num + 1)]
    plt.plot(generations, best_worst_avg[0], 'b', label='best')
    plt.plot(generations, best_worst_avg[1], 'r', label='worst')
    plt.plot(generations, best_worst_avg[2], 'g', label='avg')

    plt.title('Best/Worst/Avg Vs Generation')
    plt.xlabel('Generation')
    plt.ylabel('Best/Worst/Avg')

    plt.legend()
    plt.show()


def make_scores_chart(gen_num, scores):
    generations = [i for i in range(gen_num)]
    plt.plot(generations, scores)
    plt.title('A')
    plt.xlabel('B')
    plt.ylabel('C')
    plt.show()
