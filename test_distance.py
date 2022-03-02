# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 20:33:36 2022

@author: JoelT
"""

import timeit


TM2 = "\t{0} time =>\n\t\t{1}\n\t{0} slowest =>\n\t\t{2}\n\t{0} fastest =>\n\t\t{3}\n\t{0} average =>\n\t\t{4}"


def test_time_diameter(iteration=10000):
    """
    Tests the speed of the function "diameters" over a given number of
    iterations (by default 10000) using the intended graph.

    Parameters
    ----------
    iteration : integer, optional
        Number of times the methods are tested to evaluate velocity. The
        default is 10000.

    Returns
    -------
    The total time of BFS function anf DFS function, the average for iteration
    of BFS funtion anf DFS function and the relation between the time of the
    BFS function anf DFS fucntion in a string. If it is > 1, BFS is slower than
    DFS and if it is < 1 BFS is faster than DFS.

    """
    setup_code = """
import lab1_JTS as lab1
G = lab1.build_lastfm_graph("lastfm_asia_target_test_reduced7.csv", "lastfm_asia_edges_test_reduced7.csv") """
    test_code = """
ls = lab1.diameters(G)"""

    times = timeit.repeat(setup=setup_code, stmt=test_code, number=iteration)
    max_times = max(times)
    min_times = min(times)
    times = sum(times)
    average = times / iteration
    return times, max_times, min_times, average


times = int(
    input(
        "How many times should the algorithms be tested to extract the average"
        + "running time: "
    )
)
tp = test_time_diameter(times)
print(TM2.format("diameters()", tp[0], tp[1], tp[2], tp[3]))
