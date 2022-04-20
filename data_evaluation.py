import math

from correlation_matrix import CorrelationMatrix as CorMat


def evaluate_population(costs, material_flow, population):
    scores = []
    best_id = 0
    best_score = math.inf
    for idx, layout in enumerate(population):
        score = evaluate_solution(costs, material_flow, layout)
        if score < best_score:
            best_score = score
            best_id = idx
        scores.append(score)

    return scores, best_id


def evaluate_solution(costs, material_flow, layout):
    layout_size = costs.size
    distance = get_distances(layout)
    score = 0
    for i in range(0, layout_size):
        for j in range(0, layout_size):
            if i != j:
                score += material_flow.get(i, j) * costs.get(i, j) * distance.get(i, j)
    # print(f"Score {layout}, {score}")
    return score


def get_distances(layout):
    pop_size = len(layout)
    distance = CorMat(pop_size)
    for i in range(0, pop_size):
        for j in range(0, pop_size):
            i_machine = layout[i]
            j_machine = layout[j]
            distance.set(i, j, abs(i_machine[0] - j_machine[0]) + abs(i_machine[1] - j_machine[1]))

    return distance
