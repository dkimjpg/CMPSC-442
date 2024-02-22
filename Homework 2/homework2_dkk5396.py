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

def get2dCoords(boardList, target):
        for i, x in enumerate(boardList):
            if target in x:
                return (i, x.index(target))

def calculateReverseMove(move):
    if move == "up":
        return "down"
    if move == "down":
        return "up"
    if move == "left":
        return "right"
    if move == "right":
        return "left"

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
        count = 1
        for m in range(0, self.boardRowLength):
            for n in range(0, self.boardColLength):
                if m == self.boardRowLength - 1 and n == self.boardColLength - 1:
                    if self.get_board()[m][n] == 0:
                        return True
                    else:
                        return False
                if self.get_board()[m][n] != count:
                    return False
                count = count + 1
        #return True
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
                downBoard = TilePuzzle(currentBoard.get_board()).copy()
                downBoard.perform_move("down")
                moveList = moves.append("down")
                if downBoard.iddfs_helper(limit - 1, moveList) == False:
                    moveList.pop()
            if currentBoard.testIfPossible("left") == True:
                leftBoard = TilePuzzle(currentBoard.get_board()).copy()
                leftBoard.perform_move("left")
                moveList = moves.append("left")
                if leftBoard.iddfs_helper(limit - 1, moveList) == False:
                    moveList.pop()
            if currentBoard.testIfPossible("right") == True:
                rightBoard = TilePuzzle(currentBoard.get_board()).copy()
                rightBoard.perform_move("right")
                moveList = moves.append("right")
                if rightBoard.iddfs_helper(limit - 1, moveList) == False:
                    moveList.pop()
            
            #if self.iddfs_helper(limit - i, ): #don't think I'll need this
            #    return
        #print("delete this print statement 1")


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

    def getManhattanDistanceSum(self, board): 
        expectedBoardList = [[0 for x in range(self.boardRowLength)] for y in range(self.boardColLength)] #hopefully, this makes a 2d list of only 0 in every element. This makes it so I can start filling it out to make the expected board.
        #print("before making expected board")
        #print(expectedBoardList) #checking if it worked properly
        count = 1
        for m in range(0, self.boardRowLength):
            for n in range(0, self.boardColLength):
                if m == self.boardRowLength - 1 and n == self.boardColLength - 1: #for the last (bottom right) element of the 2d list, it should skip this and stay as 0
                    expectedBoardList[m][n] = 0
                else:
                    expectedBoardList[m][n] = count
                count = count + 1
        #print("after making expected board")
        #print(expectedBoardList) #checking again if it worked properly

        boardList = board.get_board()
        #print(boardList)
        totalSum = 0
        for m in range(0, self.boardRowLength):
            for n in range(0, self.boardColLength):
                boardNum = boardList[m][n] #value of current tile that needs to get the distance searched
                r1 = m
                c1 = n
                expectCoords = get2dCoords(expectedBoardList, boardNum) #looks for value of current tile in the expected board
                #print("boardNum:")
                #print(boardNum)
                #print(r1, c1)
                #print(expectCoords)                
                r2 = expectCoords[0]
                c2 = expectCoords[1]
                distanceSum = abs(r1 - r2) + abs(c1 - c2)   #calculates the distance sum
                #print(distanceSum)
                #print()
                totalSum = totalSum + distanceSum           #adds the distance sum to the total sum
        #print(totalSum) #check if it worked properly
        return totalSum
    
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
        After all moves are processed, go through the list and find the board with the smallest sum of Depth and Manhattan Distance (or use a priority queue and use .get() to get the smallest sum)
        Once the board is found, add it to the list. Check if the board is solved, and if it is, return the path that was taken to get to it.
        Otherwise, the algorithm goes back to the beginning of the while loop.
        """
        currentBoard = TilePuzzle(self.get_board()).copy()
        #print("currentBoard")
        #print(currentBoard.get_board())
        reverseMove = "none because this is the start of the puzzle"
        moveQueue = PriorityQueue()
        depth = 0
        movesList = []
        chosenMoveTuple = (0, (0, 0, [], reverseMove, depth, currentBoard.get_board()))
        while(True):
        #for test in range(0, 20):
            #moveQueue = PriorityQueue()
            depth = len(movesList)
            currentBoard = TilePuzzle(chosenMoveTuple[1][5]).copy()
            if currentBoard.testIfPossible("up") == True and reverseMove != "up":
                copyBoard = TilePuzzle(currentBoard.get_board()).copy()
                copyBoard.perform_move("up")
                sum = copyBoard.getManhattanDistanceSum(copyBoard) + depth #NEED TO ADD ManhattanDistanceSum AND the current depth, so that would be the distance of movesList
                #print(sum)
                #print("up")
                moveTuple = (sum, 1 ,movesList, "up", depth, copyBoard.get_board()) #IMPORTANT note: the 1 shown in the tuple is necessary for the priority queue to work, without it, it will prioritize alphabetical order first, making it prioritize "down" as its movement of choice if there are any ties. This is contrary to what the instruction examples show.
                moveQueue.put((sum, moveTuple)) #did (sum, moveTuple) in case PriorityQueue only worked with tuples with only two elements
            if currentBoard.testIfPossible("down") == True and reverseMove != "down":
                copyBoard = TilePuzzle(currentBoard.get_board()).copy()
                copyBoard.perform_move("down")
                sum = copyBoard.getManhattanDistanceSum(copyBoard) + depth
                #print(sum)
                #print("down")
                moveTuple = (sum, 2 ,movesList, "down", depth, copyBoard.get_board())
                moveQueue.put((sum, moveTuple))
            if currentBoard.testIfPossible("left") == True and reverseMove != "left":
                copyBoard = TilePuzzle(currentBoard.get_board()).copy()
                copyBoard.perform_move("left")
                sum = copyBoard.getManhattanDistanceSum(copyBoard) + depth
                #print(sum)
                #print("left")
                moveTuple = (sum, 3 ,movesList, "left", depth, copyBoard.get_board())
                moveQueue.put((sum, moveTuple))
            if currentBoard.testIfPossible("right") == True and reverseMove != "right":
                copyBoard = TilePuzzle(currentBoard.get_board()).copy()
                copyBoard.perform_move("right")
                sum = copyBoard.getManhattanDistanceSum(copyBoard) + depth
                #print(sum)
                #print("right")
                moveTuple = (sum, 4 ,movesList, "right", depth, copyBoard.get_board())
                moveQueue.put((sum, moveTuple))
            #print(moveQueue.queue[0])
            #print(moveQueue.queue[1])
            #print(moveQueue.queue[2])
            chosenMoveTuple = moveQueue.get() #this should yield the moveTuple
            #print(chosenMoveTuple)
            #print()
            movesList = chosenMoveTuple[1][2].copy() #copy the list
            chosenMove = chosenMoveTuple[1][3]
            #print("chosenMove:")
            #print(chosenMove)
            #print()

            reverseMove = calculateReverseMove(chosenMove) #chosenMove should be the move itself, which should be a string
            movesList.append(chosenMove)
            currentBoard.perform_move(chosenMove)
            #print(movesList)
            if currentBoard.is_solved() == True:
                #print("finished")
                #print(currentBoard.get_board())
                return movesList

        #pass

############################################################
# Section 2: Grid Navigation
############################################################
def calcEndDist(point, end): #calculates the distance from a point to the end point
    pointX = point[0]
    pointY = point[1]
    endX = end[0]
    endY = end[1]
    xDist = abs(endX - pointX)
    yDist = abs(endY - pointY)
    dist = math.hypot(xDist, yDist) * 10 #math.floor(math.hypot(xDist, yDist) * 10) #multiply by 10 and then use floor division to truncate the rest of the decimal off
    dist = math.floor(dist)
    return dist

def calcPathDistance(path): #traces the path taken to get an accurate measurement of the distance from start to the current point
    distance = 0
    for move in path:
        if move == "upLeft" or move == "upRight" or move == "downLeft" or move == "downRight":
            distance = distance + 14
        else:
            distance = distance + 10
    return distance

def findPossibleMoves(point, scene):
    numRows = len(scene)
    numCols = len(scene[0])
    movesList = ["up", "upLeft", "upRight", "left", "right", "down", "downLeft", "downRight"]
    pointRow = point[0]
    pointCol = point[1]
    """
    Removing based on the following positions:
    7 8 9
    4 5 6
    1 2 3
    """
    #print("chosen point: {}".format(point))
    if pointRow - 1 < 0:                   #positions 7, 8, 9
        #print("7, 8, 9")
        if pointCol - 1 < 0:               #position 7
            movesList.remove("left")
            movesList.remove("downLeft")
            #check for True in down, right, and downRight
            if scene[pointRow + 1][pointCol] == True:
                movesList.remove("down")
            if scene[pointRow][pointCol + 1] == True:
                movesList.remove("right")
            if scene[pointRow + 1][pointCol + 1] == True:
                movesList.remove("downRight")
        elif pointCol + 1 >= numCols:      #position 9
            movesList.remove("right")
            movesList.remove("downRight")
            #check for True in down, left, and downLeft
            if scene[pointRow + 1][pointCol] == True:
                movesList.remove("down")
            if scene[pointRow][pointCol - 1] == True:
                movesList.remove("left")
            if scene[pointRow + 1][pointCol - 1] == True:
                movesList.remove("downLeft")
        else:                              #position 8
            #check for True in down, right, downRight, left, and downLeft
            if scene[pointRow + 1][pointCol] == True:
                movesList.remove("down")
            if scene[pointRow][pointCol + 1] == True:
                movesList.remove("right")
            if scene[pointRow + 1][pointCol + 1] == True:
                movesList.remove("downRight")
            if scene[pointRow][pointCol - 1] == True:
                movesList.remove("left")
            if scene[pointRow + 1][pointCol - 1] == True:
                movesList.remove("downLeft")
        movesList.remove("up")
        movesList.remove("upLeft")
        movesList.remove("upRight")  
    elif pointRow + 1 >= numRows:          #positions 1, 2, 3
        #print("1, 2, 3")
        if pointCol - 1 < 0:               #position 1
            movesList.remove("left")
            movesList.remove("upLeft")
            #check for True in up, right, and upRight
            #print(scene[pointRow][pointCol + 1])
            if scene[pointRow - 1][pointCol] == True:
                movesList.remove("up")
            if scene[pointRow][pointCol + 1] == True:
                movesList.remove("right")
            if scene[pointRow - 1][pointCol + 1] == True:
                movesList.remove("upRight")
        elif pointCol + 1 >= numCols:      #position 3
            movesList.remove("right")
            movesList.remove("upRight")
            #check for True in up, left, and upLeft
            if scene[pointRow - 1][pointCol] == True:
                movesList.remove("up")
            if scene[pointRow][pointCol - 1] == True:
                movesList.remove("left")
            if scene[pointRow - 1][pointCol - 1] == True:
                movesList.remove("upLeft")
        else:                              #position 2
            if scene[pointRow][pointCol - 1] == True:
                movesList.remove("left")
            if scene[pointRow - 1][pointCol - 1] == True:
                movesList.remove("upLeft")
            if scene[pointRow - 1][pointCol] == True:
                movesList.remove("up")
            if scene[pointRow - 1][pointCol + 1] == True:
                movesList.remove("upRight")
            if scene[pointRow][pointCol + 1] == True:
                movesList.remove("right")
        movesList.remove("down")
        movesList.remove("downLeft")
        movesList.remove("downRight")
                                           
        
    elif pointCol - 1 < 0:                 #position 4
        #check for True in up, right, upRight, down, and downRight
        #print("4")
        if scene[pointRow - 1][pointCol] == True:
            movesList.remove("up")
        if scene[pointRow][pointCol + 1] == True:
            movesList.remove("right")
        if scene[pointRow - 1][pointCol + 1] == True:
            movesList.remove("upRight")
        if scene[pointRow + 1][pointCol] == True:
            movesList.remove("down")
        if scene[pointRow + 1][pointCol + 1] == True:
            movesList.remove("downRight")
        movesList.remove("left")
        movesList.remove("upLeft")
        movesList.remove("downLeft")
    elif pointCol + 1 >= numCols:           #position 6
        #check for True in up, left, upLeft, down, and downLeft
        #print("6")
        if scene[pointRow - 1][pointCol] == True:
            movesList.remove("up")
        if scene[pointRow][pointCol - 1] == True:
            movesList.remove("left")
        if scene[pointRow - 1][pointCol - 1] == True:
            movesList.remove("upLeft")
        if scene[pointRow + 1][pointCol] == True:
            movesList.remove("down")
        if scene[pointRow + 1][pointCol - 1] == True:
            movesList.remove("downLeft")
        movesList.remove("right")
        movesList.remove("upRight")
        movesList.remove("downRight")
    else:                                  #position 5
        #check every direction if there exists a True, remove that move if there is
        #print("5")
        if scene[pointRow - 1][pointCol] == True:
            movesList.remove("up")        
        if scene[pointRow + 1][pointCol] == True:
            movesList.remove("down")
        if scene[pointRow][pointCol + 1] == True:
            movesList.remove("right")
        if scene[pointRow][pointCol - 1] == True:
            movesList.remove("left")
        if scene[pointRow - 1][pointCol + 1] == True:
            movesList.remove("upRight")
        if scene[pointRow - 1][pointCol - 1] == True:
            movesList.remove("upLeft")
        if scene[pointRow + 1][pointCol + 1] == True:
            movesList.remove("downRight")
        if scene[pointRow + 1][pointCol - 1] == True:
            movesList.remove("downLeft")
    
    #STILL NEED TO CHECK FOR ANY SPACES THAT SAY TRUE, add this later when I have time, probably by using scene[x][y], whatever x and y are supposed to be
    #Update: As of the time I'm writing this, it turns out the algorithm I wrote ALMOST works (when looking at the output, anyway). Turns out, not checking
    #for the spaces that say True just makes it so the algorithm traverses through spaces that say True as well. Looks like it's time to fix this.

    #print(scene)
    #print(movesList) Test to make sure this works
    return movesList

def getMoveValue(move, point, scene): #assumes that only valid moves are being put into this
    pointRow = point[0]
    pointCol = point[1]
    newPointRow = pointRow
    newPointCol = pointCol
    if move == "up":
        newPointRow = pointRow - 1
    if move == "upLeft":
        newPointRow = pointRow - 1
        newPointCol = pointCol - 1
    if move == "upRight":
        newPointRow = pointRow - 1
        newPointCol = pointCol + 1
    if move == "down":
        newPointRow = pointRow + 1
    if move == "downLeft":
        newPointRow = pointRow + 1
        newPointCol = pointCol - 1
    if move == "downRight":
        newPointRow = pointRow + 1
        newPointCol = pointCol + 1
    if move == "left":
        newPointCol = pointCol - 1
    if move == "right":
        newPointCol = pointCol + 1
    newPoint = (newPointRow, newPointCol)
    #print newPoint
    return newPoint

def find_path(start, goal, scene):
    startRow = start[0]
    startCol = start[1]
    goalRow = goal[0]
    goalCol = goal[1]

    #checks if the start point or goal point lies on an obstacle (which means to check if the coordinates for either is True), return None if this is the case
    if scene[startRow][startCol] == True:
        return None
    if scene[goalRow][goalCol] == True:
        return None
    if startRow == goalRow and startCol == goalCol: #if start and goal are the same, just return the goal tuple (or start tuple, they're both supposed to be the same anyway)
        return goal
    
    """
    For the terminating case, since I'll probably use a priority queue because I'm using A star search, if the priority queue is empty,
    that means that all possible areas have been traversed and it is impossible to reach the goal. This might need to be changes, but
    for now, it seems to be the best terminating case. 
    Something important to note: after finishing looking at all of a node's options, the node should not be considered again. It's probably
    best to move it to a list of nodes to not consider, so if that particular node shows up, I can check if the node is on the list to not
    consider so it won't be considered in calculations. Eventually, all nodes that are reachable from the starting node should be put onto
    that list if the end node cannot be reached.
    """
    #Also, make something that checks if it is possible to even move from the start position. Check every possible move, and if all of them fail, return None.
    
    """
    To start, make a while loop that terminates if every possible point from the start point has been explored. The best way to do this is to probably
    use a priority queue that is filled with potential points that have been found but have not finished considering all of its options, and when that
    queue is empty (use .empty() on a priority queue, and if True is returned, that's when the while loop can terminate), set something so it can terminate.
    To run the actual algorithm, I'll want to follow some of the steps from the a star algorithm in question 1.
    Another thing I'll want to do is make a helper function that calculates the distance from the current point to the end point.
        Not to mention a helper function that tests if a specific direction is even possible, or better yet, a function that returns a list of directions
        that are actually possible.
    But in the while loop, I should try every possible direction. After that, I'll choose the most optimal direction based on the sum of the distance to the
    end point and the distance of the amount currently traveled (or the length of path list). Other than that, everything else should be similar to question 1's
    work, really.

    One more thing, since Euclidian distance is supposed to be used, make vertical and horizontal equal to 10, but diagonals should be 14, since normally it would
    be about 1.4 due to using the Pythagorean theorem to get the hypotenuse, so multiply all number by 10 so cardinal direction is 10, and diagonal is 14. This just
    keeps things simpler with just integers.
    """

    potentialQueue = PriorityQueue()
    path = [start]
    movesPath = []
    startingDist = calcEndDist(start, goal)
    #startTuple = (startingDist + 0, startingDist, 0, start, path) #Tuple is made like this: (sum of distance to end and depth, distance to end, distance(depth) of path, current point tuple, path list)
    #potentialQueue.put(startTuple)
    finishedList = [] #while running, check if a point that is found is already in this, if it is, skip over that point
    
    obstructed = False
    currentPoint = start
    #while obstructed == False:     
    for test in range(0, 20):   
        #depth = len(path)
        newDepth = 0
        #print()
        possibleMoves = findPossibleMoves(currentPoint, scene)
        #print("possible moves:")
        #print(possibleMoves)
        for move in possibleMoves: #iterate through all the possible moves (which are just strings of directions right now) and prepare their tuples and put them in the priority queue
            #probably should get the sum of the goalDistance and path distance for each move, then select the lowest one (that might require use of the priority queue)
            newPoint = getMoveValue(move, currentPoint, scene) #sends the direction to move to the helper function to get the new point tuple:should be a tuple of the new point found after doing the move
            if newPoint not in finishedList: #checks if the newPoint has already been explored, if it is not, continue with the following code
                #print("current considered move: {}".format(move))
                moveRow = newPoint[0]
                moveCol = newPoint[1]
                currentMovePath = path.copy()
                currentMovePath.append(newPoint)
                currentTakenMovesPath = movesPath.copy()
                currentTakenMovesPath.append(move)
                if moveRow == goalRow and moveCol == goalCol: #if goal point is found (by comparing the current point coords to the goal point coords), return the path list
                    return currentMovePath
                
                #goal point was not found, continue with the search
                distToEnd = calcEndDist(newPoint, goal)
                travelledDist = calcPathDistance(currentTakenMovesPath) #traces the path that was taken to get an accurate distance from start to current point
                sum = travelledDist + distToEnd
                #print("sum: {}".format(sum))
                #print("distToEnd: {}".format(distToEnd))

                diagPenalty = 1                         #created so the algorithm would prefer vertical and horizontal movement over diagonal movement in the event of a deadlock
                if move == "upLeft" or move == "upRight" or move == "downLeft" or move == "downRight":
                    diagPenalty = 999
                
                preferLessMoves = len(currentMovePath)  #created so the algorithm would prefer paths with less moves in the path in the event of a deadlock

                #moveTuple = (sum, distToEnd, newDepth, newPoint, currentMovePath, move)
                #Create a tuple that contains the following(sum of distance to end and distance from start, distance to end, penalty for diagonal, length of total moves taken, tuple of the next point, list of points on the path, string of the next move, list of moves taken on the path)
                moveTuple = (sum, distToEnd, diagPenalty, preferLessMoves, newPoint, currentMovePath, move, currentTakenMovesPath) 
                potentialQueue.put(moveTuple)
        
        if potentialQueue.empty() == True: #if all points that are accessible from start have been explored, there is nothing left to do but return None
            obstructed = True              #this probably doesn't really need to be done, but I'll set it just in case
            return None
        
        #now use .get() from the priority queue, it should use the sum as its main way to determine priority, then it should use distToEnd
        finishedList.append(currentPoint)              #append currentPoint to finishedList since we are done exploring currentPoint's options
        #print("current potential queue: {}".format(potentialQueue.queue))
        #while potentialQueue.queue[0][3] in finishedList: #designed to get rid of duplicate points
            #currentPointTuple = potentialQueue.get()
        currentPointTuple = potentialQueue.get()       #if there's a problem here, that means the if statement that checks if potentialQueue is empty didn't work somehow, and I have no idea what to do about that
        currentPoint = currentPointTuple[4]
        truePath = currentPointTuple[5]
        #print("new current tuple: {}".format(currentPointTuple))
        #print("new current point: {}".format(currentPoint))
        #print("next move to take: {}".format(currentPointTuple[6]))
        #path.append(currentPoint)                      #by the way, currentPoint is supposed to be a tuple with just the row and col values, like this: (row, col)
        path = truePath.copy()
        movesPath = currentPointTuple[7].copy()
        #print("\n")
        #print(currentPoint)
        #now that the new point has been chosen, it should go back to the beginning of the loop and start the process over, but I still feel like something's missing
        #I figured out what was missing, I forgot to append currentPoint to path and also forgot to change the depth setting

    #pass

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

print("\nfinding solutions using a star")
b = [[4,1,2], [0,5,3], [7,8,6]]
#print("b")
#print(b)
p = TilePuzzle(b)
print(p.find_solution_a_star())

print()
b = [[1,2,3], [4,0,5], [6,7,8]]
#print(b)
p = TilePuzzle(b)
print(p.find_solution_a_star())

print("\n Grid Navigation Tests")
scene = [[False, False, False], [False, True , False], [False, False, False]]
print(find_path((0, 0), (2, 1), scene))
print()

scene = [[False, True, False], [False, True, False], [False, True, False]]
print(find_path((0, 0), (0, 2), scene))
print()

scene = [[False, False, False, False], [True, True, False, True], [False, False, True, False], [False, False, True, False]]
print("----------------------")
print(find_path((3, 0), (3, 3), scene))
print()