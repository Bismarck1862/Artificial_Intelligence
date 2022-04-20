import constant
import random_data
import data_evaluation
import data_loading
import selection_operators
import crossover_mutation_operators

from correlation_matrix import CorrelationMatrix as CorMat


def test_random_population():
    pop_size = 9
    x_size = 3
    y_size = 4
    layout = random_data.get_random_layout(pop_size, x_size, y_size)
    assert len(layout) == pop_size
    for elem in layout:
        assert elem[0] < x_size
        assert elem[1] < y_size


def test_random_data():
    pop_size = 9
    bound = 10
    costs, material_flow = random_data.get_random_data(pop_size, bound)
    assert costs.size == pop_size
    assert material_flow.size == pop_size
    for i in range(pop_size - 1):
        for j in range(pop_size - 1):
            assert costs.get(i, j) < bound
            assert material_flow.get(i, j) < bound


def test_get_distances():
    simple_layout = [[0, 1], [0, 0], [1, 1], [1, 0]]
    linear_layout = [[0, 90], [0, 1], [0, 2], [0, 3]]
    harder_layout = [[3, 0], [0, 4], [2, 2], [3, 3]]
    assert data_evaluation.get_distances(simple_layout).matrix \
           == [[0, 1, 1, 2], [1, 0, 2, 1], [1, 2, 0, 1], [2, 1, 1, 0]]
    assert data_evaluation.get_distances(linear_layout).matrix \
           == [[0, 89, 88, 87], [89, 0, 1, 2], [88, 1, 0, 1], [87, 2, 1, 0]]
    assert data_evaluation.get_distances(harder_layout).matrix \
           == [[0, 7, 3, 3], [7, 0, 4, 4], [3, 4, 0, 2], [3, 4, 2, 0]]


def test_solution_evaluation():
    simple_layout = [[0, 1], [0, 0], [1, 1], [1, 0]]
    linear_layout = [[0, 90], [0, 1], [0, 2], [0, 3]]
    harder_layout = [[3, 0], [0, 4], [2, 2], [3, 3]]
    costs_one = CorMat(4, default_value=1)
    flow_one = CorMat(4, default_value=1)
    assert data_evaluation.evaluate_solution(costs_one, flow_one, simple_layout) == 8
    assert data_evaluation.evaluate_solution(costs_one, flow_one, linear_layout) == 268
    assert data_evaluation.evaluate_solution(costs_one, flow_one, harder_layout) == 23


def test_score_save_load():
    pop = [[0, 2], [0, 4], [0, 5], [0, 9], [0, 11], [0, 3], [0, 8], [0, 0], [0, 6], [0, 7], [0, 10], [0, 1]]
    score = 10
    data_loading.save_score('test_score_1.json', pop, score)
    pop_loaded, score_loaded = data_loading.load_score('test_score_1.json')
    assert pop_loaded == pop
    assert score_loaded == score


