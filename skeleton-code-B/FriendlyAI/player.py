import FriendlyAI.CachexLogic
import FriendlyAI.CachexGame
from FriendlyAI.CachexGame import CachexGame
# import FriendlyAI.CachexNNet
import numpy as np
from FriendlyAI.utils import dotdict
# from NNet import NNetWrapper as NNet
import FriendlyAI.MCTS
from FriendlyAI.MCTS import MCTS

from FriendlyAI.CachexLogic import Board

class Player:
    def __init__(self, player, n):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.
        """
        # first turn starts from 1 or 2
        self.color = 1 if player == "red" else -1
        self.n = n
        self.g = CachexGame(n, self.color)
        self.args1 = dotdict({'numMCTSSims': 1000, 'cpuct':1.0})
        self.mcts = MCTS(self.g, self.args1)
        self.eval = lambda x: np.argmax(self.mcts.getActionProb(x, temp=0))

    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        # put your code here
        a = self.eval(self.g.getCanonicalForm(self.g.board, self.color))
        # convert to coord        
        action = ("STEAL", ) if a == self.n*self.n else ("PLACE", int(a/self.n), int(a % self.n))
        print(action)
        return action

    def turn(self, player, action):
        """
        Called at the end of each player's turn to inform this player of 
        their chosen action. Update your internal representation of the 
        game state based on this. The parameter action is the chosen 
        action itself. 
        
        Note: At the end of your player's turn, the action parameter is
        the same as what your player returned from the action method
        above. However, the referee has validated it at this point.
        """
        # put your code here
        a = self.n*self.n if action == ("STEAL", ) else action[1] * self.n + action[2]
        self.g.board.execute_move(a, self.color)

