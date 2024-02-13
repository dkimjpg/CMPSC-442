############################################################
# CMPSC 442: Uninformed Search
############################################################

student_name = "David Kim"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math
import random
from itertools import permutations
from collections import deque #may or may not need this

############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    squared = n * n
    numOfComb = math.comb(squared, n) #math combination, would look like: (n^2)C(n)
    #print(numOfComb)
    return numOfComb
    #pass

def num_placements_one_per_row(n):
    numOfPlacements = n ** n #assuming that this does exponents properly
    #print(numOfPlacements)
    return numOfPlacements
    #pass

def n_queens_valid(board):
    lengthBoard = len(board)
    for i in board: #i will iterate through the board, representing the queen that is currently placed
        count = i + 1
        for x in range(count, lengthBoard): #x will be compared to i to see if the next queen is invalidly placed, and if so, return False
            if board[i] == board[x]:
                #print("error 1")
                return False
            distance = abs(x - i)
            if board[i] + distance == board[x]:
                #print("error 2")
                return False
            if board[i] - distance == board[x]:
                #print("error 3")
                return False
    #assuming that the entire board is valid after all the checks
    return True

    #pass

def n_queens_helper(board):
    if n_queens_valid(board) == True:
        #yield board #not sure if yield works here, the way I coded it might be wrong
        return board
    else:
        return False
    #pass

def n_queens_solutions(n): 
    #maybe use the combinations from itertools to generate all the possible combinations of lists, then feed all those lists 
    #into n_queens_valid with a for loop, or maybe make a new function that has n_queens_valid, but yields at the end instead,
    #that way, I can get every single valid list that way.
    #boardList = [*range(0, n)]
    #print(n)
    boardList = [*range(0,n)]
    #print(boardList)
    allBoards = list(permutations(boardList, n)) #allboards is a list of all possible arrangements of the board, so it is basically a list of lists
    #print(allBoards)
    solutions = []
    
    for currentBoard in allBoards:
        testBoard = n_queens_helper(currentBoard)
        if testBoard != False:
            yield testBoard
            solutions.append(testBoard)
        #print(n_queens_helper(currentBoard))
    
    #return solutions #not sure if I'm supposed to return this or just use only the yields...
    #pass

