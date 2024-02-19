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
from queue import PriorityQueue


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
            failedMoves = []
            if move < 0.25:
                self.perform_move("up")                
                """
                worked = self.perform_move("up")
                if worked == False:  #intended to test whether or not the move was valid, if invalid, reroll
                    failedMoves.append("up")
                    while move < 0.25:
                        move = random.random()
                """
            if move >= 0.25 and move < 0.5:
                self.perform_move("down")
                """
                if worked == False:
                    i = i - 1
                """
            if move >= 0.5 and move < 0.75:
                self.perform_move("left")
                """
                if worked == False:
                    i = i - 1
                """
            if move >= 0.75:
                self.perform_move("down")
                """
                if worked == False:
                    i = i - 1
                """
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
    
    def testIfPossible(self, move):
        testBoard = TilePuzzle(self.get_board()).copy()
        testMove = testBoard.perform_move(move)
        return testMove

    def successors(self):
        listOfTuples = []                                 #create empty list that takes the tuples that will be made, this will be converted into a tuple later
        #listOfTuples = [0] * (self.boardRowLength * self.boardColLength) #use this in case the previous line doesn't work, also replace the listOfTuples.append() in the following for loops.
        currentBoard = TilePuzzle(self.board).copy() #this NEEDS to be set as a LightsOutPuzzle, I spent hours trying to figure out why self.board and self.board.copy() didn't work. The copy() only works with LightsOutPuzzle() data types.

        upTest = currentBoard.testIfPossible("up")
        downTest = currentBoard.testIfPossible("down")
        leftTest = currentBoard.testIfPossible("left")
        rightTest = currentBoard.testIfPossible("right")

        if upTest == True:
            move = "up"
            copyCurrentBoard = currentBoard.copy()
            copyCurrentBoard.perform_move(move)
            successorTuple = (move, copyCurrentBoard)
            listOfTuples.append(successorTuple)
        
        if downTest == True:
            move = "down"
            copyCurrentBoard = currentBoard.copy()
            copyCurrentBoard.perform_move(move)
            successorTuple = (move, copyCurrentBoard)
            listOfTuples.append(successorTuple)

        if leftTest == True:
            move = "left"
            copyCurrentBoard = currentBoard.copy()
            copyCurrentBoard.perform_move(move)
            successorTuple = (move, copyCurrentBoard)
            listOfTuples.append(successorTuple)
        
        if rightTest == True:
            move = "right"
            copyCurrentBoard = currentBoard.copy()
            copyCurrentBoard.perform_move(move)
            successorTuple = (move, copyCurrentBoard)
            listOfTuples.append(successorTuple)


        """
        for m in range(0, self.boardRowLength):
            for n in range(0, self.boardColLength):
                move = (m, n)                                        #create move tuple
                copyCurrentBoard = currentBoard.copy()               #check if this is a Board or a List, it needs to be a Board, so cast it into a Board if it is not
                copyCurrentBoard.perform_move(m, n)                  #might want to check if it actually performed the move.
                successorBoard = copyCurrentBoard
                successorTuple = (move, successorBoard)
                listOfTuples.append(successorTuple)
        """
                
        tupleOfTuples = tuple(listOfTuples)            #convert the list into a tuple by casting it into a tuple
        return tupleOfTuples
        #pass

    def iddfs_helper(self, limit, moves): #yields all solutions to the current board of length no more than  limit which are continuations of the provided move list.
        #this method should be recursive since it has to increase the limit at each level
        #I think that moves is supposed to be the current list (or whatever I used to collect the moves) of moves that I need to test to see if they yield anything
        #Actually, moves is supposed to be a list of strings that contain the all the moves leading up to the current board
        currentBoard = TilePuzzle(self.get_board()).copy()
        if limit < 0: #think something's wrong with this
            return False
        
        #from here, I should probably iterate through moves and use recursion to explore each move's possible moves until the limit is reached.
        if currentBoard.is_solved() == True:
            return moves
        for i in range(0, limit + 1):
            if currentBoard.testIfPossible("up") == True:
                upBoard = TilePuzzle(currentBoard.get_board()).copy()
                upBoard.perform_move("up")
                moveList = moves.append("up")
                if upBoard.iddfs_helper(limit - 1, moveList) == False:
                    moveList.pop()
            if currentBoard.testIfPossible("down") == True:
                upBoard = TilePuzzle(currentBoard.get_board()).copy()
                upBoard.perform_move("down")
                moveList = moves.append("down")
                if upBoard.iddfs_helper(limit - 1, moveList) == False:
                    moveList.pop()
            if currentBoard.testIfPossible("left") == True:
                upBoard = TilePuzzle(currentBoard.get_board()).copy()
                upBoard.perform_move("left")
                moveList = moves.append("left")
                if upBoard.iddfs_helper(limit - 1, moveList) == False:
                    moveList.pop()
            if currentBoard.testIfPossible("right") == True:
                upBoard = TilePuzzle(currentBoard.get_board()).copy()
                upBoard.perform_move("right")
                moveList = moves.append("right")
                if upBoard.iddfs_helper(limit - 1, moveList) == False:
                    moveList.pop()
            
            #if self.iddfs_helper(limit - i, ): #don't think I'll need this
            #    return
        print("delete this print statement 1")


    # Required
    def find_solutions_iddfs(self):
        """
        How IDDFS (Iterative Deepening Depth-First Search) works:
        Run DFS, but only to a certain limit of levels. Start from depth limit 0, and each time that the goal node is not found, increment the depth limit.
        For each depth limit, DFS is running until the goal node is found. 
        This takes longer than BFS, but uses up less space. This is also faster than DFS.
        """
        limit = 0
        moves = []
        while(True): #assuming the board is solvable
            self.iddfs_helper(limit, moves)
            if len(moves) != 0:                  #if moves list is not empty, then the solution has been found, return the list of moves
                return moves                     #come up with something for the list of moves
            limit = limit + 1
        
        print("got out of while loop")
        return False #just putting this here so something is outputted at the end somehow
        #pass

    # Required
    def find_solution_a_star(self):
        """
        Create a list that should contain the current board, then create an infinite while loop. 
        Within that while loop, make a for loop that iterates through all elements in the list with the boards.
        For each iteration, look at all possible moves while ignoring any backwards moves (these are moves that reverse progress, like moving down if the previous move was up)
            May want to make a helper function that checks if any possible moves are backwards.
        For all possible moves, create a copy of the board and perform the move. Then get the Manhattan Distance of each tile and get the sum of all Manhattan Distances on the board.
            May also want to make a helper function that gets the sum of all Manhattan Distances (probably should send the whole board to the function, return a number)
        Next, get the following stats, (sum of Manhattan Distances, path(should be a list of strings),  move(should be a string)), and put this tuple in a list (or priority queue)
        Go through the list and find the board with the smallest sum of Depth and Manhattan Distance (or use a priority queue and use .get() to get the smallest sum)
        Once the board is found, add it to the list. Check if the board is solved, and if it is, return the path that was taken to get to it.
        Otherwise, the algorithm goes back to the beginning of the while loop.
        """

        
        #pass

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

print("\nis_solved")
p = TilePuzzle([[1, 2], [3, 0]])
print(p.is_solved())
p = TilePuzzle([[0, 1], [3, 2]])
print(p.is_solved())

print("\ncopy")
p = create_tile_puzzle(3, 3) 
p2 = p.copy()
print(p.get_board() == p2.get_board())
p = create_tile_puzzle(3, 3)
p2 = p.copy()
p.perform_move("left")
print(p.get_board() == p2.get_board())

print("\nsuccessors")
p = create_tile_puzzle(3, 3)
for move, new_p in p.successors():
    print(move, new_p.get_board())
print("")
b = [[1,2,3], [4,0,5], [6,7,8]] 
p = TilePuzzle(b)
for move, new_p in p.successors():
    print(move, new_p.get_board())