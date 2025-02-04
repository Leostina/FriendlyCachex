"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json
from search.util import *

# main()
def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)


    # given starting board config
    board, start_cell, goal_cell = process_input(data)
    path = a_star(board.board_size, board, start_cell, goal_cell)
    
    # Visualise the path
    #visual_path(board, path, [start_cell, goal_cell])

    pa_path = [p for p in path if p.coord not in (board.red_cells.keys() if board.im_red else board.blue_cells.keys())] # part a path
    print(len(pa_path))
    [print(cell.coord) for cell in pa_path]

# s_star()
# Author: Leo 
# A* Search
def a_star(n, board, start, goal):

    enemies = board.blue_cells

    if board.im_red:
        enemies = board.blue_cells
        captured = board.red_cells
    else:
        enemies = board.red_cells
        captured = board.blue_cells

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
        return coord[0] >= 0 and coord[1] >= 0 and coord[0] < n and coord[1] < n and (coord not in enemies.keys())

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


            cell.g_val = curr_cell.g_val + 1 if cell.coord not in captured.keys() else curr_cell.g_val # one more step 
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
    return []