############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board                       #m x n grid
        if board != []:
            self.boardRowLength = len(board)     #m rows 
            self.boardColLength = len(board[0])  #n columns
        #pass

    def get_board(self):
        return self.board
        #pass

    def perform_move(self, row, col):
        currentBoard = self.board 
        if self.board == []: #this might also cause problems, it was designed to get rid of empty boards
            pass
        elif row < self.boardRowLength and col < self.boardColLength:  #this could cause some problems later, check this in case by printing self.boardRowLength and row (and vice versa)
            #the selected light should always be toggled.
            currentBoard[row][col] = not currentBoard[row][col]
            
            #check all four neighbors if they exist and toggle if they exist
            if row - 1 >= 0:
                currentBoard[row - 1][col] = not currentBoard[row - 1][col]
            if col - 1 >= 0:
                currentBoard[row][col - 1] = not currentBoard[row][col - 1]
            if row + 1 < self.boardRowLength:
                currentBoard[row + 1][col] = not currentBoard[row + 1][col]
            if col + 1 < self.boardColLength:
                currentBoard[row][col + 1] = not currentBoard[row][col + 1]
        #pass

    def scramble(self): 
        #test this sometime in the future, I just don't know how to right now. I should probably just make a board and then just print 
        #the output of scramble once. Then do print the output of scramble again to check if it's truly random.
        for m in range(0, self.boardRowLength):
            for n in range(0, self.boardColLength):
                """
                print("toggled {0},{1}".format(m,n))
                print(self.board)
                self.perform_move(m,n)
                print(self.board)
                print("")
                """                
                if random.random() < 0.5:
                    #print("")
                    #print("toggled {0},{1}".format(m,n))
                    #print(self.board)
                    self.perform_move(m, n)
                    #print(self.board)                
        #pass

    def is_solved(self): #takes in a LightsOffPuzzle object, not a list
        if self.get_board() == []:
            return False
        for m in range(0, self.boardRowLength):
            for n in range(0, self.boardColLength):
                if self.get_board()[m][n] == True:
                    return False
        
        #print(self.get_board()) #testing

        return True
        #pass

    def copy(self):
        #makeCopy = create_puzzle(self.boardRowLength, self.boardColLength)            #use this instead if the next line fails sometime in the future
        makeCopy = [[False] * self.boardColLength for i in range(0, self.boardRowLength)] #makes a 2d list filled with only False, it's like create_puzzle, but faster (sort of). Need to start with Column length, then Row length
        boardCopy = LightsOutPuzzle(makeCopy)
        #print(boardCopy.get_board())
        for m in range(0, self.boardRowLength):
            for n in range(0, self.boardColLength):
                #print("/--\\")
                #print("({}, {})".format(m, n))
                #print("row:{} Col:{}".format(self.boardRowLength, self.boardColLength))
                #print(boardCopy.board[m][n])
                #print("===")
                boardCopy.board[m][n] = self.board[m][n]
                #print(boardCopy.board[m][n])
                #print("\\--/")
        #print("whattypeisthis")
        #print(type(boardCopy))
        return boardCopy

        #pass

    def successors(self):
        listOfTuples = []                                 #create empty list that takes the tuples that will be made, this will be converted into a tuple later
        #listOfTuples = [0] * (self.boardRowLength * self.boardColLength) #use this in case the previous line doesn't work, also replace the listOfTuples.append() in the following for loops.
        currentBoard = LightsOutPuzzle(self.board).copy() #this NEEDS to be set as a LightsOutPuzzle, I spent hours trying to figure out why self.board and self.board.copy() didn't work. The copy() only works with LightsOutPuzzle() data types.
        #counter = 0

        for m in range(0, self.boardRowLength):
            for n in range(0, self.boardColLength):
                move = (m, n)                                        #create move tuple
                copyCurrentBoard = currentBoard.copy()               #check if this is a Board or a List, it needs to be a Board, so cast it into a Board if it is not
                copyCurrentBoard.perform_move(m, n)                  #might want to check if it actually performed the move.
                successorBoard = copyCurrentBoard
                successorTuple = (move, successorBoard)
                listOfTuples.append(successorTuple)

                #use the following (besides the print statments) if appending to listOfTuples doesn't work
                #listOfTuples[counter] = successorTuple
                #print(listOfTuples)
                #counter = counter + 1
                #print(counter)
                
        tupleOfTuples = tuple(listOfTuples)            #convert the list into a tuple by casting it into a tuple
        return tupleOfTuples
        #pass

    def find_solution(self):
        if self.board == []: #tests if board is empty, check this to make sure it doesn't break anything
            return None
        if LightsOutPuzzle(self.board).is_solved() == True: #if the current board is not solvable, return None
            return None
        frontierList = [] #frontier list will be made up of tuples that have (move(), LightsOutPuzzle board, path[])
        exploredSet = set() #stores visited boards so the same board is not visited twice
        firstBoard = LightsOutPuzzle(self.board).copy()
        firstBoardTup = ((-1, -1), firstBoard, []) #used (-1, -1) as the move for the first tuple since I just need a place holder. The tuple is (move(), board, path[]), with the path being an empty list for the first board
        frontierList.append(firstBoardTup)
        #successList = firstBoard.successors()
        
        while(True):
            if not frontierList: #if frontierList is empty, return None
                return None
            currentBoardTup = frontierList.pop(0) #pops the first entry from the frontierList (should be a LightsOutPuzzle), also currentBoardTup should be the following: (move, board, path)
            currentMove = currentBoardTup[0]
            #currentBoard = currentBoardTup[1]
            currentPath = currentBoardTup[2]
            exploredSet.add(tuple(map(tuple, currentBoardTup[1].get_board())))   #converted it from a 2d list to a 2d tuple, otherwise it gives a hash error and won't properly put things into a set. I was stuck on this for hours...
            #print(frontierList) #want to check if pop actually removed it
            successTups = currentBoardTup[1].successors() #currentBoardTup[1] should be the LightsOutPuzzle board
            for childNode in successTups:  #each childNode will be a tuple of the following: (move, LightsOutPuzzle board)
                childMove = childNode[0]   #move of current childNode
                childBoard = childNode[1]  #LightsOutPuzzle board of current childNode                
                if childMove != currentMove:
                    childPath = currentPath.copy() #need to find a way so that I append to the original path, instead of just adding on the current node to the previous node
                    childPath.append(childMove)
                    childFrontier = (childMove, childBoard, childPath)
                    if childBoard.is_solved() == True:
                        return childPath #should return a list of the path to the current childNode and append the current move to the path list
                    dontappendchildfrontier = False
                    if tuple(map(tuple,childBoard.get_board())) in exploredSet:
                        dontappendchildfrontier = True
                    for frontiers in frontierList:
                        if childBoard.get_board() == frontiers[1].get_board():
                            dontappendchildfrontier = True
                    if dontappendchildfrontier == False: #checks if child is not in frontier list
                        frontierList.append(childFrontier)
                    
        #return None
        #pass

