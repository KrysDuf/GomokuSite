## code for the player's subclass of Gomoku Agent
from gomoku import BOARD_SIZE
from gomokuAgent import GomokuAgent
import re
from misc import legalMove
import sys
import numpy as np # we can use the prime function to do our tests WITHOUT having to repeat the methods

class Player(GomokuAgent):

    '''
    findHighest - a function where the player picks the best option out of the
    found priority list
    @param self
    @param board
    @return self.gridScanner(board)
    '''
    def move(self, board):
        return self.gridScanner(board)


                            
    '''
    gridScanner - a function returning a 2D array that shows priorities of a given diagram
    @param - the gomoku board
    @return - priorScan, the given grid 
    '''
    def gridScanner(self, board):
        X = 5
        Y = 5
        highestValue = 0
        boardPrime = np.rot90(board) # for the 90 degree angle
        value = 0

        for row in range(BOARD_SIZE): # the for loops will use a similar structure to the win test
            for col in range(BOARD_SIZE):
                if (board[row, col] == 0): # the rule for all the 9 arrays is the centre is always 0 - as this is the space we wish to play
                    value = value + self.rowScan(board, row, col)
                    value = value + self.diagScan(board, row, col)
                    # we need to repeat the process for the 90 degree angle
                    value = value + self.rowScan(boardPrime, row, col)
                    value = value + self.diagScan(boardPrime, row, col)
                    # after this we can add the value to the current selected item, and reset value to 0
                    if(highestValue < value):
                        X = row
                        Y = col
                        highestValue = value
                    
                    value = 0

        return tuple((X, Y))



    '''
    rowScan - a function that gathers a 9 array, 4 to the left of selected tile, and 5 to the right of the
    selected tile. Then calls the Weighting code, before returning the given value into the Scanner
    @param board - the Gomoku board (either the regular or Prime (90deg rotated) board
    @param row - the row selected
    @param col - the column selected
    @return self.getValue(scanList) - the calculated priority number given by getValue(array)
    '''  
    def rowScan(self, board, row, col):
        if (board[row, col] != 0):
            return 0
        scanList = []
        for i in range(row-4, row+5): # for the rowScan - we count 4 col items before and 4 col items after the empty space
            if (i > 0 and i < BOARD_SIZE):
                scanList.append(board[i, col])
            else:
                scanList.append(-2)

        # once all the items are gathered, we can directly call the function for value and return to gridScanner
        return self.getValue(scanList) 


    '''
    diagScan - a function that gathers a 9 array, 4 to the left of selected tile, and 5 to the right of the
    selected tile. Then calls the Weighting code, before returning the given value into the Scanner
    @param board - the Gomoku board (either the regular or Prime (90deg rotated) board
    @param row - the row selected
    @param col - the column selected
    @return self.getValue(scanList) - the calculated priority number given by getValue(array)
    '''
    def diagScan(self, board, row, col):
        if (board[row, col] != 0):
            return 0
        scanList = []
        for i in range(col-4, col+5): # for the diagScan, we use THRESHOLD to deal
            if (i > 0 and i < BOARD_SIZE):
                scanList.append(board[row, i])
            else:
                scanList.append(-2)

        # once all the items are gathered, we can directly call the function for value and return to gridScanner
        return self.getValue(scanList)




    '''
    getValue - a function that will take an array, and determine the priority
    based on the placements of characters in the string derived by array

    @param array - the 9 size array
    @return value - the determined priority value as a result of combo
    '''
    def getValue(self, array): #0 = opponent, 1 = empty, 2 = ours
        value = 0
        arrStr = ""

        for i in array:
            if (self.ID == -1):
                arrStr = arrStr + str((i*-1)+1)
            else:
                arrStr = arrStr + str(i+1)
        
        #Winning States
        if(re.search("2{4}", arrStr)):
            value = value + 10000
        if(re.search("21222", arrStr)):
            value = value + 10000
        if(re.search("22212", arrStr)):
            value = value + 10000
        if(re.search("22122", arrStr)):
            value = value + 10000

        # 3 in a row with both ends clear and one end having 2 clear
        if(re.search("10{3}1", arrStr)): #  10001s 
            if(re.search("10{3}11", arrStr) or re.search("110{3}1", arrStr)):
                value = value + 1000
            else:
                value = value + 100
      
        if(re.search("1{1,2}2{3}1{1,2}", arrStr)): 
            if(re.search("112221", arrStr) or re.search("122211", arrStr)):
                value = value + 1000
            else:
                value = value + 100

        if(re.search("0{4}", arrStr)):
            value = value + 1000

        # our 3 in a row
        if(re.search("1{1,2}2221{1.2}", arrStr)): 
            value = value + 50

        # 2 in a row with spaces on the sides
        if(re.search("1{1,2}221{1,2}", arrStr)): 
            value = value + 10

        # Empty space with 1-2 opponent or our pieces on both sides
        if(re.search("..0{1,2}10{1,2}..", arrStr)): 
            value = value + 10   
        if(re.search("..2{1,2}12{1,2}..", arrStr)):
            value = value + 10   

        # matching 2 of the same adjecent to target cell
        if(re.search("....100...", arrStr)): 
            value = value + 3    
        if(re.search("...001....", arrStr)):
            value = value + 3
        if(re.search("....122...", arrStr)):
            value = value + 3    
        if(re.search("...221....", arrStr)):
            value = value + 3

        # adjecent to another piece
        if(re.search("....12...", arrStr)): 
            value = value + 2
        if(re.search("...21....", arrStr)):
            value = value + 2
        if(re.search("....10...", arrStr)): 
            value = value + 1
        if(re.search("...01....", arrStr)):
            value = value + 1
        return value


