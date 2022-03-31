"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching

This module contains some helper functions for printing actions and boards.
Feel free to use and/or modify them to help you develop your program.
"""

from itertools import islice
import string
from this import d
from matplotlib.image import imread


def apply_ansi(str, bold=True, color=None):
    """
    Wraps a string with ANSI control codes to enable basic terminal-based
    formatting on that string. Note: Not all terminals will be compatible!
    Don't worry if you don't know what this means - this is completely
    optional to use, and not required to complete the project!

    Arguments:

    str -- String to apply ANSI control codes to
    bold -- True if you want the text to be rendered bold
    color -- Colour of the text. Currently only red/"r" and blue/"b" are
        supported, but this can easily be extended if desired...

    """
    bold_code = "\033[1m" if bold else ""
    color_code = ""
    if color == "r":
        color_code = "\033[31m"
    if color == "b":
        color_code = "\033[34m"
    return f"{bold_code}{color_code}{str}\033[0m"



# Author: Leo
# a cell
class Cell():
    def __init__(self, coord=None, parent=None, g_val=0, h_val=0, f_val=0):
        self.coord = coord
        self.parent = parent
        self.g_val = g_val
        self.h_val = h_val
        self.f_val = f_val

    def __eq__(self, cell):
        return self.coord == cell.coord

    def __str__(self):
        return "Coord: {}, Parent: {}, g: {}, h: {}, f: {}".format(self.coord, self.parent, self.g_val, self.h_val, self.f_val)

# Author: Leo
# a board, im_red == False indicates we are BLUE xD
class Board():
    def __init__(self, board_size, red_cells=None, blue_cells=None, im_red=True) -> None:
        self.board_size = board_size
        self.red_cells = red_cells
        self.blue_cells = blue_cells
        self.im_red = im_red 
    
    def __str__(self):
        size_str = "| Board size: " + str(self.board_size) + "\n"
        color_str = "| Side: " + (apply_ansi("RED", bold = True, color = "r") if (self.im_red) else apply_ansi("RED", bold = True, color = "r")) + "\n"
        
        red_str = "| Red cells: \n"
        if (self.red_cells):                
            for cell in self.red_cells:
                red_str += ("| "+ apply_ansi(str(cell), bold = True, color = "r")  + "\n")
            red_str += "\n"
        else:
            red_str += "| -\n"

        blue_str = "| Blue cells: \n"
        if (self.blue_cells):
            for cell in self.blue_cells:
                blue_str += ("| " + apply_ansi(str(cell),
                             bold=True, color="b")+"\n")
            blue_str += "\n"
        else:
            blue_str += "| -\n"
        return size_str + color_str + red_str + blue_str




def print_coordinate(r, q, **kwargs):
    """
    Output an axial coordinate (r, q) according to the format instructions.

    Any keyword arguments are passed through to the print function.
    """
    print(f"({r},{q})", **kwargs)

def print_board(n, board_dict, message="", ansi=False, **kwargs):
    """
    For help with visualisation and debugging: output a board diagram with
    any information you like (tokens, heuristic values, distances, etc.).

    Arguments:

    n -- The size of the board
    board_dict -- A dictionary with (r, q) tuples as keys (following axial
        coordinate system from specification) and printable objects (e.g.
        strings, numbers) as values.
        This function will arrange these printable values on a hex grid
        and output the result.
        Note: At most the first 5 characters will be printed from the string
        representation of each value.
    message -- A printable object (e.g. string, number) that will be placed
        above the board in the visualisation. Default is "" (no message).
    ansi -- True if you want to use ANSI control codes to enrich the output.
        Compatible with terminals supporting ANSI control codes. Default
        False.
    
    Any other keyword arguments are passed through to the print function.

    Example:

        >>> board_dict = {
        ...     (0, 4): "hello",
        ...     (1, 1): "r",
        ...     (1, 2): "b",
        ...     (3, 2): "$",
        ...     (2, 3): "***",
        ... }
        >>> print_board(5, board_dict, "message goes here", ansi=False)
        # message goes here
        #              .-'-._.-'-._.-'-._.-'-._.-'-.
        #             |     |     |     |     |     |
        #           .-'-._.-'-._.-'-._.-'-._.-'-._.-'
        #          |     |     |  $  |     |     |
        #        .-'-._.-'-._.-'-._.-'-._.-'-._.-'
        #       |     |     |     | *** |     |
        #     .-'-._.-'-._.-'-._.-'-._.-'-._.-'
        #    |     |  r  |  b  |     |     |
        #  .-'-._.-'-._.-'-._.-'-._.-'-._.-'
        # |     |     |     |     |hello| 
        # '-._.-'-._.-'-._.-'-._.-'-._.-'
        
    """

    stitch_pattern = ".-'-._"
    edge_col_len = 3
    v_divider = "|"
    h_spacing = len(stitch_pattern)
    output = message + "\n"

    # Helper function to only selectively apply ansi formatting if enabled
    apply_ansi_s = apply_ansi if ansi else lambda str, **_: str

    # Generator to repeat pattern string (char by char) infinitely
    def repeat(pattern):
        while True:
            for c in pattern:
                yield c

    # Generate stitching pattern given some offset and length
    def stitching(offset, length):
        return "".join(islice(repeat(stitch_pattern), offset, length))

    # Loop through each row i from top (print ordering)
    # Note that n - i - 1 is equivalent to r in axial coordinates
    for i in range(n):
        x_padding = (n - i - 1) * int(h_spacing / 2)
        stitch_length = (n * h_spacing) - 1 + \
            (int(h_spacing / 2) + 1 if i > 0 else 0)
        mid_stitching = stitching(0, stitch_length)

        # Handle coloured borders for ansi outputs
        # Fairly ugly code, but there is no "simple" solution
        if i == 0:
            mid_stitching = apply_ansi_s(mid_stitching, color="r")
        else:
            mid_stitching = \
                apply_ansi_s(mid_stitching[:edge_col_len], color="b") + \
                mid_stitching[edge_col_len:-edge_col_len] + \
                apply_ansi_s(mid_stitching[-edge_col_len:], color="b")

        output += " " * (x_padding + 1) + mid_stitching + "\n"
        output += " " * x_padding + apply_ansi_s(v_divider, color="b")

        # Loop through each column j from left to right
        # Note that j is equivalent to q in axial coordinates
        for j in range(n):
            coord = (n - i - 1, j)
            value = str(board_dict.get(coord, ""))
            contents = value.center(h_spacing - 1)
            if ansi:
                contents = apply_ansi_s(contents, color=value)
            output += contents + (v_divider if j < n - 1 else "")
        output += apply_ansi_s(v_divider, color="b")
        output += "\n"
    
    # Final/lower stitching (note use of offset here)
    stitch_length = (n * h_spacing) + int(h_spacing / 2)
    lower_stitching = stitching(int(h_spacing / 2) - 1, stitch_length)
    output += apply_ansi_s(lower_stitching, color="r") + "\n"

    # Print to terminal (with optional args forwarded)
    print(output, **kwargs)



# process_input()
# Author: Leo
def process_input(json_dict):
    """process input dict read from json"""

    board_n = json_dict["n"]
    start_board = {(cell[1], cell[2]):cell[0] for cell in json_dict["board"]}
    start = json_dict["start"]
    goal = json_dict["goal"]

    board = Board(board_size=board_n, red_cells=None, blue_cells=start_board, im_red=True)
    print(board)

    disp_board = start_board.copy()
    disp_board.update({tuple(start): "S",tuple(goal): "G"})
    print_board(n=board_n, board_dict=disp_board, message=apply_ansi(
        str("== Input processed, Starting and Goal cells are marked as S/G, enjoy! =="), True, "b"), ansi=True)

    return board_n, start_board, start, goal


# visual_path()
# Author: Leo
def visual_path(board_n, start_board, path):
    # path is identical to the start_board
    if (len(path)<=2):
        return start_board
    disp_board = start_board.copy()
    idx = 1
    for cell in path[1:-1]:
        disp_board.update({cell.coord : str(idx)})
        idx+=1
    print_board(n=board_n , board_dict=disp_board, message=apply_ansi(
    str("== Displaying a path, from player BLUE =="), True, "b"), ansi=True)
