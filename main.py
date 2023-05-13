# create a board and initialize it by zeros
import math
from random import random

RowsNum = 6
ColsNum = 7
Empty = 0
PLAYER = 1
OPPONENT = 2  #AI
def createBoard():
    board = []
    for i in range(RowsNum):
        row = [0] * ColsNum
        board.append(row)
    return board

# print the board
def printBoard(board):
    for row in board:
        print(row)

def dropPiece(board, row, col, piece):
    board[row][col] = piece
#check if the cell in last row in a specif col is empty to drop a piece
def isEmpty(board, col):
    return board[RowsNum-1][col] == 0

# get the deepest available cell, return its row index
def getTheDeeppestEmptyRow(board, col):
    for i in range(RowsNum -1, -1, -1):
        if board[i][col] == 0:
            return i
    return -1

# function to get all the valid cols
def get_valid_locations(board):
	valid_locations = []
	for col in range(ColsNum):
		if isEmpty(board, col):
			valid_locations.append(col)
	return valid_locations


def playerScore(board, piece):
    #check horizontal winning
    for i in range(RowsNum):
        for j in range(ColsNum-3):
            if board[i][j] == piece and board[i][j+1] == piece and board[i][j+2] == piece and board[i][j+3] == piece:
                return True
    #check vertical winning
    for i in range(RowsNum-3):
        for j in range(ColsNum):
            if board[i][j] == piece and board[i+1][j] == piece and board[i+2][j] == piece and board[i+3][j] == piece:
                return True

    # check negative diagonal winning
    for i in range(RowsNum-3):
        for j in range(ColsNum - 3):
            if board[i][j] == piece and board[i + 1][j-1] == piece and board[i + 2][j-2] == piece and board[i + 3][j-3] == piece:
                return True

        # check positive diagonal winning
        for i in range(RowsNum - 3):
            for j in range(ColsNum - 3):
                if board[i][j] == piece and board[i + 1][j + 1] == piece and board[i + 2][j + 2] == piece and board[i + 3][j + 3] == piece:
                    return True
# calculate the score for each possible window, that we pass to the function
def calculateScore(window, piece):
    aiPiece = 2
    opponentPlayer = 1
    if piece == 1:
        opponentPlayer = 2
    if window.count(piece) == 4:
        return 1000
    elif window.count(piece) == 3 and window.count(Empty) == 1:
        return 5
    elif window.count(piece) == 2 and window.count(Empty) == 2:
        return 2
    elif window.count(opponentPlayer) == 3 and window.count(Empty) == 1:
        return -4



def isTerminalNode(board):
    arr_length = len(get_valid_locations(board))
    if playerScore(board, PLAYER) or playerScore(board, OPPONENT) or arr_length == 0:
        return True

def minimax(board, depth, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = isTerminalNode(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if playerScore(board, OPPONENT):
				return None, 100000000000000
			elif playerScore(board, PLAYER):
				return None, -10000000000000
			else: # Game is over, no more valid moves
				return None, 0
		else: # Depth is zero
			return None, calculateScore(board, OPPONENT)
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = getTheDeeppestEmptyRow(board, col)
			if row is None:
				continue
			b_copy = board.copy()
			dropPiece(b_copy, row, col, OPPONENT)
			new_score = minimax(b_copy, depth-1, False)[1]
			if new_score > value:
				value = new_score
				column = col
		return column, value
	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = getTheDeeppestEmptyRow(board, col)
			if row is None:
				continue
			b_copy = board.copy()
			dropPiece(b_copy, row, col, PLAYER)
			new_score = minimax(b_copy, depth-1, True)[1]
			if new_score < value:
				value = new_score
				column = col
		return column, value



flag = True
board = createBoard()
tempBoard = board
turn = 1
while(flag):
    #printBoard(board)
    if turn == 1:
        col = int(input("Player 1, Enter the col: "))
        row = getTheDeeppestEmptyRow(tempBoard, col-1)
        piece = 1
        if row != -1:
            dropPiece(tempBoard, row, col-1, piece)
            if playerScore(board, piece):
                print("Playe 1 wins!!")
                flag = False
        else:
            print("Select another col!")
        board = tempBoard
        printBoard(board)
        print("------------")
        turn = 2
    elif turn == 2:
        col = int(input("Player 2, Enter the col: "))
        row = getTheDeeppestEmptyRow(tempBoard, col - 1)
        piece = 2
        if row != -1:
            dropPiece(tempBoard, row, col - 1, piece)
            if playerScore(board, piece):
                print("Player 2 wins!!")
                flag = False
        else:
            print("Select another col!")
        board = tempBoard
        #print("board:", board[0][0])
        printBoard(board)
        print("------------")
        turn = 1
if flag == True:
    print("No one wins!")

    #if(turn == 0):