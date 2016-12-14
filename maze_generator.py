# -*- coding: utf-8 -*-
"""
# Code by Erik Sweet and Bill Basener

"""

import random
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
def generate_maze(num_rows, num_cols):
    M = np.zeros((num_rows,num_cols,5), dtype=np.uint8)
    # The array M is going to hold the array information for each cell.
    # The first four coordinates tell if walls exist on those sides 
    # and the fifth indicates if the cell has been visited in the search.
    # M(LEFT, UP, RIGHT, DOWN, CHECK_IF_VISITED)
    image = np.zeros((num_rows*10,num_cols*10), dtype=np.uint8)
    # The array image is going to be the output image to display
    
    # Set starting row and column
    r = 0
    c = 0
    history = [(r,c)] # The history is the 
    
    # Trace a path though the cells of the maze and open walls along the path.
    # We do this with a while loop, repeating the loop until there is no history, 
    # which would mean we backtracked to the initial start.
    while history: 
        M[r,c,4] = 1 # designate this location as visited
        # check if the adjacent cells are valid for moving to
        check = []
        if c > 0 and M[r,c-1,4] == 0:
            check.append('L')  
        if r > 0 and M[r-1,c,4] == 0:
            check.append('U')
        if c < num_cols-1 and M[r,c+1,4] == 0:
            check.append('R')
        if r < num_rows-1 and M[r+1,c,4] == 0:
            check.append('D')    
        
        if len(check): # If there is a valid cell to move to.
            # Mark the walls between cells as open if we move
            history.append([r,c])
            move_direction = random.choice(check)
            if move_direction == 'L':
                M[r,c,0] = 1
                c = c-1
                M[r,c,2] = 1
            if move_direction == 'U':
                M[r,c,1] = 1
                r = r-1
                M[r,c,3] = 1
            if move_direction == 'R':
                M[r,c,2] = 1
                c = c+1
                M[r,c,0] = 1
            if move_direction == 'D':
                M[r,c,3] = 1
                r = r+1
                M[r,c,1] = 1
        else: # If there are no valid cells to move to.
    	# retrace one step back in history if no move is possible
            r,c = history.pop()
        
             
    # Open the walls at the start and finish
    M[0,0,0] = 1
    M[num_rows-1,num_cols-1,2] = 1
        
    # Generate the image for display
    for row in range(0,num_rows):
        for col in range(0,num_cols):
            cell_data = M[row,col]
            for i in range(10*row+1,10*row+9):
                image[i,range(10*col+1,10*col+9)] = 255
                if cell_data[0] == 1:image[range(10*row+1,10*row+9),10*col] = 255
                if cell_data[1] == 1:image[10*row,range(10*col+1,10*col+9)] = 255
                if cell_data[2] == 1:image[range(10*row+1,10*row+9),10*col+9] = 255
                if cell_data[3] == 1:image[10*row+9,range(10*col+1,10*col+9)] = 255
    
    # Display the image
    plt.imshow(image, cmap = cm.Greys_r, interpolation='none')
    plt.show()
    return M
    
    
import numpy
from numpy.random import random_integers as rand
from numpy.random import randint
import matplotlib.pyplot as pyplot


def maze(width=81, height=51, complexity=.75, density=.75, progress_function=None):
    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    density    = int(density * ((shape[0] // 2) * (shape[1] // 2)))
    # Build actual maze
    Z = numpy.zeros(shape, dtype=bool)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1

    total_iterations = density * complexity
    iteration = 0
    # Make aisles
    for i in range(density):
        x, y = randint(0, shape[1] // 2) * 2, randint(0, shape[0] // 2) * 2
        Z[y, x] = 1
        for j in range(complexity):
            iteration += 1
            #  & 131072 is a power of 2
            if iteration & 131071 == 0 and progress_function is not None:
                progress_function(iteration / total_iterations)
            neighbours = []
            if x > 1:             neighbours.append((y, x - 2))
            if x < shape[1] - 2:  neighbours.append((y, x + 2))
            if y > 1:             neighbours.append((y - 2, x))
            if y < shape[0] - 2:  neighbours.append((y + 2, x))
            if len(neighbours):
                y_,x_ = neighbours[randint(0, len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
    return Z


def transform_maze(m):
    """
    Transform maze to our format
    :param m:
    :type m:
    :return:
    :rtype:
    """
    inverted = np.invert(m)
    # Convert True to 2 and False to -1
    m_n = np.apply_over_axes(lambda e, ee: e * 3 - 1, inverted, [0])
    # Add goal:
    possible_goals = np.argwhere(inverted)
    goal_index = np.random.randint(0, len(possible_goals))
    m_n[tuple(possible_goals[goal_index])] = 1
    return m_n


def mi_pyt_maze(*args, **kwargs):
    # in output False = ok, True = maze, we want it vice versa
    m = maze(*args, **kwargs)
    m_n = transform_maze(m)

    pyplot.figure(figsize=(10, 5))
    pyplot.imshow(np.invert(m_n), cmap=pyplot.cm.binary, interpolation='nearest')
    pyplot.xticks([]), pyplot.yticks([])
    # pyplot.show()
    pyplot.savefig("maze.png")
    return m_n