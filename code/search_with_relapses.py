import time
import copy
import matplotlib.pyplot as plt
import constants as con
from alg_variable import check_limits
import data_loading as dl


def backtracking_search(score, data, field, limits, counter):
    if len(field) == pow(data.size, 2):
        score.append(field)

    unassigned_elem = data.get_unassigned_elem(field)
    if not unassigned_elem:
        return score, counter
    for value in data.get_values(unassigned_elem):
        counter += 1
        local_field = field.copy()
        local_field[unassigned_elem] = value
        if check_limits(limits, local_field, unassigned_elem):
            score, counter = backtracking_search(score, data, local_field, limits, counter)
    return score, counter


def backtracking_time(score, data, field, limits, counter):
    start_time = time.perf_counter()
    result, counter = backtracking_search(score, data, field, limits, counter)
    end_time = time.perf_counter()
    counted_time = end_time - start_time
    print(f"Time needed: {counted_time} seconds")
    return result, counter, counted_time


def backtracking_time_one_sol(data, field, limits, counter):
    start_time = time.perf_counter()
    result, counter = backtracking_search_one_sol(data, field, limits, counter)
    end_time = time.perf_counter()
    print(f"Time needed: {end_time - start_time} seconds")
    return result, counter


def backtracking_search_one_sol(data, field, limits, counter):
    if len(field) == pow(data.size, 2):
        return field, counter

    unassigned_elem = data.get_unassigned_elem(field)
    for value in data.get_values(unassigned_elem):
        counter += 1
        local_field = field.copy()
        local_field[unassigned_elem] = value
        if check_limits(limits, local_field, unassigned_elem):
            result, counter = backtracking_search_one_sol(data, local_field, limits, counter)
            if result is not None:
                return result, counter
    return None, counter


def forward_time(score, data, field, limits, counter):
    start_time = time.perf_counter()
    mod_start_domains(data, field, limits)
    result, counter = forward_search(score, data, field, limits, counter)
    end_time = time.perf_counter()
    counted_time = end_time - start_time
    print(f"Time needed: {counted_time} seconds")
    return result, counter, counted_time


def mod_start_domains(data, field, limits):
    for pos in field.keys():
        data.modify_domains(field, limits, pos)


def forward_search(score, data, field, limits, counter):
    if len(field) == pow(data.size, 2):
        score.append(field)

    unassigned_elem = data.get_unassigned_elem(field)
    if not unassigned_elem:
        return score, counter
    for value in data.get_values(unassigned_elem):
        counter += 1
        local_field = field.copy()
        local_field[unassigned_elem] = value
        local_data = copy.copy(data)
        all_not_empty = local_data.modify_domains(local_field, limits, unassigned_elem)
        if all_not_empty:
            score, counter = forward_search(score, local_data, local_field, limits, counter)
    return score, counter


def arc_constraints(data, field, limits, counter):
    queue = dict()
    for pos in data.variables:
        queue[pos] = 1

    while len(queue) > 0:
        position = list(queue.keys())[0]
        queue.pop(position)
        not_empty, domain_changed, dom_size = data.revise(field, limits, position, 0)
        counter += dom_size
        if not not_empty:
            return False, counter
        # if len(data.domains[position]) == 1:
        #     field[position] = data.domains[position][0]
    return True, counter


def make_chart(games_sizes, y_axis_bt, y_axis_fc, chart_type=con.NODES_TYPE):
    plt.xticks(games_sizes)
    plt.plot(games_sizes, y_axis_bt, 'b', label='BT')
    plt.plot(games_sizes, y_axis_fc, 'g', label='FC')

    if chart_type == con.NODES_TYPE:
        plt.title('Nodes visits')
        plt.ylabel('Nodes')
    elif chart_type == con.TIME_TYPE:
        plt.title('Time duration')
        plt.ylabel('Seconds')
    plt.xlabel('Game size')

    plt.legend()
    plt.show()


def get_games_stats(files, sizes, data_type=con.FUTOSHIKI):
    nodes_visited_bt = []
    times_bt = []
    nodes_visited_fc = []
    times_fc = []
    for idx, file in enumerate(files):
        size = sizes[idx]
        if data_type == con.FUTOSHIKI:
            field, data, limits = dl.load_futoshiki(file, size)
        elif data_type == con.BINARY:
            field, data, limits = dl.load_binary(file)
        # data.count_level(limits)
        # _, counter = arc_constraints(data, field, limits, 0)
        # print(counter)
        # data.count_freedom(limits)
        score, counter, counted_time = backtracking_time([], data, field, limits, 0)
        nodes_visited_bt.append(counter)
        times_bt.append(counted_time)

        if data_type == con.FUTOSHIKI:
            field, data, limits = dl.load_futoshiki(file, size)
        elif data_type == con.BINARY:
            field, data, limits = dl.load_binary(file)
        # data.count_level(limits)
        # _, counter = arc_constraints(data, field, limits, 0)
        # print(counter)
        # data.count_freedom(limits)
        score, counter, counted_time = forward_time([], data, field, limits, 0)
        nodes_visited_fc.append(counter)
        times_fc.append(counted_time)

    return nodes_visited_bt, nodes_visited_fc, times_bt, times_fc
