import data_evaluation
import data_loading
import random_data
import constant

import algorithm as alg

if __name__ == '__main__':
    costs, material_flow = random_data.get_random_data(9, 10)
    population = random_data.get_random_layout(9, 3, 4)
    print(f"Random: {data_evaluation.evaluate_solution(costs, material_flow, population)}")

    pop = random_data.get_random_layout(9, 3, 3)
    costs = data_loading.load_data('easy_cost.json', constant.COST_RESOURCE)
    flow = data_loading.load_data('easy_flow.json', constant.FLOW_RESOURCE)
    dist = data_evaluation.get_distances(population)
    print(f"Easy: {data_evaluation.evaluate_solution(costs, flow, pop)}")

    pop = random_data.get_random_layout(12, 1, 12)
    costs = data_loading.load_data('flat_cost.json', constant.COST_RESOURCE)
    flow = data_loading.load_data('flat_flow.json', constant.FLOW_RESOURCE)
    print(f"Flat: {data_evaluation.evaluate_solution(costs, flow, pop)}")

    pop = random_data.get_random_layout(24, 5, 6)
    costs = data_loading.load_data('hard_cost.json', constant.COST_RESOURCE)
    flow = data_loading.load_data('hard_flow.json', constant.FLOW_RESOURCE)
    print(f"Hard: {data_evaluation.evaluate_solution(costs, flow, pop)}")

    pop_size = 200
    gen_num = 100
    crossover_prob = 0.3
    mutation_prob = 0.1
    tournament_size = 20

    pop = random_data.get_random_population(pop_size, 12, 1, 12)
    costs = data_loading.load_data('flat_cost.json', constant.COST_RESOURCE)
    flow = data_loading.load_data('flat_flow.json', constant.FLOW_RESOURCE)
    print("flat")
    alg.run_algorithm(tries_num=10, pop_size=pop_size, layout_size=12, x_size=1, y_size=12, generation_number=gen_num,
                      population=pop, costs=costs, flow=flow, tournament_size=tournament_size,
                      selection_op=constant.BOTH_CODE,
                      crossover_prob=crossover_prob, mutation_prob=mutation_prob)

    pop = random_data.get_random_population(pop_size, 9, 3, 3)
    costs = data_loading.load_data('easy_cost.json', constant.COST_RESOURCE)
    flow = data_loading.load_data('easy_flow.json', constant.FLOW_RESOURCE)

    print("easy")
    alg.run_algorithm(tries_num=10, pop_size=pop_size, layout_size=9, x_size=3, y_size=3, generation_number=gen_num,
                      population=pop, costs=costs, flow=flow, tournament_size=tournament_size,
                      selection_op=constant.BOTH_CODE,
                      crossover_prob=crossover_prob, mutation_prob=mutation_prob)

    pop = random_data.get_random_population(pop_size, 24, 5, 6)
    costs = data_loading.load_data('hard_cost.json', constant.COST_RESOURCE)
    flow = data_loading.load_data('hard_flow.json', constant.FLOW_RESOURCE)

    # print("hard")
    # alg.run_algorithm(tries_num=10, pop_size=pop_size, layout_size=24, x_size=5, y_size=6, generation_number=gen_num,
    #                   population=pop, costs=costs, flow=flow, tournament_size=tournament_size,
    #                   selection_op=constant.BOTH_CODE,
    #                   crossover_prob=crossover_prob, mutation_prob=mutation_prob)

    layout, score, best_worst_avg = alg.whole_algorithm(pop_size, 24, 5, 6, generation_number=gen_num,
                                                        population=pop,
                                                        costs=costs, flow=flow,
                                                        tournament_size=tournament_size,
                                                        selection_op=constant.TOURNAMENT_CODE,
                                                        bound=10,
                                                        crossover_prob=crossover_prob, mutation_prob=mutation_prob,
                                                        random=False)
    print(score)
    alg.make_chart(gen_num, best_worst_avg)
