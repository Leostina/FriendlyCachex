import numpy as np
from .CachexBoard import *

# Very small number
_EPS = 1e-8
_MAX_REPEAT_STATES = 7
_MAX_TURNS = 343 

class CachexGame():
    content_lookup = {-1: "B", 0: "-", 1:"R"}
    
    @staticmethod
    def getPieceContent(piece):
        return CachexGame.content_lookup[piece]

    def getInitBoard(self, n, color):
        # return the board at init
        board = Board(self.n, color)
        return board

    def __init__(self, n, color):
        self.n = n
        self.color = color
        self.board = self.getInitBoard(n, color)

    def getBoardSize(self):
        return (self.n, self.n)

    def getActionSize(self):
        return self.n*self.n + 1

    def getNextState(self, board, player, action):
        b = board.deep_copy()
        b.execute_move(action, player)
        return (b, -player) 
    
    def getValidMoves(self, board, player):
        moves = (board.n*board.n+1)*[0]
        for r in range(board.n):
            for q in range(board.n):
                if board._data[r][q] == 0:
                    moves[board.n*r+q] = 1
        if board.turn == 2:
            moves[-1] = 1
        elif board.turn == 1 and board.n > 2 and board.n % 2 == 1:
            moves[int((board.n*board.n-1)/2)] = 0
        return np.array(moves)
            
    def getGameEnded(self, board:Board, player):

        # draw?
        if board.turn >= _MAX_TURNS or any(np.array(list(board.history.values()))>=_MAX_REPEAT_STATES):
            return _EPS
        # winner?
        
        frontier = [(r,0) for r in range(board.n) if board._data[r, 0] == -player]
        explored = set()
        while (len(frontier)):
            curr_coord = frontier.pop()
            explored.add(curr_coord)
            for coord in board._coord_neighbours(curr_coord):
                if coord not in explored and board._data[coord] == -player:
                    if coord[1] == board.n- 1 :
                        return -player
                    frontier.append(coord)

        frontier = [(0,q) for q in range(board.n) if board._data[0,q] == player]
        explored = set()
        while (len(frontier)):
            curr_coord = frontier.pop()
            explored.add(curr_coord)
            for coord in board._coord_neighbours(curr_coord):
                if coord not in explored and board._data[coord] == player:
                    if coord[0] == board.n - 1:
                        return player
                    frontier.append(coord)

        return 0

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        board._data*=player

        return board

    def getSymmetries(self, board, pi):
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []
        # rot 180 deg and itsef
        for i in [2,4]:
            newB = np.rot90(board._data, i)
            newPi = np.rot90(pi_board, i)
            l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board:Board):
        specode = board.turn
        if specode != 1 and specode != 2:
            specode = 3
        return (board._data+specode).tobytes()

    def stringRepresentationReadable(self, canonicalBoard):
        board_s = "".join(self.content_lookup[cell] for r in canonicalBoard for cell in r)
        return board_s

    