def create_puzzle(rows, cols):
    if rows == 0 and cols == 0:
        return LightsOutPuzzle([])
    makeBoard = []
    for m in range(0, rows):
        rowList = []
        for n in range(0, cols):
            rowList.append(False)
        makeBoard.append(rowList)
    finalBoard = LightsOutPuzzle(makeBoard)
    return finalBoard
    #pass

############################################################
# Section 3: Linear Disk Movement
############################################################
class disk(object):
    
    def __init__(self, placement):
        self.placement = placement
        #pass

    def get_placement(self):
        return self.placement
    
    def move_disk(placement):
        return placement + 1
    
    def hop_disk(placement):
        return placement + 2

def compare_Lists(diskList, finishedDiskList):
    #if diskList.reverse() == finishedDiskList:
    if reversed(diskList) == finishedDiskList:
        return True

def leftMostDisk(diskList):
    for pos in diskList:
        if pos == "o":
            return pos

def checkMove(diskList, pos):
    if pos + 1 > len(diskList):
        return False
    if diskList[pos + 1] == "o":
        return False
    if diskList[pos + 1] == "_":
        return True
    
def checkHop(diskList, pos):
    if pos + 2 > len(diskList):
        return False
    if diskList[pos + 2] == "o":
        return False
    if diskList[pos + 2] == "_":
        return True

def solve_identical_disks(length, n):
    
    if length == n: #base case, if length is same as number of disks, it's already solved
        return []
    
    frontierList = []
    exploredSet = set()

    #create the list for the disks
    diskList = []
    for i in range(0,n):
        #print(i)
        diskList.append("o")
    for i in range(n, length):
        diskList.append("_")
    #print(diskList)
    finishedDiskList = diskList.copy()
    finishedDiskList.reverse()
    #print(finishedDiskList)
    diskTupleCombo = (diskList, [])

    frontierList.append(diskTupleCombo)

    while(True):
        if not frontierList: #if frontierList is empty, return None
            return None
        
        currentTupleCombo = frontierList.pop(0)
        currentDiskList = currentTupleCombo[0]
        currentPath = currentTupleCombo[1]
        exploredSet.add(tuple(map(tuple, currentDiskList)))        

        firstDiskPos = leftMostDisk(currentDiskList)
        for disk in currentDiskList:            
            #print(currentDiskList)

            if disk == "o":
                pos = currentDiskList.index(disk)
                #print("aaaaaaa")
                #print(pos)
                if checkMove(currentDiskList, pos) == True:
                    newDiskListMove = currentDiskList.copy()
                    newDiskListMove[pos] = "_"
                    newDiskListMove[pos + 1] = "o"
                    newDiskListMove = tuple(map(tuple, newDiskListMove))
                    movePath = currentPath.copy()
                    movePath.append((pos, pos + 1))

                    if newDiskListMove not in exploredSet:
                        dontappendthislist = False
                        for frontiers in frontierList:
                            if frontiers[0] == newDiskListMove: #the disk list is in frontiers, so don't append
                                dontappendthislist = True
                                                
                        if dontappendthislist == False:
                            if compare_Lists(newDiskListMove, finishedDiskList) == True:
                                return movePath
                            newDiskTupleMoveCombo = (newDiskListMove, movePath)
                            frontierList.append(newDiskTupleMoveCombo)
                if checkHop(currentDiskList, pos) == True:
                    newDiskListHop = currentDiskList.copy()
                    newDiskListHop[pos] = "_"
                    newDiskListHop[pos + 2] = "o"
                    newDiskListHop = tuple(map(tuple, newDiskListHop))
                    hopPath = currentPath.copy()
                    hopPath.append((pos, pos + 2))

                    if newDiskListHop not in exploredSet:
                        dontappendthislist = False
                        for frontiers in frontierList:
                            if frontiers[0] == newDiskListHop: #the disk list is in frontiers, so don't append
                                #print("a")
                                #print(frontiers[0])
                                #print(newDiskListHop)
                                dontappendthislist = True
                                                
                        if dontappendthislist == False:                            
                            if compare_Lists(newDiskListHop, finishedDiskList) == True:
                                return movePath
                            newDiskTupleHopCombo = (newDiskListHop, hopPath)
                            frontierList.append(newDiskTupleHopCombo)
            #else:


        """
        move = currentPos + 1
        hop = currentPos + 2
        
        diskSuccessors = (move, hop)
        adjacentDiskExists = False
        for i in diskSuccessors:
            if compare_Lists(currentDiskList, finishedDiskList) == True:
                return currentPath
            if diskList[i] == "_":
                adjacentDiskExists = True
                frontierList.append
        if diskList[currentPos + 1] == "o":
            adjacentDiskExists = True
        """
        

    #pass

