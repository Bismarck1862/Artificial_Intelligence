import json

import constant
from correlation_matrix import CorrelationMatrix as CorMat


def load_data(file_name, resource):
    try:
        with open(file_name) as json_file:
            data = json.load(json_file)
            pop_size = count_pop_size(data)
            costs = CorMat(pop_size)
            for elem in data:
                x = elem[constant.SOURCE]
                y = elem[constant.DESTINATION]
                cost = elem[resource]
                costs.set(x, y, cost)
            return costs
    except IOError:
        print('File not found')
        return CorMat(1)


def save_score(file_name, layout, score):
    score = json.dumps({constant.SCORE: score, constant.LAYOUT: layout})
    with open(file_name, 'w') as json_file:
        json_file.write(score)


def load_score(file_name):
    with open(file_name) as json_file:
        data = json.load(json_file)
        score = data[constant.SCORE]
        layout = data[constant.LAYOUT]
    return layout, score


def count_pop_size(data):
    max_value = 0
    for elem in data:
        x = elem[constant.SOURCE]
        y = elem[constant.DESTINATION]
        if x > max_value:
            max_value = x
        if y > max_value:
            max_value = y
    return max_value + 1
