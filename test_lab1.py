# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 09:13:14 2022

@author: Joel Tapia Salvador (1638962)
"""
import random
import timeit
import networkx as nx
import lab1


# Tuple with the seeds for the random module of the arbitrary generated values
# for the 9 test with different values.
SEEDS = (
    "93748347651",
    "47586937894",
    "38582562745",
    "63498098389",
    "84560368491",
    "79364783672",
    "28075067910",
    "58495397832",
    "17836548901",
)
# Tuple with the ranges for the random module to generate the values coinciding
# with those in the test files.
RANGES = (
    (20, 11, 9),
    (20, 11, 9),
    (20, 11, 9),
    (20, 11, 9),
    (20, 11, 9),
    (20, 11, 9),
    (100, 35, 22),
    (3, 100, 13),
    (1000, 16, 16),
)
# Part of the names of the arbitrary created-files that contains the nodes.
NODES_FILE = "lastfm_asia_target_test_reduced"
# Part of the names of the arbitrary created-files that contains the edges.
EDGE_FILES = "lastfm_asia_edges_test_reduced"
# Tuple with the last part of the names of the arbitrary created_files.
NAMES = ("1", "2", "3", "4", "5", "6", "7", "8", "9")
# File type.
CSV = ".csv"
# Standaard messages of the main program.
TESTING = 'Testing "{}" function: '
PSD = "\tPassed => "
TM = (
    "\tBFS time =>\n\t\t{0}\n\tBFS average =>\n\t\t{2}\n\t"
    + "DFS time =>\n\t\t{1}\n\tDFS average =>\n\t\t{3}\n\t"
    + "BFS / DFS relation =>\n\t\t{4}"
)
DELIMITER = "--------------------------------------------------------------"


def test_build_lastfm_graph(seed_i, range_t, name_i):
    """
    Tests the function "test_build_lastfm_graph" from the module "lab1".

    Parameters
    ----------
    seed_i : string
        Seed used by random module to generate the arbitrary list to test the
        function, to ensure that the result are the same as the files.
    range_t : tuple
        3 element long tuple that indicated the limits of range module for
        every seed, to ensure that the result are the same as the files.
    name_i : string
        Part of the name of the files that coincide with the given seed.

    Returns
    -------
    bool
        The test is passed without an AssertionError generated.
    expected_graph : networkx graph type
        Is the graph used to compare the the result of the functions tested.
    obtained_graph : networkx graph type
        Is the graph were the functions tested are aplied.

    """
    # Sets the seed to generate predifined random lists to mach the data in
    # test files and verify the methods with smaller arbitrary data sets.
    random.seed(seed_i)
    # Generates the arbitrary graph using list generated with the seed.
    expected_graph = nx.Graph()
    expected_nodes = [
        (str(node), {"target": str(random.randint(0, range_t[0]))})
        for node in range(range_t[1])
    ]
    expected_edges = [
        (str(node), str(random.randint(0, range_t[1] - 1)))
        for node in range(range_t[2])
    ]
    expected_graph.add_nodes_from(expected_nodes)
    expected_graph.add_edges_from(expected_edges)
    # Gets the values of the properties of the expected graph using networkx
    # build in methods anf functions.
    expected_number_of_nodes = expected_graph.number_of_nodes()
    expected_number_of_edges = expected_graph.number_of_edges()
    expected_degree = expected_graph.degree()
    expected_density = nx.density(expected_graph)
    # Generates de graph using the function tested and the test files.
    obtained_graph = lab1.build_lastfm_graph(
        NODES_FILE + name_i + CSV, EDGE_FILES + name_i + CSV
    )
    # Gets the values of the properties of the test graph using networkx
    # build in methods and functions.
    obtained_number_of_nodes = obtained_graph.number_of_nodes()
    obtained_number_of_edges = obtained_graph.number_of_edges()
    obtained_degree = obtained_graph.degree()
    obtained_density = nx.density(obtained_graph)
    # Error message in case conditions are not achived.
    t_a = (
        "\n\t\tObtained number of nodes => {0}"
        + "\n\t\tObtained numbes of edges => {1}"
    )
    t_a = t_a.format(obtained_number_of_nodes, obtained_number_of_edges)
    t_b = "\n\t\tObtained degrees => " + str(obtained_degree())
    t_c = ("\n\t\tObtained density => ") + str(obtained_density)
    # Verifies number of nodes.
    assert obtained_number_of_nodes == expected_number_of_nodes, (
        "Number of nodes doesn't match with expected result." + t_a
    )
    # Verifies number of edges.
    assert obtained_number_of_edges == expected_number_of_edges, (
        "Number of edges doesn't match with expected result." + t_a
    )
    # Verifies degrees.
    for node, deg in expected_degree:
        assert deg == obtained_degree[node], (
            "Degrees doesn't match with expected result." + t_b
        )
    # Verifies density.
    assert obtained_density == expected_density, (
        "Density doesn't match with expected result." + t_c
    )
    return True, expected_graph, obtained_graph


def test_how_many_components_bfs(expected_graph, obtained_graph):
    """
    Tests the function "how_many_components_BFS" from the module "lab1".

    Parameters
    ----------
    expected_graph : networkx graph type
        Is the graph used to compare the the result of the functions tested.
    obtained_graph : networkx graph type
        Is the graph were the functions tested are aplied.

    Returns
    -------
    bool
        The test is passed without an AssertionError generated.

    """
    # Using netwotkx build in function "connected_components" generates a
    # sorted (from most length to lest) list of sorted (from lest aplphabetical
    # to most) list of components with the strings of the names of the nodes in
    # said component.
    expected_components = sorted(
        [sorted(list(i)) for i in nx.connected_components(expected_graph)],
        key=len,
        reverse=True,
    )  # = [['1', '10', '2', '4', '5', '7', '8'], ['0', '3', '6', '9']]
    # Using networkx build in fuction "number_connected_components" counts the
    # number of components of the expected graph.
    expected_number_of_components = nx.number_connected_components(
        expected_graph
    )  # = 2
    # Using the function "how_many_components_BFS" from "lab1" generates a
    # sorted (from most length to lest) list of sorted (from lest aplphabetical
    # to most) list of components with the strings of the names of the nodes in
    # said component.
    obtained_components = sorted(
        [sorted(i) for i in lab1.how_many_components_BFS(obtained_graph)],
        key=len,
        reverse=True,
    )
    # Measures the leng of the list obtained by the function
    # "how_many_components_BFS" from "lab1".
    obtained_number_of_components = len(obtained_components)
    # Verifies the number of components.
    assert expected_number_of_components == obtained_number_of_components, (
        "Number of components doesn't match with expected result."
        + "\n\t\tObtained number of components => "
        + str(obtained_number_of_components)
    )
    # Verifies that the components are the same (hence why we sorted them
    # previosly).
    assert expected_components == obtained_components, (
        "Components doesn't match with expected result."
        + "\n\t\tObtained components => "
        + str(obtained_components)
    )
    return True


def test_how_many_components_dfs(expected_graph, obtained_graph):
    """
    Tests the function "how_many_components_DFS" from the module "lab1".

    Parameters
    ----------
    expected_graph : networkx graph type
        Is the graph used to compare the the result of the functions tested.
    obtained_graph : networkx graph type
        Is the graph were the functions tested are aplied.

    Returns
    -------
    bool
        The test is passed without an AssertionError generated.

    """
    # Using netwotkx build in function "connected_components" generates a
    # sorted (from most length to lest) list of sorted (from lest aplphabetical
    # to most) list of components with the strings of the names of the nodes in
    # said component.
    expected_components = sorted(
        [sorted(list(i)) for i in nx.connected_components(expected_graph)],
        key=len,
        reverse=True,
    )  # = [['1', '10', '2', '4', '5', '7', '8'], ['0', '3', '6', '9']]
    # Using networkx build in fuction "number_connected_components" counts the
    # number of components of the expected graph.
    expected_number_of_components = nx.number_connected_components(
        expected_graph
    )  # = 2
    # Using the function "how_many_components_DFS" from "lab1" generates a
    # sorted (from most length to lest) list of sorted (from lest aplphabetical
    # to most) list of components with the strings of the names of the nodes in
    # said component.
    obtained_components = sorted(
        [sorted(i) for i in lab1.how_many_components_DFS(obtained_graph)],
        key=len,
        reverse=True,
    )
    # Measures the leng of the list obtained by the function
    # "how_many_components_DFS" from "lab1".
    obtained_number_of_components = len(obtained_components)
    # Verifies the number of components.
    assert expected_number_of_components == obtained_number_of_components, (
        "Number of components doesn't match with expected result."
        + "\n\t\tObtained number of components => "
        + str(obtained_number_of_components)
    )
    # Verifies that the components are the same (hence why we sorted them
    # previosly).
    assert expected_components == obtained_components, (
        "Components doesn't match with expected result."
        + "\n\t\tObtained components => "
        + str(obtained_components)
    )
    return True


def test_faster_reduced(name_i, iteration=10000):
    """
    Tests the speed of the functions BFS and DFS over a given number of
    iterations (by default 10000) using the reduced-test-version graph.

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
    setup_code = (
        """
import lab1
NODES_FILE = "lastfm_asia_target_test_reduced"""
        + name_i
        + """.csv"
EDGE_FILES = "lastfm_asia_edges_test_reduced"""
        + name_i
        + """.csv"
G = lab1.build_lastfm_graph(NODES_FILE, EDGE_FILES)"""
    )
    test_code1 = """
ls = lab1.how_many_components_BFS(G)"""
    test_code2 = """
ls = lab1.how_many_components_DFS(G)"""
    times1 = timeit.repeat(setup=setup_code, stmt=test_code1, number=iteration)
    times2 = timeit.repeat(setup=setup_code, stmt=test_code2, number=iteration)
    times1 = sum(times1)
    times2 = sum(times2)
    proportion = times1 / times2
    average1 = times1 / iteration
    average2 = times2 / iteration
    return times1, times2, average1, average2, proportion


