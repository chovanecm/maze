# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 09:33:02 2016

@author: Martin
"""
import maze_generator as mg
import numpy as np
from queue import PriorityQueue
from math import inf
from matplotlib import pyplot as plt
from math import sqrt
from maze import analyze
import pytest

@pytest.fixture()
def stored_maze1():
    maze = np.fromfile("fixtures/maze.dat", dtype=np.int)
    maze = maze.reshape((sqrt(len(maze)), sqrt(len(maze))))
    return maze, True

@pytest.fixture()
def stored_maze2():
    maze = np.fromfile("fixtures/not_reachable_maze.dat", dtype=np.int)
    maze = maze.reshape((sqrt(len(maze)), sqrt(len(maze))))
    return maze, False


def test_reachable(stored_maze1, stored_maze2):
    a1 = analyze(stored_maze1[0])
    assert(a1.is_reachable == stored_maze1[1])
    a2 = analyze(stored_maze2[0])
    assert(a2.is_reachable == stored_maze2[1])


def test_directions(stored_maze2):
    a = analyze(stored_maze2[0])
    assert(a.directions[20, 23] == " ")
    assert(a.directions[0, 0] == "#")
    assert(a.directions[0, 0] == "#")
    assert(a.directions[10, 29] == "x")
    #some better tests could be here, such as following the direction signs
    
def test_path(stored_maze2):
    a = analyze(stored_maze2[0])
    point = (1, 1)
    distance = a.distances[point]
    path = a.path(*point)
    assert(len(path) == distance + 1)
    assert(path[0] == point)
    assert(path[-1] == a.goal)
# maze.tofile("fixtures/maze.dat")
# visualise(maze)
#visualise(mg.mi_pyt_maze(15, 100, 2, 2))



