## code for the player's subclass of Gomoku Agent
from gomoku import BOARD_SIZE
from gomokuAgent import GomokuAgent
import re
from misc import legalMove
import sys
import numpy as np # we can use the prime function to do our tests WITHOUT having to repeat the methods

class Player(GomokuAgent):
    def move(self, board):
        while True:
            x=input()
            y=input()
            moveLoc = (int(x),int(y))
            if legalMove(board, moveLoc):
                return moveLoc
            print("Illegal move,Try Again")


