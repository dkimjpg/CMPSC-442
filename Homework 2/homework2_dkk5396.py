############################################################
# CMPSC 442: Informed Search
############################################################

student_name = "David Kim"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math
import random
from itertools import permutations


############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols): #check if I made this right
    if rows == 0 and cols == 0:
        return TilePuzzle([])
    makeBoard = []
    for m in range(0, rows):
        rowList = []
        for n in range(1, cols + 1):
            if m == rows - 1 and n == cols:
                rowList.append(0)
            else:
                rowList.append(n + (m * cols))
        makeBoard.append(rowList)
    
    finalBoard = TilePuzzle(makeBoard)
    return finalBoard
    #pass

class TilePuzzle(object):
    
    # Required
    def __init__(self, board):
        self.board = board
        if board != []:
            self.boardRowLength = len(board)     #m rows 
            self.boardColLength = len(board[0])  #n columns
        #pass

    def get_board(self):
        return self.board
        #pass
    
    def get_empty_tile(self):
        currentBoard = self.get_board().copy()
        boardRow = self.boardRowLength
        boardCol = self.boardColLength
        for r in range(0, boardRow):
            for c in range(0, boardCol):
                if currentBoard[r][c] == 0:
                    return (r, c)            #tuple that contains (row, col)

    def perform_move(self, direction):
        emptyTile = self.get_empty_tile() #finds the empty tile
        #print(emptyTile)                 #prints location of the empty tile
        tileRow = emptyTile[0]
        tileCol = emptyTile[1]
        #tileRow = len(self.get_board()) - 1
        #tileCol = len(self.get_board()[0]) - 1
        if direction == "up":
            if tileRow - 1 >= 0: #check if this and all the others are done right
                storeTile = self.board[tileRow - 1][tileCol]
                self.board[tileRow][tileCol] = storeTile
                self.board[tileRow - 1][tileCol] = 0
                return True
            else:
                return False
        elif direction == "down":
            if tileRow + 1 < self.boardRowLength:
                storeTile = self.board[tileRow + 1][tileCol]
                self.board[tileRow][tileCol] = storeTile
                self.board[tileRow + 1][tileCol] = 0
                return True
            else:
                return False
        elif direction == "left":
            if tileCol - 1 >= 0:
                storeTile = self.board[tileRow][tileCol - 1]
                self.board[tileRow][tileCol] = storeTile
                self.board[tileRow][tileCol - 1] = 0
                return True
            else:
                return False
        elif direction == "right":
            if tileCol + 1 < self.boardColLength:
                storeTile = self.board[tileRow][tileCol + 1]
                self.board[tileRow][tileCol] = storeTile
                self.board[tileRow][tileCol + 1] = 0
                return True
            else:
                return False
        else:
            return False
        #pass

    def scramble(self, num_moves):
        for i in range(0, num_moves):
            move = random.random()
            if move < 0.25:
                self.perform_move("up")
            elif move >= 0.25 and move < 0.5:
                self.perform_move("down")
            elif move >= 0.5 and move < 0.75:
                self.perform_move("left")
            elif move >= 0.75:
                self.perform_move("down")
        #pass

    def is_solved(self):
        if self.get_board() == []:
            return False
        for m in range(0, self.boardRowLength):
            for n in range(0, self.boardColLength):
                if self.get_board()[m][n] == True:
                    return False
        #pass

    def copy(self):
        #makeCopy = create_puzzle(self.boardRowLength, self.boardColLength)            #use this instead if the next line fails sometime in the future
        makeCopy = [[False] * self.boardColLength for i in range(0, self.boardRowLength)] #makes a 2d list filled with only False, it's like create_puzzle, but faster (sort of). Need to start with Column length, then Row length
        boardCopy = TilePuzzle(makeCopy)
        for m in range(0, self.boardRowLength):
            for n in range(0, self.boardColLength):
                boardCopy.board[m][n] = self.board[m][n]
        return boardCopy
        #pass

    def successors(self):
        listOfTuples = []                                 #create empty list that takes the tuples that will be made, this will be converted into a tuple later
        #listOfTuples = [0] * (self.boardRowLength * self.boardColLength) #use this in case the previous line doesn't work, also replace the listOfTuples.append() in the following for loops.
        currentBoard = TilePuzzle(self.board).copy() #this NEEDS to be set as a LightsOutPuzzle, I spent hours trying to figure out why self.board and self.board.copy() didn't work. The copy() only works with LightsOutPuzzle() data types.

        for m in range(0, self.boardRowLength):
            for n in range(0, self.boardColLength):
                move = (m, n)                                        #create move tuple
                copyCurrentBoard = currentBoard.copy()               #check if this is a Board or a List, it needs to be a Board, so cast it into a Board if it is not
                copyCurrentBoard.perform_move(m, n)                  #might want to check if it actually performed the move.
                successorBoard = copyCurrentBoard
                successorTuple = (move, successorBoard)
                listOfTuples.append(successorTuple)
                
        tupleOfTuples = tuple(listOfTuples)            #convert the list into a tuple by casting it into a tuple
        return tupleOfTuples
        #pass

    # Required
    def find_solutions_iddfs(self):
        pass

    # Required
    def find_solution_a_star(self):
        pass

############################################################
# Section 2: Grid Navigation
############################################################

def find_path(start, goal, scene):
    pass

############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

def solve_distinct_disks(length, n):
    pass

############################################################
# Section 4: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    pass

class DominoesGame(object):

    # Required
    def __init__(self, board):
        pass

    def get_board(self):
        pass

    def reset(self):
        pass

    def is_legal_move(self, row, col, vertical):
        pass

    def legal_moves(self, vertical):
        pass

    def perform_move(self, row, col, vertical):
        pass

    def game_over(self, vertical):
        pass

    def copy(self):
        pass

    def successors(self, vertical):
        pass

    def get_random_move(self, vertical):
        pass

    # Required
    def get_best_move(self, vertical, limit):
        pass

############################################################
# Tests

# MAKE SURE TO COMMENT OUT WHEN SUBMITTING <---------------------------------------------------------------------------------------

############################################################

#TilePuzzle Infrastructure Tests
print("TilePuzzle Infrastructure Tests")
print("getBoard")
p = TilePuzzle([[1, 2], [3, 0]])
print(p.get_board())
p = TilePuzzle([[0, 1], [3, 2]])
print(p.get_board())

print("\ncreate_tile_puzzle")
p = create_tile_puzzle(3, 3) 
print(p.get_board())
p = create_tile_puzzle(2, 4)
print(p.get_board())

print("\nperform_move")
p = create_tile_puzzle(3, 3) 
print(p.perform_move("up"))
print(p.get_board())
p = create_tile_puzzle(3, 3) 
print( p.perform_move("down"))
print(p.get_board())

print("\nscramble")
scrambleTest1 = create_tile_puzzle(3, 3)
scrambleTest1.scramble(1)
print(scrambleTest1.get_board())
scrambleTest1.scramble(1)
print(scrambleTest1.get_board())