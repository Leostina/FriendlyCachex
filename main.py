"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json
from typing import List
from numpy import fromiter

from sympy import true

# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:
from util import *
def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)
    
    print(apply_ansi("Hi Selena in RED", True, "r"))
    print(apply_ansi("Hi Selena in BLUE", True, "b"))
    
    # given starting board config 
    board_n, start_board, start_cell, goal_cell = process_input(data)
    
    
    # TODO:
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information).


class Cell():
    def __init__(self, coord=None, parent=None, g_val=0, h_val=0, f_val=0):
        self.coord = coord
        self.parent = parent
        self.g_val = g_val
        self.h_val = h_val
        self.f_val = f_val

    def __eq__(self, cell):
        return self.coord == cell.coord

def astar(map, start, goal):

    # return index of the Cell with min f_val 
    def min_f_val(list) -> int:
        best_i = 0
        best_val = list[0].f_val
        for i in range(len(list)):
            val = list[i].f_val
            if val < best_val:
                best_val = val
                best_i = i
        return best_i

    def check_valid_cell(coord, n):
        return coord[0] > 0 and coord[1] > 0 and coord[0] < n and coord[1] < n and (coord not in map.keys())

    def path_backtrack(cell) -> list:
        path = []
        while(cell):
            path.insert(0, cell.coord)
            cell = cell.parent
        return path


    # init
    start = Cell(coord=start)
    goal = Cell(coord=goal)
    frontier_list = []
    visited_list = []
    frontier, visited = [start], []


    while (len(frontier) > 0):
        # find and move to the best cell with min f_val in the frontier
        curr_idx = min_f_val(frontier)
        curr_cell = frontier[curr_idx]
        visited.append(curr_cell) 
        frontier.pop(curr_idx)

        # goal test
        if curr_cell == goal:
            path_backtrack(curr_cell)

        # reachable cells
        reachable = []
        for delta in [(1,-1),(1,0),(0,1),(-1,1),(-1,0),(0,-1)]:
            new_coord = curr_cell.coord + delta
            if check_valid_cell(new_coord):
                reachable.append(Cell(new_coord))