def solve_distinct_disks(length, n):
    if length == n: #base case, if length is same as number of disks, it's already solved
        return []
    
    frontierList = []
    exploredSet = set()

    #create the list for the disks
    diskList = []
    for i in range(0,n):
        #print(i)
        diskList.append("o")
    for i in range(n, length):
        diskList.append("_")
    #print(diskList)
    finishedDiskList = diskList.copy()
    finishedDiskList.reverse()
    #print(finishedDiskList)
    diskTupleCombo = (diskList, [])

    frontierList.append(diskTupleCombo)

    while(True):
        if not frontierList: #if frontierList is empty, return None
            return None
        
        currentTupleCombo = frontierList.pop(0)
        currentDiskList = currentTupleCombo[0]
        currentPath = currentTupleCombo[1]
        exploredSet.add(tuple(map(tuple, currentDiskList)))        

        firstDiskPos = leftMostDisk(currentDiskList)
        for disk in currentDiskList:            
            #print(currentDiskList)

            if disk == "o":
                pos = currentDiskList.index(disk)
                #print("aaaaaaa")
                #print(pos)
                if checkMove(currentDiskList, pos) == True:
                    newDiskListMove = currentDiskList.copy()
                    newDiskListMove[pos] = "_"
                    newDiskListMove[pos + 1] = "o"
                    newDiskListMove = tuple(map(tuple, newDiskListMove))
                    movePath = currentPath.copy()
                    movePath.append((pos, pos + 1))

                    if newDiskListMove not in exploredSet:
                        dontappendthislist = False
                        for frontiers in frontierList:
                            if frontiers[0] == newDiskListMove: #the disk list is in frontiers, so don't append
                                dontappendthislist = True
                                                
                        if dontappendthislist == False:
                            if compare_Lists(newDiskListMove, finishedDiskList) == True:
                                return movePath
                            newDiskTupleMoveCombo = (newDiskListMove, movePath)
                            frontierList.append(newDiskTupleMoveCombo)
                if checkHop(currentDiskList, pos) == True:
                    newDiskListHop = currentDiskList.copy()
                    newDiskListHop[pos] = "_"
                    newDiskListHop[pos + 2] = "o"
                    newDiskListHop = tuple(map(tuple, newDiskListHop))
                    hopPath = currentPath.copy()
                    hopPath.append((pos, pos + 2))

                    if newDiskListHop not in exploredSet:
                        dontappendthislist = False
                        for frontiers in frontierList:
                            if frontiers[0] == newDiskListHop: #the disk list is in frontiers, so don't append
                                #print("a")
                                #print(frontiers[0])
                                #print(newDiskListHop)
                                dontappendthislist = True
                                                
                        if dontappendthislist == False:                            
                            if compare_Lists(newDiskListHop, finishedDiskList) == True:
                                return movePath
                            newDiskTupleHopCombo = (newDiskListHop, hopPath)
                            frontierList.append(newDiskTupleHopCombo)
    #pass


