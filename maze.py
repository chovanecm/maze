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

def analyze(maze):
    goal = find_goal(maze)
    distances, predecessors = dijkstra(maze, goal)
    class Result():
        def __init__(self):
            self.distances = distances
            self.is_reachable = (distances[maze >= 0] >= 0).min()
            self.directions = np.full(maze.shape, "#", dtype="|S1")
            # Empty spaces (not reachable)
            self.directions[(maze >= 0) & (distances == -1)] = " "
            for i in range(maze.shape[0]):
                self.directions[i, predecessors[i, :, 0] == i-1] = "^"
                self.directions[i, predecessors[i, :, 0] == i + 1] = "v"
            for i in range(maze.shape[1]):
                self.directions[predecessors[:, i, 1] == i - 1, i] = "<"
                self.directions[predecessors[:, i, 1] == i + 1, i] = ">"
            self.directions[tuple(goal)] = "X"

            self.goal = tuple(goal)

        def path(self, row, column):
            if distances[row, column] < 0:
                raise IndexError("No way from this point.")
            t_goal = tuple(goal)
            shortest_path = []
            node = (row, column)
            shortest_path.append(node)
            while node != t_goal:
                node = tuple(predecessors[node])
                shortest_path.append(node)
            return shortest_path

    return Result()


def find_goal(maze):
    goal = np.argwhere(maze == 1)
    if goal is not None and len(goal) > 0:
        return goal[0]
    else:
        return None


def dijkstra(maze, start):
    INF = maze.shape[0] * maze.shape[1] * 2
    distances = np.full(shape=maze.shape, fill_value=INF, dtype=np.int)
    distances[tuple(start)] = 0
    predecessors = np.full(shape=(maze.shape[0], maze.shape[1], 2), fill_value = (-100, -100), dtype=(int, int))
    q = PriorityQueue()

    def relax(u1, u2):
        if distances[tuple(u2)] > distances[tuple(u1)] + 1:
            distances[tuple(u2)] = distances[tuple(u1)] + 1
            predecessors[tuple(u2)] = u1
            q.put((distances[tuple(u2)], tuple(u2)))

    def adj(u):
        adj_list = []
        north = u + (-1, 0)
        south = u + (1, 0)
        east = u + (0, 1)
        west = u + (0, -1)
        if north[0] >= 0 and maze[tuple(north)] >= 0:
            adj_list.append(north)
        if south[0] < maze.shape[0] and maze[tuple(south)] >= 0:
            adj_list.append(south)
        if east[1] < maze.shape[1] and maze[tuple(east)] >= 0:
            adj_list.append(east)
        if west[1] >= 0 and maze[tuple(west)] >= 0:
            adj_list.append(west)
        return adj_list


    #for i in range(maze.shape[0]):
    #    for j in range(maze.shape[1]):
    #        if (maze[i,j] > 0):
    q.put((0, tuple(start)))

    while not q.empty():
        u = np.array(q.get()[1])
        for u_a in adj(u):
            relax(u, u_a)
    distances[distances == INF] = -1

    return distances, predecessors



def visualise(maze):
    res = analyze(maze)

    #cp[distances == distances.max()] = max + 10
    plt.imshow(res.distances, interpolation="nearest")
    plt.show()
    print(res.directions)


# maze.tofile("fixtures/maze.dat")
# visualise(maze)
#visualise(mg.mi_pyt_maze(15, 100, 2, 2))


if __name__ == "__main__":
    import gui

    gui.main()
