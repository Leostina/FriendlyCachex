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
    board, start_cell, goal_cell = process_input(data)
    

    # TODO:
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information).
    
    path = a_star(board.board_size, (board.blue_cells if board.im_red else board.red_cells), start_cell, goal_cell)
    print(len(path))
    [print(p.coord) for p in path]


    # visual the path we found
    visual_path(board, path, extra_cells=[start_cell, goal_cell])

def a_star(n, board, start, goal):
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
        return coord[0] >= 0 and coord[1] >= 0 and coord[0] < n and coord[1] < n and (coord not in board.keys())

    def path_backtrack(cell) -> list:
        path = []
        while(cell):
            path.insert(0, cell)
            cell = cell.parent
        return path

    def calc_heuristic(cell, goal):
        return abs(goal.coord[0]-cell.coord[0]) + abs(goal.coord[1]-cell.coord[1])

    def add_tuple(t1, t2):
        return (t1[0]+t2[0], t1[1]+t2[1])

    # init

    frontier, visited = [start], []


    while (len(frontier) > 0):
        # find and move to the best cell with min f_val in the frontier
        curr_idx = min_f_val(frontier)
        curr_cell = frontier[curr_idx]
        visited.append(curr_cell) 
        frontier.pop(curr_idx)
        
        # goal test
        if curr_cell == goal:
            return path_backtrack(curr_cell)


        # reachable cells
        reachable = []
        for delta in [(1,-1),(1,0),(0,1),(-1,1),(-1,0),(0,-1)]:
            new_coord = add_tuple(curr_cell.coord,delta)
            if check_valid_cell(new_coord, n):
                reachable.append(Cell(coord=new_coord, parent=curr_cell))

        # examine each reachable
        for cell in reachable:

            # if visited, pass on
            if any(cell == v for v in visited):
                continue

            # assign g h f values
            cell.g_val = curr_cell.g_val + 1 # one more step
            cell.h_val = calc_heuristic(cell, goal)
            cell.f_val = cell.g_val + cell.h_val

            # if cell exists in frontier, add if new version has a better f value
            add = True
            for fid, f in enumerate(frontier):
                if f == cell:
                    if f.g_val < cell.g_val:
                        add = False
                        break
                    else:
                        frontier.pop(fid)
            if add:
                frontier.append(cell)
