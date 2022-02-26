# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 11:21:53 2022

@author: Joel Tapia Salvador (1638962)
"""
import random


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
    "09846738943"
)
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
    (20, 5, 5)
)
NAMES = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
lt = []
for i, j, n in zip(SEEDS, RANGES, NAMES):
    random.seed(i)
    with open(
        "lastfm_asia_target_test_reduced" + n + ".csv", "w", encoding="utf-8"
    ) as file:
        file.write("id,target\n")
        expected_nodes = [
            file.write(str(i) + "," + str(random.randint(0, j[0])) + "\n")
            for i in range(j[1])
        ]
    with open(
        "lastfm_asia_edges_test_reduced" + n + ".csv", "w", encoding="utf-8"
    ) as file:
        file.write("node_1,node_2\n")
        expected_edges = [
            file.write(str(i) + "," + str(random.randint(0, j[1] - 1)) + "\n")
            for i in range(j[2])
        ]
        lt.append((expected_nodes, expected_edges))