def test_faster_extended(iteration=10000):
    """
    Tests the speed of the functions BFS and DFS over a given number of
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
import lab1
G = lab1.build_lastfm_graph()"""
    test_code1 = """
ls = lab1.how_many_components_BFS(G)"""
    test_code2 = """
ls = lab1.how_many_components_DFS(G)"""
    times1 = timeit.repeat(setup=setup_code, stmt=test_code1, number=iteration)
    times2 = timeit.repeat(setup=setup_code, stmt=test_code2, number=iteration)
    times1 = sum(times1)
    times2 = sum(times2)
    proportion = times1 / times2
    average1 = times1 / iteration
    average2 = times2 / iteration
    return times1, times2, average1, average2, proportion


def test_how_many_degrees(expected_graph, obtained_graph):
    """
    Tests the function "how_many_degrees" from the module "lab1" with all pair
    of nodes of the given graph.

    Parameters
    ----------
    expected_graph : networkx graph type
        Is the graph used to compare the the result of the functions tested.
    obtained_graph : networkx graph type
        Is the graph were the functions tested are aplied.

    Returns
    -------
    bool
        The test is passed without an AssertionError generated.

    """
    for node_a in list(expected_graph.nodes):
        for node_b in list(expected_graph.nodes):
            try:
                obtained_path = lab1.how_many_degrees(obtained_graph, node_a, node_b)
                expected_path = nx.algorithms.shortest_paths.generic.shortest_path(
                    expected_graph, node_a, node_b
                )
                expected_length_path = len(expected_path)
                obtained_length_path = len(obtained_path)
                assert expected_length_path == obtained_length_path, (
                    "Length of path doesn't match with expected result."
                    + "\n\t\tObtained length of path => "
                    + str(obtained_length_path)
                )
                assert expected_path == obtained_path, (
                    "Path doesn't match with expected result."
                    + "\n\t\tObtained path => "
                    + str(obtained_path)
                )
            except nx.NetworkXNoPath:
                assert obtained_path is None, (
                    "Path not expected and path is returned."
                    + "\n\t\tObtained path => "
                    + str(obtained_path)
                )
    return True


