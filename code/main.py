import data_loading as dl
import alg_variable as al
import constants as con
import search_with_relapses

if __name__ == '__main__':
    print('futoshiki_4x4')
    size = 4
    field_fut, data, limits_fut = dl.load_futoshiki('futoshiki_4x4', size)
    score, counter, _ = search_with_relapses.backtracking_time([], data, field_fut, limits_fut, 0)
    al.print_score(score, size)
    print(counter)

    print('futoshiki_4x4')
    size = 4
    field_fut, data, limits_fut = dl.load_futoshiki('futoshiki_4x4', size)
    score, counter, _ = search_with_relapses.forward_time([], data, field_fut, limits_fut, 0)
    al.print_score(score, size)
    print(counter)
    #
    print('futoshiki_5x5')
    size = 5
    field_fut, data, limits_fut = dl.load_futoshiki('futoshiki_5x5', size)
    score, counter, _ = search_with_relapses.backtracking_time([], data, field_fut, limits_fut, 0)
    al.print_score(score, size)
    print(counter)

    print('futoshiki_6x6')
    size = 6
    field_fut, data, limits_fut = dl.load_futoshiki('futoshiki_6x6', size)
    data.count_level(limits_fut)
    score, counter = search_with_relapses.forward_time([], data, field_fut, limits_fut, 0)
    print(counter)

    print('binary_6x6')
    field, data, limits = dl.load_binary('binary_6x6')
    score, counter = search_with_relapses.backtracking_time([], data, field, limits, 0)
    print(search_with_relapses.arc_constraints(data, field, limits))
    print(data.domains)
    al.print_score(score, 6)
    print(counter)

    print('binary_6x6')
    field, data, limits = dl.load_binary('binary_6x6')
    score, counter = search_with_relapses.forward_time([], data, field, limits, 0)
    al.print_score(score, 6)
    print(counter)

    # game_sizes = [4, 5, 6]
    # files = ['futoshiki_4x4', 'futoshiki_5x5', 'futoshiki_6x6']

    game_sizes = [6, 8, 10]
    files = ['binary_6x6', 'binary_8x8', 'binary_10x10']
    nodes_bt, nodes_fc, times_bt, times_fc = search_with_relapses.get_games_stats(files, game_sizes,
                                                                                  data_type=con.BINARY)
    print("Nodes")
    print(nodes_bt)
    print(nodes_fc)
    print("Time")
    print(times_bt)
    print(times_fc)
    search_with_relapses.make_chart(game_sizes, nodes_bt, nodes_fc, chart_type=con.NODES_TYPE)
    search_with_relapses.make_chart(game_sizes, times_bt, times_fc, chart_type=con.TIME_TYPE)
