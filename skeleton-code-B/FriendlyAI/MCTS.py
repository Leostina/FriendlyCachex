import math
from FriendlyAI.CachexGame import CachexGame
from FriendlyAI.CachexBoard import Board
import numpy as np
#######################################################
# partially referenced from 
# https://github.com/suragnair/alpha-zero-general
#######################################################

EPS = 1e-8

class MCTS():

    def __init__(self, game, iterno):
        self.game = game
        self.iterno = iterno
        self.Es = {} 
        self.Qsa = {} 
        self.Vs = {}  
        self.Ns = {}  
        self.Nsa = {}
        self.Ps = {}  


    def getActionProb(self, board, temp=1):

        for i in range(self.iterno):
            self.search(board)
        ## debug
        # for key in self.Nsa.keys():
        #     data = np.reshape(np.frombuffer(key[0], dtype=int),[board.n,board.n])
        #     temp_b = Board(board.n)
        #     temp_b._data = data
        #     CachexGame.display(CachexGame, temp_b)

        s = self.game.stringRepresentation(board)
        counts = [self.Nsa[(s, a)] if (s, a) in self.Nsa else 0 for a in range(self.game.getActionSize())]
        
        if temp == 0:
            bestAs = np.array(np.argwhere(counts == np.max(counts))).flatten()
            bestA = np.random.choice(bestAs)
            probs = [0] * len(counts)
            probs[bestA] = 1
            return probs
        counts = [x ** (1. / temp) for x in counts]
        counts_sum = float(sum(counts))
        probs = [x / counts_sum for x in counts]
        return probs


    def rollout(self, board, curr_player):
        next_player = curr_player
        while(1):
            v = self.game.getGameEnded(board, self.game.color)
            if v != 0:
                return v 
            
            a = np.random.choice(self.game.getValidMoves(board, next_player))
            board, next_player = self.game.getNextState(board, next_player, a)
            # board.swap_pos()

    def search(self, board):

        s = self.game.stringRepresentation(board)

        if s not in self.Es:
            self.Es[s] = self.game.getGameEnded(board, 1)
        if self.Es[s] != 0:
            # end, terminal node
            return -self.Es[s]

        if s not in self.Ps:
            # !!! Replace self.Ps[s], v = self.nnet.predict(board._data)
            valids = self.game.getValidMoves(board, 1)
            self.Ps[s], v = np.array((self.game.n*self.game.n+1 )*[EPS]), self.rollout(board, 1)
            self.Ps[s] = self.Ps[s] * valids 
            sum_Ps_s = np.sum(self.Ps[s])
            
            self.Ps[s] /= sum_Ps_s

            self.Vs[s] = valids
            self.Ns[s] = 0
            return -v

        valids = self.Vs[s]
        cur_best = -float('inf')
        best_act = -1
        # arg UCB
        for a in range(self.game.getActionSize()):
            if valids[a]:
                if (s, a) in self.Qsa:
                    u = self.Qsa[(s, a)] + self.Ps[s][a] * math.sqrt(self.Ns[s]) / (
                            1 + self.Nsa[(s, a)])
                else:
                    u = self.Ps[s][a] * math.sqrt(self.Ns[s] + EPS)  # Q = 0 ?

                if u > cur_best:
                    cur_best = u
                    best_act = a

        a = best_act
        if board.turn > 343:
            return EPS


        next_board, _ = self.game.getNextState(board, 1, a)
        next_board.swap_pos()

        v = self.search(next_board)

        if (s, a) in self.Qsa:
            self.Qsa[(s, a)] = (self.Nsa[(s, a)] * self.Qsa[(s, a)] + v) / (self.Nsa[(s, a)] + 1)
            self.Nsa[(s, a)] += 1

        else:
            self.Qsa[(s, a)] = v
            self.Nsa[(s, a)] = 1

        self.Ns[s] += 1
        return -v

