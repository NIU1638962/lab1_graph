# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 08:36:20 2022

@author: Joel Tapia Salvador (1638962)
"""
import networkx as nx
import numpy as np

NODES_FILE = "lastfm_asia_target.csv"
EDGES_FILE = "lastfm_asia_edges.csv"


def build_lastfm_graph(node_file=NODES_FILE, edge_file=EDGES_FILE):
    """
    Inicialize the graph from the files given as parameters.

    Parameters
    ----------
    node_file : str, optional
        Name of the file with the nodes of the graph, separated by ",", first
        column is the name of the node, seconf one is the attribute of said
        node. The default is NODES_FILE.
    edge_file : TYPE, optional
        Name of the file with the eges of the graph, separated by ",", first
        column is the name of the first node, seconf one is the name of the
        second node. The default is EDGES_FILE.

    Returns
    -------
    G : networkx graph type
        Graph generated from the files given as parameters.

    """
    G = nx.Graph()
    with open(node_file, "r", encoding="utf-8") as file_n:
        """
        Using a list comprehension: reads file, line by line, ignoring the
        first line (header line), generate a list of tuples with the node name
        as first argument and node dictionary propery as second argument.
        From that list, using networkx built in method '.add_nodes_from()',
        creates the nodes from the list of tuples.
        """
        G.add_nodes_from(
            [
                (line.split(",")[0], {"target": line.split(",")[1][:-1]})
                for num, line in enumerate(file_n)
                if num != 0
            ]
        )
    with open(edge_file, "r", encoding="utf-8") as file_e:
        """
        Using a list comprehension: reads file, line by line, ignoring the
        first line (header line), generate a list of edges (tuples) with the
        node names as arguments.
        From that list, using networkx built in method '.add_edges_from()',
        creates the edges from the list of tuples.
        """
        G.add_edges_from(
            [tuple(line[:-1].split(",")) for num, line in enumerate(file_e) if num != 0]
        )
    return G


graph = build_lastfm_graph()


def how_many_components_BFS(G=graph):
    """
    Generates a list of list with components of the given graph using
    Breadth-First Search (https://en.wikipedia.org/wiki/Breadth-first_search).
    Each list of component has the names of the nodes in said component.

    Parameters
    ----------
    G : networkx graph type, optional
        Graph from wich we want to extract the components. The default is
        graph.

    Returns
    -------
    components : list of list of strings.
        List of list with components of the given graph
        Each list of component has the names of the nodes in said component.

    """
    components = []  # List were the components will be saved.
    dic_visited = {}  # Dictionary were we will save the nodes visited.
    for i in list(G.nodes):  # Add the nodes to the dictionary.
        dic_visited[i] = False
        """"False" means that the nodes hasn't been visited yet,
        "True" means that it has been visited."""
    for node in dic_visited.keys():  # If there is more than one component we
        if not dic_visited[node]:  # need toverify that all components (nodes)
            components.append(BFS(G, node, dic_visited))  # has beenvisited and
            # if not, generate a new one.
    return components


def BFS(G, node, dic_visited):
    """
    Generates a new component starting in the given node,
    searching for neighboors (Breadth-first search algorithm), we reuse the
    dictionary with the visited node.

    Parameters
    ----------
    G : networkx graph type
        Graph from wich we want to extract the component.
    node : string
        Name of the node of graph G from wichi we will start the search of the
        component.
    dic : dictionary
        Dictionary with all the nodes of the graph Gthat represents if a node
        has already been searched or not ("True" for searched and "False" for
        not searched).

    Returns
    -------
    component : List of strings
        Has the names of the nodes in the component.

    """
    next_visit = []  # List were the nodes that will be search next.
    component = [node]  # List with the nodes of to the current component.
    dic_added = {}
    for i in list(G.nodes):  # Add the nodes to the dictionary.
        dic_added[i] = False
        """"False" means that the nodes hasn't been added to "next_visit",
        "True" means that it has been added to "next_visit"."""
    next_visit.append(node)
    dic_added[node] = True  # Mark the starting node as added to "next_visit".
    while len(next_visit) > 0:
        current_node = next_visit.pop()  # Retrive last element of the list
        for i in list(nx.neighbors(G, current_node)):  # serach theirs neighbors,
            if (
                not dic_visited[i] and not dic_added[i]
            ):  # if the neighbor hasn't been visited adds it to
                next_visit.insert(0, i)  # start of the list with node to visit
                component.append(i)  # adds it to the current component and
                dic_added[i] = True  # mark it as added to avoid adding it to
                # times befor visiting it.
        dic_visited[current_node] = True  # when we finish searching for its neighbors
        # we mark the node as visited.
    return component


def how_many_components_DFS(G=graph):
    """
    Generates a list of list with components of the given graph using
    Depth-First Search (https://en.wikipedia.org/wiki/Depth-first_search).
    Each list of component has the names of the nodes in said component.

    Parameters
    ----------
    G : networkx graph type, optional
        Graph from wich we want to extract the components. The default is
        graph.

    Returns
    -------
    components : list of list of strings.
        List of list with components of the given graph
        Each list of component has the names of the nodes in said component.

    """
    components = []  # List were the components will be saved.
    dic_visited = {}  # Dictionary were we will save the nodes visited.
    for i in list(G.nodes):  # Add the nodes to the dictionary.
        dic_visited[i] = False
        """"False" means that the nodes hasn't been visited yet,
        "True" means that it has been visited."""
    for node in dic_visited.keys():  # If there is more than one component we
        if not dic_visited[node]:  # need toverify that all components (nodes)
            components.append(DFS(G, node, dic_visited))  # has beenvisited and
            # if not, generate a new one.
    return components


def DFS(G, node, dic_visited):
    """
    Generates a new component starting in the given node,
    searching for neighboors (Deep-first search algorithm), we reuse the
    dictionary with the visited node.

    Parameters
    ----------
    G : networkx graph type
        Graph from wich we want to extract the component.
    node : string
        Name of the node of graph G from wich we will start the search of the
        component.
    dic : dictionary
        Dictionary with all the nodes of the graph G that represents if a node
        has already been searched or not ("True" for searched and "False" for
        not searched).

    Returns
    -------
    component : List of strings
        Has the names of the nodes in the component.

    """
    next_visit = []  # List were the nodes that will be search next.
    component = [node]  # List with the nodes of to the current component.
    dic_added = {}
    for i in list(G.nodes):  # Add the nodes to the dictionary.
        dic_added[i] = False
        """"False" means that the nodes hasn't been added to "next_visit",
        "True" means that it has been added to "next_visit"."""
    next_visit.append(node)
    dic_added[node] = True  # Mark the starting node as added to "next_visit".
    while len(next_visit) > 0:
        current_node = next_visit.pop()  # Retrive last element of the list
        for i in list(nx.neighbors(G, current_node)):  # serach theirs neighbors,
            if (
                not dic_visited[i] and not dic_added[i]
            ):  # if the neighbor hasn't been visited adds it to
                next_visit.append(i)  # start of the list with node to visit
                component.append(i)  # adds it to the current component and
                dic_added[i] = True  # mark it as added to avoid adding it to
                # times befor visiting it.
        dic_visited[current_node] = True  # when we finish searching for its neighbors
        # we mark the node as visited.
    return component


def how_many_degrees(G, a, b):
    """
    Returns the shortest path of the graph G from a to b using Floyd's
    algorithm.

    Parameters
    ----------
    G : networkx graph type
        Graph from wich we want to extract the shortest path.
    a : TYPE
        Staring node.
    b : TYPE
        Ending node.

    Returns
    -------
    List of nodes.
        If there is no path return an empty list, otherwise return the sequence
        of nodes of the path stating at a and ending at b.

    """
    total = [[a, 0]]
    queue = [(a, 0)]
    visited = []
    while queue:
        node, distance = queue.pop(0)
        if node in visited:
            continue
        visited.append(node)
        if node == b:
            return distance
        for adjacent in G.neighbors(node):
            queue.append((adjacent, distance + 1))
            total.append([adjacent, distance + 1])
    distancedict = {}
    for item in total:
        node = item[0]
        distance = item[1]
        if node not in distancedict:
            distancedict[node] = distance
        elif distance < distancedict[node]:
            distancedict[node] = distance
    if b in distancedict:
        return distancedict[b]


def floyd_algorithm(G=graph):
    """
    Executes Floyd's algorith in the graph G
    (https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm).

    Parameters
    ----------
    G : networkx graph type
        Graph from wich we want to extract the shortest path. The default is
        graph.

    Returns
    -------
    dist : list of list (matix)
        Matrix with the distances betwen each pair of nodes.
    next_node : list of list (matix)
        Matrix with the next node of the shortest path.

    """
    # Inicialize a ditionary of dictionaries (froming a matrix with keys), with
    # each value set to infinity, this dictionary will store the value of the
    # current shortest path betwen two nodes.
    dist = [[float("inf") for j in range(int(i))] for i in G.nodes]
    # Inicialize a ditionary of dictionaries (froming a matrix with keys), with
    # each value set to None, this dictionary will store the value of the
    # previus node of the shortest path betwen two nodes.
    # next_node = [[None for j in range(int(i))] for i in G.nodes]
    # We
    for i in G.nodes:
        i = int(i)
        for j in range(i):
            if j != i:
                if str(j) in G[str(i)]:
                    dist[i][j] = 1
                    # next_node[i][j] = j
    for k in G.nodes:
        k = int(k)
        for i in G.nodes:
            i = int(i)
            for j in range(i):
                if int(i) != j and k != j and k != i:
                    if i > k:
                        if j > k:
                            temp_dist = dist[i][k] + dist[j][k]
                        else:
                            temp_dist = dist[i][k] + dist[k][j]
                    else:
                        temp_dist = dist[k][i] + dist[k][j]
                    if dist[i][j] > temp_dist:
                        dist[i][j] = temp_dist
                        # next_node[i][j] = next_node[i][k]
    return dist


def diameters(G=graph):
    dist = floyd_algorithm(G)
    dist = dist[1:]
    diameter = max([max(i) for i in dist])
    if diameter == float("inf"):
        return None
    return diameter
