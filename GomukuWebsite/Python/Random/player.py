import numpy as np
from misc import legalMove, winningTest
from gomokuAgent import GomokuAgent
from gomoku import BOARD_SIZE, X_IN_A_LINE

movesMade = 0
providedBoard = None

class Player(GomokuAgent):

    def move(self, board):
        global providedBoard, movesMade
        providedBoard = board.copy()

        bestMove = self.findBestMove(providedBoard)
        movesMade += 1

        return bestMove
    
    def findBestMove(self, board):
        bestValue = -1000
        bestMove = (-1, 1)
        possibleStates = Player.getChildBoards(self.ID, board)

        for ps in possibleStates:
            moveValue = self.minimax(ps, 1, 3, True)
    
            if moveValue > bestValue:
                bestValue = moveValue
                bestMove = self.findNewMoveLoc(ps, board)

        return tuple(bestMove)

    def findNewMoveLoc(self, newBoard, oldBoard):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if newBoard[r, c] != oldBoard[r, c]:
                    return (r, c)

    def minimax(self, board, currentDepth, targetDepth,  maximizingPlayer):
        minimaxValue = self.hFunction(board)

        # game over
        if minimaxValue == 100 or minimaxValue == -100:
            return minimaxValue

        if currentDepth == targetDepth:
            return minimaxValue

        if maximizingPlayer:
            maxEval = -1000
            childBoards = Player.getChildBoards(self.ID, board)
            for child in childBoards:
                evalResult = self.minimax(child, currentDepth + 1, targetDepth, False)
                maxEval = max(maxEval, evalResult)
            return maxEval
        else:
            minEval = 1000
            childBoards = Player.getChildBoards(self.ID * -1, board)
            for child in childBoards:
                evalResult = self.minimax(child, currentDepth + 1, targetDepth, True)
                minEval = min(minEval, evalResult)
            return minEval


    # order from high priority to low priority
    @staticmethod
    def getChildBoards(ID, parentBoard):
        opponentID = ID * -1
        childBoards = list()
        patternFound = False        

        # complete five in a row if straight four is detected
        # scan for straight 4 horizontally left to right
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE-5): 
                if parentBoard[row, col] == 0 and parentBoard[row, col+1] == ID and \
                    parentBoard[row, col+2] == ID and parentBoard[row, col+3] == ID and parentBoard[row, col+4] == ID and \
                    parentBoard[row, col+5] == 0:
                    childBoard = parentBoard.copy()
                    childBoard[row, col] = ID
                    childBoards.append(childBoard)
                    patternFound = True
        # scan for straight 4 vertially top to bottom
        for row in range(BOARD_SIZE-5):
            for col in range(BOARD_SIZE):
                if parentBoard[row, col] == 0 and parentBoard[row+1, col] == ID and \
                    parentBoard[row+2, col] == ID and parentBoard[row+3, col] == ID and parentBoard[row+4, col] == ID and \
                    parentBoard[row+5, col] == 0:
                    childBoard = parentBoard.copy()
                    childBoard[row, col] = ID
                    childBoards.append(childBoard)
                    patternFound = True
        # scan for straight 4 diagonally left to right
        for row in range(BOARD_SIZE-5):
            for col in range(BOARD_SIZE-5):
                if parentBoard[row, col] == 0 and parentBoard[row+1, col+1] == ID and \
                    parentBoard[row+2, col+2] == ID and parentBoard[row+3, col+3] == ID and parentBoard[row+4, col+4] == ID and \
                    parentBoard[row+5, col+5] == 0:
                    childBoard = parentBoard.copy()
                    childBoard[row, col] = ID
                    childBoards.append(childBoard)
                    patternFound = True
        # scan for straight 4 diagonally right to left
        for row in reversed(range(BOARD_SIZE-5)):
            for col in reversed(range(BOARD_SIZE-5)):
                if parentBoard[row, col] == 0 and parentBoard[row-1, col-1] == ID and \
                    parentBoard[row-2, col-2] == ID and parentBoard[row-3, col-3] == ID and parentBoard[row-4, col-4] == ID and \
                    parentBoard[row-5, col-5] == 0:
                    childBoard = parentBoard.copy()
                    childBoard[row, col] = ID
                    childBoards.append(childBoard)
                    patternFound = True

        # immediately block if opponent has 3 in a row
        # scan horizontally left to right
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE-4):
                if parentBoard[row, col] == 0 and parentBoard[row, col+1] == opponentID and \
                    parentBoard[row, col+2] == opponentID and parentBoard[row, col+3] == opponentID and \
                    parentBoard[row, col+4] == 0:
                    childBoard1 = parentBoard.copy()
                    childBoard1[row, col] = ID
                    childBoards.append(childBoard1)
                    patternFound = True
         # scan vertially top to bottom
        for row in range(BOARD_SIZE-4):
            for col in range(BOARD_SIZE):
                if parentBoard[row, col] == 0 and parentBoard[row+1, col] == opponentID and \
                    parentBoard[row+2, col] == opponentID and parentBoard[row+3, col] == opponentID and \
                    parentBoard[row+4, col] == 0:
                    childBoard1 = parentBoard.copy()
                    childBoard1[row, col] = ID
                    childBoards.append(childBoard1)
                    patternFound = True
        # # scan diagonally left to right
        for row in range(BOARD_SIZE-4):
            for col in range(BOARD_SIZE-4):
                if parentBoard[row, col] == 0 and parentBoard[row+1, col+1] == ID and \
                    parentBoard[row+2, col+2] == ID and parentBoard[row+3, col+3] == ID and \
                    parentBoard[row+4, col+4] == 0:
                    childBoard1 = parentBoard.copy()
                    childBoard1[row, col] = ID
                    childBoards.append(childBoard1)
                    patternFound = True
        # # scan diagonally right to left
        for row in reversed(range(BOARD_SIZE-4)):
            for col in reversed(range(BOARD_SIZE-4)):
                if parentBoard[row, col] == 0 and parentBoard[row-1, col-1] == ID and \
                    parentBoard[row-2, col-2] == ID and parentBoard[row-3, col-3] == ID and \
                    parentBoard[row-4, col-4] == 0:
                    childBoard1 = parentBoard.copy()
                    childBoard1[row, col] = ID
                    childBoards.append(childBoard1)
                    patternFound = True

        if not patternFound:
            while True:
                moveLoc = tuple(np.random.randint(BOARD_SIZE, size=2))
                if legalMove(parentBoard, moveLoc):
                    childBoard = parentBoard.copy()
                    childBoard[moveLoc] = ID
                    childBoards.append(childBoard)
                    break
            
        
        return childBoards

    # 0 1 1 1 1 0 if ID = 1
    # unobstructed 4 in a row
    @staticmethod
    def straightFourCount(board, ID):
        count = 0

        # scan horizontally left to right
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE-5): 
                if board[row, col] == 0 and board[row, col+1] == ID and \
                    board[row, col+2] == ID and board[row, col+3] == ID and board[row, col+4] == ID and \
                    board[row, col+5] == 0:
                    count +=1

        # scan vertially top to bottom
        for row in range(BOARD_SIZE-5):
            for col in range(BOARD_SIZE):
                if board[row, col] == 0 and board[row+1, col] == ID and \
                    board[row+2, col] == ID and board[row+3, col] == ID and board[row+4, col] == ID and \
                    board[row+5, col] == 0:
                    count +=1
        
        # scan diagonally left to right
        for row in range(BOARD_SIZE-5):
            for col in range(BOARD_SIZE-5):
                if board[row, col] == 0 and board[row+1, col+1] == ID and \
                    board[row+2, col+2] == ID and board[row+3, col+3] == ID and board[row+4, col+4] == ID and \
                    board[row+5, col+5] == 0:
                    count +=1

        # scan diagonally right to left
        for row in reversed(range(BOARD_SIZE-5)):
            for col in reversed(range(BOARD_SIZE-5)):
                if board[row, col] == 0 and board[row-1, col-1] == ID and \
                    board[row-2, col-2] == ID and board[row-3, col-3] == ID and board[row-4, col-4] == ID and \
                    board[row-5, col-5] == 0:
                    count +=1

        return count

    # 0 1 1 1 0 if ID = 1
    # unobstructed 3 in a row
    @staticmethod
    def straightThreeCount(board, ID):
        count = 0

        # scan horizontally left to right
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE-4):
                if board[row, col] == 0 and board[row, col+1] == ID and \
                    board[row, col+2] == ID and board[row, col+3] == ID and \
                    board[row, col+4] == 0:
                    count +=1

        # scan vertially top to bottom
        for row in range(BOARD_SIZE-4):
            for col in range(BOARD_SIZE):
                if board[row, col] == 0 and board[row+1, col] == ID and \
                    board[row+2, col] == ID and board[row+3, col] == ID and \
                    board[row+4, col] == 0:
                    count += 1

        # scan diagonally left to right
        for row in range(BOARD_SIZE-4):
            for col in range(BOARD_SIZE-4):
                if board[row, col] == 0 and board[row+1, col+1] == ID and \
                    board[row+2, col+2] == ID and board[row+3, col+3] == ID and \
                    board[row+4, col+4] == 0:
                    count +=1

        # scan diagonally right to left
        for row in reversed(range(BOARD_SIZE-4)):
            for col in reversed(range(BOARD_SIZE-4)):
                if board[row, col] == 0 and board[row-1, col-1] == ID and \
                    board[row-2, col-2] == ID and board[row-3, col-3] == ID and \
                    board[row-4, col-4] == 0:
                    count +=1

        return count

    # -1 1 1 1 1 0 or 0 1 1 1 1 -1 if ID = 1
    # 4 in a row obsrructed on only one side
    @staticmethod
    def fourInARowCount(board, ID):
        count = 0
        opponentID = ID * -1

        # scan horizontally left to right
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE-5): 
                if board[row, col] == opponentID and board[row, col+1] == ID and \
                    board[row, col+2] == ID and board[row, col+3] == ID and board[row, col+4] == ID and \
                    board[row, col+5] == 0:
                    count +=1

                if board[row, col] == ID and board[row, col+1] == ID and \
                    board[row, col+2] == ID and board[row, col+3] == ID and board[row, col+4] == ID and \
                    board[row, col+5] == opponentID:
                    count +=1

        # scan vertially top to bottom
        for row in range(BOARD_SIZE-5):
            for col in range(BOARD_SIZE):
                if board[row, col] == opponentID and board[row+1, col] == ID and \
                    board[row+2, col] == ID and board[row+3, col] == ID and board[row+4, col] == ID and \
                    board[row+5, col] == 0:
                    count +=1

                if board[row, col] == 0 and board[row+1, col] == ID and \
                    board[row+2, col] == ID and board[row+3, col] == ID and board[row+4, col] == ID and \
                    board[row+5, col] == opponentID:
                    count +=1
        
        # scan diagonally left to right
        for row in range(BOARD_SIZE-5):
            for col in range(BOARD_SIZE-5):
                if board[row, col] == opponentID and board[row+1, col+1] == ID and \
                    board[row+2, col+2] == ID and board[row+3, col+3] == ID and board[row+4, col+4] == ID and \
                    board[row+5, col+5] == 0:
                    count +=1

                if board[row, col] == 0 and board[row+1, col+1] == ID and \
                    board[row+2, col+2] == ID and board[row+3, col+3] == ID and board[row+4, col+4] == ID and \
                    board[row+5, col+5] == opponentID:
                    count +=1

        # scan diagonally right to left
        for row in reversed(range(BOARD_SIZE-5)):
            for col in reversed(range(BOARD_SIZE-5)):
                if board[row, col] == opponentID and board[row-1, col-1] == ID and \
                    board[row-2, col-2] == ID and board[row-3, col-3] == ID and board[row-4, col-4] == ID and \
                    board[row-5, col-5] == 0:
                    count +=1

                if board[row, col] == 0 and board[row-1, col-1] == ID and \
                    board[row-2, col-2] == ID and board[row-3, col-3] == ID and board[row-4, col-4] == ID and \
                    board[row-5, col-5] == opponentID:
                    count +=1
            
        return count

    # 0 1 0 1 1  or 1 1 0 1 0 if ID = 1
    @staticmethod
    def brokenThreeCount(board, ID):
        count = 0

        # scan horizontally left to right
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE-4): 
                if board[row, col] == 0 and board[row, col+1] == ID and \
                    board[row, col+2] == 0 and board[row, col+3] == ID and board[row, col+4] == ID:
                    count +=1

                if board[row, col] == ID and board[row, col+1] == ID and \
                    board[row, col+2] == 0 and board[row, col+3] == ID and board[row, col+4] == 0:
                    count +=1

        # scan vertially top to bottom 
        for row in range(BOARD_SIZE-4):
            for col in range(BOARD_SIZE):
                if board[row, col] == 0 and board[row+1, col] == ID and \
                    board[row+2, col] == 0 and board[row+3, col] == ID and board[row+4, col] == ID:
                    count +=1

                if board[row, col] == ID and board[row+1, col] == ID and \
                    board[row+2, col] == 0 and board[row+3, col] == ID and board[row+4, col] == 0:
                    count +=1
        
        # scan diagonally left to right
        for row in range(BOARD_SIZE-4):
            for col in range(BOARD_SIZE-4):
                if board[row, col] == 0 and board[row+1, col+1] == ID and \
                    board[row+2, col+2] == 0 and board[row+3, col+3] == ID and board[row+4, col+4] == ID:
                    count +=1

                if board[row, col] == ID and board[row+1, col+1] == ID and \
                    board[row+2, col+2] == 0 and board[row+3, col+3] == ID and board[row+4, col+4] == 0:
                    count +=1

        # scan diagonally right to left 
        for row in reversed(range(BOARD_SIZE-4)):
            for col in reversed(range(BOARD_SIZE-4)):
                if board[row, col] == 0 and board[row-1, col-1] == ID and \
                    board[row-2, col-2] == 0 and board[row-3, col-3] == ID and board[row-4, col-4] == ID:
                    count +=1

                if board[row, col] == ID and board[row-1, col-1] == ID and \
                    board[row-2, col-2] == 0 and board[row-3, col-3] == ID and board[row-4, col-4] == 0:
                    count +=1
            
        return count

    # 0 1 1 0 if ID = 1
    @staticmethod
    def twoInARow(board, ID):
        count = 0

        # scan horizontally left to right
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE-3):
                if board[row, col] == 0 and board[row, col+1] == ID and \
                    board[row, col+2] == ID and board[row, col+3] == 0:
                    count +=1

        # scan vertially top to bottom
        for row in range(BOARD_SIZE-3):
            for col in range(BOARD_SIZE):
                if board[row, col] == 0 and board[row+1, col] == ID and \
                    board[row+2, col] == ID and board[row+3, col] == 0:
                    count += 1

        # scan diagonally left to right
        for row in range(BOARD_SIZE-3):
            for col in range(BOARD_SIZE-3):
                if board[row, col] == 0 and board[row+1, col+1] == ID and \
                    board[row+2, col+2] == ID and board[row+3, col+3] == 0:
                    count +=1

        # scan diagonally right to left
        for row in reversed(range(BOARD_SIZE-3)):
            for col in reversed(range(BOARD_SIZE-3)):
                if board[row, col] == 0 and board[row-1, col-1] == ID and \
                    board[row-2, col-2] == ID and board[row-3, col-3] == 0:
                    count +=1

        return count

    # 0 1 0 1 0 if ID = 1
    # possible to convert into straight three 0 1 1 1 0
    @staticmethod
    def brokenTwoInARow(board, ID):
        count = 0

        # scan horizontally left to right
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE-4): 
                if board[row, col] == 0 and board[row, col+1] == ID and \
                    board[row, col+2] == 0 and board[row, col+3] == ID and board[row, col+4] == 0:
                    count +=1

        # scan vertially top to bottom 
        for row in range(BOARD_SIZE-4):
            for col in range(BOARD_SIZE):
                if board[row, col] == 0 and board[row+1, col] == ID and \
                    board[row+2, col] == 0 and board[row+3, col] == ID and board[row+4, col] == 0:
                    count +=1
        
        # scan diagonally left to right
        for row in range(BOARD_SIZE-4):
            for col in range(BOARD_SIZE-4):
                if board[row, col] == 0 and board[row+1, col+1] == ID and \
                    board[row+2, col+2] == 0 and board[row+3, col+3] == ID and board[row+4, col+4] == 0:
                    count +=1

        # scan diagonally right to left 
        for row in reversed(range(BOARD_SIZE-4)):
            for col in reversed(range(BOARD_SIZE-4)):
                if board[row, col] == 0 and board[row-1, col-1] == ID and \
                    board[row-2, col-2] == 0 and board[row-3, col-3] == ID and board[row-4, col-4] == 0:
                    count +=1
            
        return count

    @staticmethod
    def singleCount(board, ID):
        count = 0

        # for row in range(BOARD_SIZE):
        #     for col in range(BOARD_SIZE):
        #         if 
        return count

    
    # Its static evaluator - behaves in only one way, independent of who is playing
    # Evaluation function only identify and weigh patterns of our PlayerID
    # The higher the eval number, the board has lot of  potential wiinning sequences
    # for us which is good for us, bad for opponent
    # The lower the eval number, the board has less potential wiinning sequences
    # which is good for opponent, bad for us
    # Find patterns straightFour, four-in-a-row, three-in-a-row, broken-three, two-in-a-row, broken two in a row, single
    
    def hFunction(self, board):
        PlayerID = self.ID
        opponentID = PlayerID * -1

        if winningTest(PlayerID, board, X_IN_A_LINE):
            return +100
        if winningTest(opponentID, board, X_IN_A_LINE):
            return -100

        base = 2
        val = (Player.straightFourCount(board, PlayerID) * pow(base, 4) * 1.2 + \
              Player.fourInARowCount(board, PlayerID) * pow(base, 4) + \
              Player.straightThreeCount(board, PlayerID) * pow(base, 3) + \
              Player.brokenThreeCount(board, PlayerID) * pow(base, 3) + \
              Player.twoInARow(board, PlayerID) * pow(base, 2) + 
              Player.brokenTwoInARow(board, PlayerID) + 
              Player.singleCount(board, PlayerID)) \
              - \
              (Player.straightFourCount(board, opponentID) * pow(base, 4) * 1.2 + \
              Player.fourInARowCount(board, opponentID) * pow(base, 4) + \
              Player.straightThreeCount(board, opponentID) * pow(base, 3) + \
              Player.brokenThreeCount(board, opponentID) * pow(base, 3) + \
              Player.twoInARow(board, opponentID) * pow(base, 2) +
              Player.brokenTwoInARow(board, opponentID) +
              Player.singleCount(board, opponentID)) 

        return val