def test_load_data():
    costs = data_loading.load_data('easy_cost.json', constant.COST_RESOURCE)
    assert costs.matrix == [[0, 1, 2, 3, 3, 4, 2, 6, 7], [0, 0, 12, 4, 7, 5, 8, 6, 5], [0, 0, 0, 5, 9, 1, 1, 1, 1],
                            [0, 0, 0, 0, 1, 1, 1, 4, 6], [0, 0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 1, 4, 6],
                            [0, 0, 0, 0, 0, 0, 0, 7, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    flow = data_loading.load_data('easy_flow.json', constant.FLOW_RESOURCE)
    assert flow.matrix == \
           [[0, 100, 3, 0, 6, 35, 190, 14, 12], [0, 0, 6, 8, 109, 78, 1, 1, 104], [0, 0, 0, 0, 0, 17, 100, 1, 31],
            [0, 0, 0, 0, 100, 1, 247, 178, 1], [0, 0, 0, 0, 0, 1, 10, 1, 79], [0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 12], [0, 0, 0, 0, 0, 0, 0, 0, 0]]


def test_selection_tournament():
    simple_layout_1 = [[0, 1], [0, 0], [1, 1], [1, 0]]
    simple_layout_2 = [[0, 0], [0, 1], [1, 1], [1, 0]]
    simple_layout_3 = [[1, 0], [0, 1], [1, 1], [0, 0]]
    costs = CorMat(4, default_value=1)
    costs.matrix = [[0, 1, 2, 3], [0, 0, 2, 3], [0, 0, 0, 1], [2, 0, 0, 0]]
    flow = CorMat(4, default_value=1)
    flow.matrix = [[0, 8, 9, 0], [1, 0, 5, 0], [3, 0, 0, 2], [2, 0, 5, 0]]
    pop = [simple_layout_1, simple_layout_2, simple_layout_3]
    scores, _ = data_evaluation.evaluate_population(costs, flow, pop)
    assert selection_operators.tournament(pop, scores, 3) == (simple_layout_3, 2)


def test_selection_roulette():
    simple_layout_1 = [[0, 1], [0, 0], [1, 1], [1, 0]]
    simple_layout_2 = [[0, 0], [0, 1], [1, 1], [1, 0]]
    simple_layout_3 = [[1, 0], [0, 1], [1, 1], [0, 0]]
    costs_one = CorMat(4, default_value=1)
    flow_one = CorMat(4, default_value=1)
    pop = [simple_layout_1, simple_layout_2, simple_layout_3]
    scores, _ = data_evaluation.evaluate_population(costs_one, flow_one, pop)
    assert selection_operators.roulette(pop, scores, rand_num=0.1) == (simple_layout_1, 0)


def test_mutation():
    simple_layout_1 = [[0, 1], [0, 0], [1, 1], [1, 0]]
    assert len(crossover_mutation_operators.mutation(simple_layout_1, 1)) == 4


def test_crossover():
    simple_layout_1 = [[0, 2], [0, 0], [1, 1], [1, 0]]
    simple_layout_2 = [[2, 0], [0, 1], [1, 1], [0, 0]]
    assert crossover_mutation_operators.crossover(simple_layout_1, simple_layout_2, 1, split_line_1=1, split_line_2=2) \
           == ([[0, 2], [0, 1], [1, 1], [1, 0]], [[2, 0], [0, 0], [1, 1], [0, 1]])


def test_crossover_copy():
    simple_layout_1 = [[0, 1], [0, 0], [1, 1], [1, 0]]
    simple_layout_2 = [[2, 0], [0, 1], [1, 1], [0, 0]]
    parent_1_copy, parent_2_copy = crossover_mutation_operators.crossover(simple_layout_1, simple_layout_2, 0)
    assert simple_layout_1 == parent_1_copy
    assert simple_layout_1 is not parent_1_copy
    assert simple_layout_2 == parent_2_copy
    assert simple_layout_2 is not parent_2_copy


def test_roulette_ref():
    simple_layout_1 = [[0, 1], [0, 0], [1, 1], [1, 0]]
    simple_layout_2 = [[2, 0], [0, 1], [1, 1], [0, 0]]
    pop = [simple_layout_1, simple_layout_2]
    costs_one = CorMat(4, default_value=1)
    flow_one = CorMat(4, default_value=1)
    scores, _ = data_evaluation.evaluate_population(costs_one, flow_one, pop)
    weights = selection_operators.weight_fun(scores)
    parent_1, _ = selection_operators.roulette(pop, weights, rand_num=0.1)

    assert simple_layout_1 == parent_1
    assert simple_layout_1 is parent_1

    parent_2, _ = selection_operators.roulette(pop, weights, rand_num=0.9)

    assert simple_layout_2 == parent_2
    assert simple_layout_2 is parent_2


def test_tournament_ref():
    simple_layout_1 = [[0, 1], [0, 0], [1, 1], [1, 0]]
    simple_layout_2 = [[2, 0], [0, 1], [1, 1], [0, 0]]
    pop = [simple_layout_1, simple_layout_2]
    costs_one = CorMat(4, default_value=1)
    flow_one = CorMat(4, default_value=1)
    scores, _ = data_evaluation.evaluate_population(costs_one, flow_one, pop)
    print(scores)
    parent_1, _ = selection_operators.tournament(pop, scores, tournament_size=2)

    assert simple_layout_1 == parent_1
    assert simple_layout_1 is parent_1

    parent_2, _ = selection_operators.tournament(pop, scores, tournament_size=1, random_numbers=[1])

    assert simple_layout_2 == parent_2
    assert simple_layout_2 is parent_2


def test_crossover_correctness_easy():
    simple_layout_1 = [[0, 1], [0, 0], [1, 1], [1, 0]]
    simple_layout_2 = [[2, 0], [0, 1], [1, 1], [0, 0]]
    parent_1_copy, parent_2_copy = crossover_mutation_operators.crossover(simple_layout_1, simple_layout_2, 0)

    for i in range(len(parent_1_copy)):
        j = i+1
        while j < len(parent_1_copy):
            assert parent_1_copy[i] != parent_1_copy[j]
            j += 1

    for i in range(len(parent_2_copy)):
        j = i+1
        while j < len(parent_2_copy):
            assert parent_2_copy[i] != parent_2_copy[j]
            j += 1


def test_crossover_correctness_medium():
    layout_1 = [(1, 0), (2, 1), (0, 1), (0, 2), (2, 2), (2, 0), (0, 0), (1, 2), (1, 1)]
    layout_2 = [(2, 1), (1, 2), (1, 0), (0, 0), (0, 2), (2, 2), (2, 0), (0, 1), (1, 1)]
    parent_1_copy, parent_2_copy = crossover_mutation_operators.crossover(layout_1, layout_2, 0)

    for i in range(len(parent_1_copy)):
        j = i + 1
        while j < len(parent_1_copy):
            assert parent_1_copy[i] != parent_1_copy[j]
            j += 1

    for i in range(len(parent_2_copy)):
        j = i + 1
        while j < len(parent_2_copy):
            assert parent_2_copy[i] != parent_2_copy[j]
            j += 1