############################################################
# Tests

# MAKE SURE TO REMOVE WHEN SUBMITTING <---------------------------------------------------------------------------------------

############################################################
"""
# N-Queens Tests
print("N-Queens Tests")
print(num_placements_all(2))
print(num_placements_all(3))
print(num_placements_one_per_row(2))
print(num_placements_one_per_row(3))

print(n_queens_valid([0, 0]))
print(n_queens_valid([0, 2]))
print(n_queens_valid([0, 1]))
print(n_queens_valid([0, 3, 1]))

solutions = n_queens_solutions(4)
print(next(solutions))
print(next(solutions))
print(list(n_queens_solutions(6)))
print(len(list(n_queens_solutions(8))))

# Lights Out Tests
print("\nLights Out Tests")
print("1.")
b = [[True, False], [False, True]]
p = LightsOutPuzzle(b)
print(p.get_board())
b = [[True, True], [True, True]]
p = LightsOutPuzzle(b)
print(p.get_board())

print("2.")
createPuzzleTest = create_puzzle(2, 3)
print(createPuzzleTest.get_board())

print("3.")
performMoveTest1 = create_puzzle(3, 3)
performMoveTest1.perform_move(1, 1)
print(performMoveTest1.get_board())
performMoveTest2 = create_puzzle(3, 3)
performMoveTest2.perform_move(0, 0)
print(performMoveTest2.get_board())
performMoveTest3 = create_puzzle(1, 1) #board of 1x1
performMoveTest3.perform_move(0, 0)
print(performMoveTest3.get_board())
performMoveTest4 = create_puzzle(1, 1) #board of 1x1
performMoveTest4.perform_move(1, 1)    #invalid placement
print(performMoveTest4.get_board())
performMoveTest5 = create_puzzle(0, 0) #empty board
performMoveTest5.perform_move(0, 0)
print(performMoveTest5.get_board())

print("4.")
scrambleTest1 = create_puzzle(3, 3)
scrambleTest1.scramble()
print(scrambleTest1.get_board())
scrambleTest1.scramble()
print(scrambleTest1.get_board())

print("5.")
solvedPuzzleBoard1 = [[True, False], [False, True]]
solvedPuzzleTest1 = LightsOutPuzzle(solvedPuzzleBoard1)
print(solvedPuzzleTest1.is_solved())
solvedPuzzleBoard2 = [[False, False], [False, False]]
solvedPuzzleTest2 = LightsOutPuzzle(solvedPuzzleBoard2)
print(solvedPuzzleTest2.is_solved())
solvedPuzzleBoard3 = [] #empty board
solvedPuzzleTest3 = LightsOutPuzzle(solvedPuzzleBoard3)
print(solvedPuzzleTest3.is_solved()) #no lights to turn off, so return false

print("6.")
originalBoard1 = create_puzzle(3, 3)
copyBoard1 = originalBoard1.copy()
print(originalBoard1.get_board() == copyBoard1.get_board())
originalBoard2 = create_puzzle(3, 3)
copyBoard2 = originalBoard2.copy()
#print(originalBoard2.get_board())
#print(copyBoard2.get_board())
originalBoard2.perform_move(1, 1)
#print(originalBoard2.get_board())
#print(copyBoard2.get_board())
print(originalBoard2.get_board() == copyBoard2.get_board())

print("7.")
successorTest1 = create_puzzle(2, 2)
for move, new_p in successorTest1.successors():
    print(move, new_p.get_board())
for i in range(2, 6):
    successorTest2 = create_puzzle(i, i + 1)
    print(len(list(successorTest2.successors())))

print("8.")
p = create_puzzle(2, 3)
for row in range(2):
    for col in range(3):
        p.perform_move(row, col)
print(p.find_solution()) #need to find a way so it doesn't print all that crap, it only prints the true path, because the gui version is just following the crap pattern
#print("a")

b = [[False, False, False],[False, False, False]]
b[0][0] = True
#b[0][1] = True
#b[0][2] = True
#b[1][1] = True
p = LightsOutPuzzle(b)
print(p.find_solution() is None)

# Linear Disk Movement Tests
print("1.")
print(solve_identical_disks(4, 2))
"""