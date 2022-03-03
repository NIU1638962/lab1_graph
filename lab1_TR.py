# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def build_lastfm_graph(filename="lastfm_asia_edges.csv"):
    f = open(filename, "r")
    G = nx.Graph()

    for line in f.read().split():
        if "node" not in line:
            a, b = line.split(",")
            G.add_edge(a, b)
    return G


G = build_lastfm_graph()


def how_many_components_BFS(G):
    component_list = []
    graph = list(G.nodes())

    while graph:
        queue = [graph[0]]
        visited = [graph[0]]
        while queue:
            current = queue.pop(0)
            neighbors = G.neighbors(current)
            graph.remove(current)

            for i in neighbors:
                if i not in visited:
                    visited.append(i)
                    queue.append(i)
        component_list.append(visited)
    return component_list


def DFS(v, g, current):
    if current not in v:
        v.append(current)
        neighbors = g.neighbors(current)
        for i in neighbors:
            DFS(v, g, i)


def how_many_components_DFS(G):
    component_list = []

    # make a list of all the nodes
    graph = list(G.nodes())

    # start the search from the first node

    while graph:
        current = graph[0]
        visited = []
        DFS(visited, G, current)
        # print(visited)
        component_list.append(visited)

        for x in visited:
            graph.remove(x)
    return component_list


def how_many_degrees(G, a, b):
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


def diameters(G):
    longest = np.inf
    graph = list(G.nodes())
    distances = []
    checked = []
    for i in graph:
        checked.append(i)
        for j in graph:
            if j not in checked:
                distances.append(how_many_degrees(G, i, j))
    distances = list(filter(None, distances))
    return max(distances)
