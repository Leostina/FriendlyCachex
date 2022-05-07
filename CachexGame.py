import numpy as np
import Setup
from Setup import Board
from Game import Game

class CachexGame(Game):
    content_lookup = {-1: "B", 0: "-", 1:"R"}
    
    @staticmethod
    def getPieceContent(piece):
        return CachexGame.content_lookup[piece]

    def __init__(self, n):
        self.n = n
        
    def getInitBoard(self):
        # return the board at init
        board = Board(self.n)
        return np.array(board._data)

    def getBoardSize(self):
        # return initial board
        return (self.n, self.n)

    def getNextState(self, board, player, action):
        # action must be a valid move
        b = Board(self.n)
        b._data = np.copy(board)
        b.execute_move(action, player)
        # switch player
        return (b._data, -player) 



    def execute_move(self, move, color):
