
import collections
from ctypes.wintypes import HINSTANCE
from queue import Queue
from numpy import zeros, array, roll, vectorize

# Very small number
_EPS = 1e-8

# Utility function to add two coord tuples
_ADD = lambda a, b: (a[0] + b[0], a[1] + b[1])

# Neighbour hex steps in clockwise order
_HEX_STEPS = array([(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)], 
    dtype="i,i")

# Pre-compute diamond capture patterns - each capture pattern is a 
# list of offset steps:
# [opposite offset, neighbour 1 offset, neighbour 2 offset]
#
# Note that the "opposite cell" offset is actually the sum of
# the two neighbouring cell offsets (for a given diamond formation)
#
# Formed diamond patterns are either "longways", in which case the
# neighbours are adjacent to each other (roll 1), OR "sideways", in
# which case the neighbours are spaced apart (roll 2). This means
# for a given cell, it is part of 6 + 6 possible diamonds.
_CAPTURE_PATTERNS = [[_ADD(n1, n2), n1, n2] 
    for n1, n2 in 
        list(zip(_HEX_STEPS, roll(_HEX_STEPS, 1))) + 
        list(zip(_HEX_STEPS, roll(_HEX_STEPS, 2)))]

# Maps between player string and internal token type
_TOKEN_MAP_OUT = { 0: None, 1: "red", 2: "blue" }
_TOKEN_MAP_IN = {v: k for k, v in _TOKEN_MAP_OUT.items()}

# Map between player token types
_SWAP_PLAYER = { 0: 0, 1: 2, 2: 1 }

# Max number of turns allowed before a draw is declared
_MAX_REPEAT_STATES = 7
_MAX_TURNS = 343 

class Board():
    def __init__(self, n):
        self.n = n
        self.turn = 1
        self.curr_move = None
        self._data = zeros((n, n), dtype=int)
        self.history = collections.Counter({self.board.digest(): 1})

    def __getitem__(self, coord):
        """
        Get the token at given board coord (r, q).
        """
        return self._data[coord]

    def __setitem__(self, coord, token):
        """
        Set the token at given board coord (r, q).
        """
        self._data[coord] = _TOKEN_MAP_IN[token]

    def digest(self):
        """
        Digest of the board state (to help with counting repeated states).
        Could use a hash function, but not really necessary for our purposes.
        """
        return self._data.tobytes()

    def swap(self):
        """
        Swap player positions by mirroring the state along the major 
        board axis. This is really just a "matrix transpose" op combined
        with a swap between player token types.
        """
        swap_player_tokens = vectorize(lambda t: _SWAP_PLAYER[t])
        self._data = swap_player_tokens(self._data.transpose())


    def place(self, token, coord):
        """
        Place a token on the board and apply captures if they exist.
        Return coordinates of captured tokens.
        """
        self[coord] = token
        return self._apply_captures(coord)

    def check_win_move(self, color):
        """
        Find connected coordinates from start_coord. This uses the token 
        value of the start_coord cell to determine which other cells are
        connected (e.g., all will be the same value). Within the connected
        cells, if there exist both pieces on start and finish line, return
        True as the winner.
        """
        # start
        if self.curr_move == None:
            return 0

        # check draw?
        if self.turn >= _MAX_REPEAT_STATES:
            return _EPS
        if self.history[self.digest()] >= _MAX_REPEAT_STATES:
            return _EPS


        # Get search token type
        token_type = self._data[self.curr_move]
        # the position in tuple (r, q) that is 0
        start_zero_idx = 0 if color == 1 else 1
        end_n_idx = 0 if color == 1 else 1
        has_start = False
        has_end = False
        # Use bfs from start coordinate
        reachable = set()
        queue = Queue(0)
        queue.put(self.curr_move)
        
        while not queue.empty():
            curr_coord = queue.get()
            if not has_start and curr_coord[start_zero_idx] == 0:
                has_start = True
            elif not has_end and curr_coord[end_n_idx] == self.n - 1:
                has_end = True
            if has_start and has_end:
                return color
            reachable.add(curr_coord)
            for coord in self._coord_neighbours(curr_coord):
                if coord not in reachable and self._data[coord] == token_type:
                    queue.put(coord)
        return 0

    def digest(self):
        """
        Digest of the board state (to help with counting repeated states).
        Could use a hash function, but not really necessary for our purposes.
        """
        return self._data.tobytes()

    def inside_bounds(self, coord):
        """
        True iff coord inside board bounds.
        """
        r, q = coord
        return r >= 0 and r < self.n and q >= 0 and q < self.n

    def is_occupied(self, coord):
        """
        True iff coord is occupied by a token (e.g., not None).
        """
        return self[coord] != None

    def _apply_captures(self, coord):
        """
        Check coord for diamond captures, and apply these to the board
        if they exist. Returns a list of captured token coordinates.
        """
        opp_type = self._data[coord]
        mid_type = _SWAP_PLAYER[opp_type]
        captured = set()

        # Check each capture pattern intersecting with coord
        for pattern in _CAPTURE_PATTERNS:
            coords = [_ADD(coord, s) for s in pattern]
            # No point checking if any coord is outside the board!
            if all(map(self.inside_bounds, coords)):
                tokens = [self._data[coord] for coord in coords]
                if tokens == [opp_type, mid_type, mid_type]:
                    # Capturing has to be deferred in case of overlaps
                    # Both mid cell tokens should be captured
                    captured.update(coords[1:])

        # Remove any captured tokens
        for coord in captured:
            self[coord] = None

        return list(captured)

    def _coord_neighbours(self, coord):
        """
        Returns (within-bounds) neighbouring coordinates for given coord.
        """
        return [_ADD(coord, step) for step in _HEX_STEPS \
            if self.inside_bounds(_ADD(coord, step))]

    def get_legal_moves(self, color):
        """
        Returns all possible legal moves. 
        When the current turn is 2,
        the player is allowed to do an extra move type: steal
        => (-1, -1) would be added to the move set to represent it.
        """
        moves = set()
        if self.turn == 2:
            action = self.n * self.n
            move = (int(action/self.n), action%self.n)
            moves.add(move)
        for r in range(self.n):
            for q in range(self.n):
                if self[r][q] == 0:
                    moves.add((r,q))
        if self.turn == 1 and self.n > 2 and self.n % 2 == 1:
            moves.remove((self.n-1)/2,(self.n-1)/2)
        return moves

    def execute_move(self, move, color):
        """Perform the given move, place new token, capture or steal"""
        # move to action
        action = move[0] * self.n + move[1] 
        # Steal
        if action == self.n * self.n:
            self.swap()
            self.turn += 1
            self.new_move = (self.new_move[1],self.new_move[0])
        # Convention place
        else:
            self.place(color, move)
            self.new_move = move
            self._apply_captures(move)
        
        # digest and update history
        self.history[self.digest()] += 1



            
        