def test_diameters(expected_graph, obtained_graph):
    """


    Returns
    -------
    bool
        DESCRIPTION.

    """
    try:
        obtained_diameter = lab1.diameters(obtained_graph)
        expected_diameter = nx.algorithms.distance_measures.diameter(expected_graph)
        assert expected_diameter == obtained_diameter, (
            "Diameter doesn't match with expected result"
            + "\n\t\tObtained diameter => "
            + str(obtained_diameter)
        )
    except nx.NetworkXError:
        assert obtained_diameter is None, (
            "Diameter doesn't match with expected result"
            + "\n\t\tObtained diameter => "
            + str(obtained_diameter)
        )
    return True


# MAIN
"""Executes the following functions given 9 diferent files and seeds and a
BFS/DFS comparation with the lastfm graph. In total 10 files and 55 tests"""
# Variable used to store tha inforamtion about the tests.
TESTS_PASSED = 0
FILES_COMPLETED = 0
faster = []
# Bucle used to executed the test with each test-file and test-seed.
for seeds, ranges, names in zip(SEEDS, RANGES, NAMES):
    # Error control, if an assert error is raised, catch the error, prints the
    # reason and allows th test to be executed with the next file.
    try:
        print(DELIMITER)
        print("TESTING FILE: " + names)
        # Test 1.
        print(TESTING.format("build_lastfm_graph()"))
        print(PSD)
        pas, expected_graph_ex, obtained_graph_ex = test_build_lastfm_graph(
            seeds, ranges, names
        )
        print("\t\t" + str(pas))
        TESTS_PASSED += 1
        # Test 2.
        print(TESTING.format("how_many_components_BFS()"))
        print(PSD)
        print(
            "\t\t"
            + str(test_how_many_components_bfs(expected_graph_ex, obtained_graph_ex))
        )
        TESTS_PASSED += 1
        # Test 3.
        print(TESTING.format("how_many_components_DFS()"))
        print(PSD)
        print(
            "\t\t"
            + str(test_how_many_components_dfs(expected_graph_ex, obtained_graph_ex))
        )
        TESTS_PASSED += 1
        # Test 4.
        print("Testing relation time of BFS/DFS using test graph:")
        tp = test_faster_reduced(names, 100)
        print(TM.format(tp[0], tp[1], tp[2], tp[3], tp[4]))
        if tp[4] < 1:
            faster.append("BFS")
        elif tp[4] > 1:
            faster.append("DFS")
        else:
            faster.append("TIE")
        TESTS_PASSED += 1
        # Test 5.
        print(TESTING.format("how_many_degrees(G, a, b)"))
        print(PSD)
        print("\t\t" + str(test_how_many_degrees(expected_graph_ex, obtained_graph_ex)))
        TESTS_PASSED += 1
        # Test 6.
        print(TESTING.format("diameters()"))
        print(PSD)
        print("\t\t" + str(test_diameters(expected_graph_ex, obtained_graph_ex)))
        TESTS_PASSED += 1

        FILES_COMPLETED += 1
    except AssertionError as msg:
        print("\t\tFalse: " + str(msg))
    except TypeError as msg:
        print("\t\tFalse: " + str(msg))
    finally:
        print(DELIMITER)
# If all the BFS/DFS comparation of the test files are executed correctly
# executes the BFS/DFS comparation with the lastfm graph.
# if len(faster) == 9:
if FILES_COMPLETED == 9:
    print(DELIMITER)
    print("Testing relation time of BFS/DFS using intended graph:")
    tp = test_faster_extended(100)
    print(TM.format(tp[0], tp[1], tp[2], tp[3], tp[4]))
    if tp[4] < 1:
        faster.append("BFS")
    elif tp[4] > 1:
        faster.append("DFS")
    else:
        faster.append("TIE")
    TESTS_PASSED += 1
    FILES_COMPLETED += 1
    print(DELIMITER)
# Prints the results of the tests.
print("Files completed: " + str(FILES_COMPLETED) + "/10")
print("Tests passed: " + str(TESTS_PASSED) + "/55")
print("Tests faster with BFS: " + str(faster.count("BFS")) + "/" + str(len(faster)))
print("Tests faster with DFS: " + str(faster.count("DFS")) + "/" + str(len(faster)))
